import io
import time
import threading
import logging
import numpy as np
from PIL import Image

# Import tflite runtime if available; allows tests to inject a mock interpreter
try:
    import tflite_runtime.interpreter as tflite  # type: ignore
except Exception:
    tflite = None

logger = logging.getLogger(__name__)


class MLService:
    """Service d'inférence TFLite robuste.

    - Permet l'injection d'une classe d'interpreter (interpreter_cls) pour les tests.
    - Gère quantization, shapes dynamiques, thread-safety et logging.
    """

    def __init__(self, model_path: str = "ml/anemia/model.tflite", interpreter_cls=None, warmup: bool = False):
        if interpreter_cls is None:
            if tflite is None:
                raise RuntimeError("tflite runtime is not installed. Install tflite-runtime or pass interpreter_cls for tests.")
            interpreter_cls = tflite.Interpreter

        self.model_path = model_path
        self.interpreter = interpreter_cls(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()[0]
        self.output_details = self.interpreter.get_output_details()[0]

        # Thread-safety (important with Flask/Gunicorn)
        self._lock = threading.Lock()

        # Example labels (should be loaded from a config file in prod)
        self.labels = ["normal", "anemia"]

        if warmup:
            # Warm-up call to reduce first-inference latency
            try:
                with self._lock:
                    # set minimal dummy input if shape allows
                    shape = self.input_details.get("shape", [1, 1, 1, 3])
                    dummy = np.zeros(shape, dtype=self.input_details.get("dtype", np.float32))
                    self.interpreter.set_tensor(self.input_details["index"], dummy)
                    self.interpreter.invoke()
            except Exception:
                logger.debug("Warmup failed; continuing without warmup", exc_info=True)

        logger.info("MLService initialized (model=%s)", model_path)

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        e = np.exp(x - np.max(x))
        return e / e.sum(axis=-1, keepdims=True)

    def analyze_bytes(self, image_bytes: bytes) -> dict:
        start = time.time()

        # --- Image loading ---
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception:
            logger.warning("Invalid image provided")
            raise ValueError("Invalid image file")

        # --- Input shape (robust to dynamic shapes) ---
        shape = self.input_details.get("shape", [1, 224, 224, 3])
        # shape format assumed (N,H,W,C) by default
        h = int(shape[1]) if shape[1] and shape[1] > 0 else img.height
        w = int(shape[2]) if shape[2] and shape[2] > 0 else img.width
        img = img.resize((w, h))

        arr = np.asarray(img)

        # Ensure channels last
        if arr.ndim == 3 and arr.shape[2] not in (1, 3):
            # try channel-first fallback
            if arr.shape[0] in (1, 3):
                arr = np.transpose(arr, (1, 2, 0))

        # --- Dtype + quantization ---
        input_dtype = self.input_details.get("dtype", np.float32)
        quant = self.input_details.get("quantization", (0.0, 0))
        scale = float(quant[0]) if quant else 0.0
        zero_point = int(quant[1]) if quant else 0

        if np.issubdtype(input_dtype, np.floating):
            arr = arr.astype(np.float32) / 255.0
        else:
            # Quantized model: convert to quantized integers correctly
            if scale == 0.0:
                # Fallback: treat as non-quantized uint8
                arr = arr.astype(np.uint8)
            else:
                # arr in [0..255] -> normalized [0..1] -> quantized
                arr = (arr.astype(np.float32) / 255.0) / scale + zero_point
                arr = np.round(arr).astype(np.int32)
                arr = np.clip(arr, np.iinfo(np.uint8).min, np.iinfo(np.uint8).max).astype(np.uint8)

        input_data = np.expand_dims(arr, axis=0)

        # --- Inference (thread-safe) ---
        try:
            with self._lock:
                self.interpreter.set_tensor(self.input_details["index"], input_data)
                self.interpreter.invoke()
                output = self.interpreter.get_tensor(self.output_details["index"])
        except Exception as e:
            logger.exception("Inference failed")
            raise RuntimeError("Inference error") from e

        # --- Output post-processing ---
        output = np.squeeze(output)

        # If output appears to be logits, apply softmax
        probs = None
        if output.ndim == 1 and not np.all((0 <= output) & (output <= 1)):
            probs = self._softmax(output)
        else:
            probs = np.asarray(output, dtype=np.float32)

        idx = int(np.argmax(probs))
        confidence = float(probs[idx])

        # --- Risk mapping (documented) ---
        if confidence > 0.75:
            risk = "high"
        elif confidence > 0.5:
            risk = "medium"
        else:
            risk = "low"

        latency_ms = int((time.time() - start) * 1000)

        logger.info(
            "Inference done | label=%s confidence=%.2f latency=%dms",
            self.labels[idx], confidence, latency_ms
        )

        return {
            "condition": "anemia",
            "label": self.labels[idx],
            "risk_level": risk,
            "confidence": round(confidence, 2),
            "latency_ms": latency_ms,
            "recommendation": "Blood test recommended",
            "raw": probs.tolist()
        }