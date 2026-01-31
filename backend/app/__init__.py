cat > backend/app/__init__.py << 'EOF'
"""Flask app factory"""
from flask import Flask
from flask_cors import CORS
from mongoengine import connect, disconnect
import os

def create_app(config_name='development'):
    """
    Create and configure Flask application
    
    Args:
        config_name: 'development', 'testing', or 'production'
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'development':
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from app.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    
    # CORS
    CORS(app)
    
    # MongoDB
    _init_mongodb(app)
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(e):
        return {'error': 'Bad request'}, 400
    
    return app

def _init_mongodb(app):
    """Initialize MongoDB connection"""
    mongo_uri = app.config.get('MONGO_URI')
    db_name = app.config.get('MONGO_DB_NAME')
    
    try:
        connect(
            db_name,
            host=mongo_uri,
            serverSelectionTimeoutMS=5000
        )
        app.logger.info(f"Connected to MongoDB: {db_name}")
    except Exception as e:
        app.logger.error(f"MongoDB connection error: {e}")
        raise
EOF