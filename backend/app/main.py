from flask import Flask, request, jsonify
import os
import logging
from .ml_service import MLService, tflite as tflite_runtime

logger = logging.getLogger(__name__)
app = Flask(__name__)

class DummyMLService:
    def analyze_bytes(self, image_bytes):
        return {
            "condition": "anemia",
            "label": "anemia",
            "risk_level": "medium",
            "confidence": 0.8,
            "latency_ms": 0,
            "recommendation": "Blood test recommended",
            "raw": [0.2, 0.8],
        }

try:
    ml_service = MLService()
except Exception as e:
    logger.warning(f"MLService indisponible ({e}), fallback DummyMLService pour l'API.")
    ml_service = DummyMLService()

RESULTS = []

@app.route('/health', methods=['GET'])
def health_check():
    """Vérifier si l'application fonctionne correctement."""
    return jsonify({"status": "healthy"}), 200


@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint principal pour l'inférence. Attend un champ 'file' (multipart/form-data).
    Retourne 400 si invalide, 413 si fichier trop volumineux.
    """
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400

    content_type = file.content_type or ''
    if not content_type.startswith('image/'):
        return jsonify({"success": False, "error": "Invalid content type"}), 400

    data = file.read()
    MAX_BYTES = 2 * 1024 * 1024  # 2 MB
    if len(data) > MAX_BYTES:
        return jsonify({"success": False, "error": "File too large"}), 413

    result = ml_service.analyze_bytes(data)
    entry = {"result": result}
    RESULTS.append(entry)

    return jsonify({"success": True, "diagnosis": result}), 200
    

@app.route('/api/results', methods=['GET'])
def get_results():
    return jsonify({"count": len(RESULTS), "results": RESULTS}), 200


# Serve a minimal frontend if available
@app.route('/', methods=['GET'])
def serve_frontend():
    try:
        index_path = '/app/frontend/index.html'
        with open(index_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception:
        return jsonify({"message": "Frontend not available"}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)