cat > backend/app/config.py << 'EOF'
"""Flask configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    DEBUG = False
    TESTING = False
    
    # MongoDB
    MONGO_URI = os.getenv(
        'MONGO_URI',
        'mongodb://admin:password@localhost:27017/healthguard?authSource=admin'
    )
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'healthguard')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')
    
    # Upload
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/healthguard_uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/healthguard_test'
    MONGO_DB_NAME = 'healthguard_test'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
EOF