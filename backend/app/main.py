from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """pouverifier si l'application fonctionne correctement."""
    return jsonify({"status": "healthy"}), 200


@app.route('/api/predict', methods=['POST'])
def predict():
    """endpoint principal pour la simulation du jour 1"""
    return jsonify ({
        "success": True,
        "diagnosis": {
            "diabetes_risk": 0.15,
            "anemia_risk": 0.08,
            "deficiency_risk": 0.022,
        }
    })
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)