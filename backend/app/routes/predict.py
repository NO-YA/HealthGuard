import os
import uuid
from flask import Blueprint, request, jsonify
from backend.app.services.ml_service import run_inference

predict_bp = Blueprint("predict", __name__)

UPLOAD_DIR = "tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@predict_bp.route("/predict/<task>", methods=["POST"])
def predict(task):
    if "image" not in request.files:
        return jsonify({"error": "Image manquante"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "Nom de fichier vide"}), 400

    filename = f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, filename)
    image.save(image_path)

    try:
        result = run_inference(task, image_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
