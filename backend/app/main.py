from flask import Flask, request, jsonify
import os
from .ml_service import MLService

app = Flask(__name__)
ml_service = MLService()
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)