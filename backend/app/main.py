from flask import Flask
from flask_cors import CORS
from backend.app.routes.predict import predict_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(predict_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
