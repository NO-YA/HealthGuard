import threading
import time
import numpy as np
import pytest
from backend.app.ml_service import MLService


class MockInterpreter:
    def __init__(self, model_path=None):
        # input_details/out_details mimic tflite structure
        self._input = {"index": 0, "shape": [1, 32, 32, 3], "dtype": np.float32, "quantization": (0.0, 0)}
        self._output = {"index": 0, "shape": [1, 2], "dtype": np.float32}
        self._tensor = None

    def allocate_tensors(self):
        pass

    def get_input_details(self):
        return [self._input]

    def get_output_details(self):
        return [self._output]

    def set_tensor(self, index, data):
        self._tensor = data

    def invoke(self):
        # fake some computation time
        time.sleep(0.01)

    def get_tensor(self, index):
        # return deterministic logits favoring class 1
        return np.array([[0.1, 0.9]], dtype=np.float32)


class MockQuantInterpreter(MockInterpreter):
    def __init__(self, model_path=None):
        super().__init__(model_path)
        self._input = {"index": 0, "shape": [1, 8, 8, 3], "dtype": np.uint8, "quantization": (0.1, 128)}
        self._output = {"index": 0, "shape": [1, 2], "dtype": np.uint8}

    def get_tensor(self, index):
        # return quantized-like values but we'll treat as probabilities
        return np.array([[10, 200]], dtype=np.float32)


def test_analyze_bytes_float_model():
    svc = MLService(interpreter_cls=MockInterpreter)
    # create a tiny valid RGB image bytes
    from PIL import Image
    import io
    buf = io.BytesIO()
    Image.new('RGB', (32, 32), (255, 0, 0)).save(buf, format='PNG')
    img = buf.getvalue()
    res = svc.analyze_bytes(img)
    diag = res["diagnosis"]
    assert diag["label"] in ("normal", "anemia")
    assert 0.0 <= diag["confidence"] <= 1.0
    assert diag["risk_level"] in ("low", "medium", "high")


def test_analyze_bytes_quantized_model():
    svc = MLService(interpreter_cls=MockQuantInterpreter)
    from PIL import Image
    import io
    buf = io.BytesIO()
    Image.new('RGB', (32, 32), (0, 255, 0)).save(buf, format='PNG')
    img = buf.getvalue()
    res = svc.analyze_bytes(img)
    diag = res["diagnosis"]
    assert "raw_output" in diag
    assert isinstance(diag["raw_output"], list)


def test_invalid_image_raises():
    svc = MLService(interpreter_cls=MockInterpreter)
    with pytest.raises(ValueError):
        svc.analyze_bytes(b"not an image")


def test_thread_safety_multiple_calls():
    svc = MLService(interpreter_cls=MockInterpreter)

    def call_it():
        from PIL import Image
        import io
        buf = io.BytesIO()
        Image.new('RGB', (32, 32), (0, 0, 255)).save(buf, format='PNG')
        img = buf.getvalue()
        for _ in range(5):
            svc.analyze_bytes(img)

    threads = [threading.Thread(target=call_it) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # if no exception, consider passed
    assert True
