import os
from ml.utils.preprocessing import preprocess_image
from ml.utils.tflite_loader import TFLiteModel


BASE_MODEL_PATH = "ml/models/inference"


MODELS = {
    "diabetes": TFLiteModel(os.path.join(BASE_MODEL_PATH, "diabetes.tflite")),
    "anemia": TFLiteModel(os.path.join(BASE_MODEL_PATH, "anemia.tflite")),
    "deficiency": TFLiteModel(os.path.join(BASE_MODEL_PATH, "deficiency.tflite")),
}


def run_inference(task: str, image_path: str) -> dict:
    if task not in MODELS:
        raise ValueError("Modèle inconnu")

    image_tensor = preprocess_image(image_path)
    score = MODELS[task].predict(image_tensor)

    return {
        "task": task,
        "score": round(score, 4),
        "diagnosis": "positive" if score >= 0.5 else "negative",
        "confidence": round(score * 100, 2)
    }
