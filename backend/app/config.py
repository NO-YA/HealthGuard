"""
Configuration centralisée pour l'application HealthGuard
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Flask
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Server
    PORT: int = int(os.getenv('PORT', 5000))
    HOST: str = os.getenv('HOST', '0.0.0.0')
    
    # Database
    MONGO_URI: str = os.getenv('MONGO_URI', 'mongodb://localhost:27017/healthguard')
    MONGO_DB_NAME: str = os.getenv('MONGO_DB_NAME', 'healthguard')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', 'json')  # json ou text
    
    # ML Models
    MODELS_PATH: str = os.getenv('MODELS_PATH', './ml')
    CONFIDENCE_THRESHOLD: float = float(os.getenv('CONFIDENCE_THRESHOLD', 0.75))
    
    # Security
    ENABLE_CORS: bool = os.getenv('ENABLE_CORS', 'True').lower() == 'true'
    CORS_ORIGINS: list = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5000').split(',')
    
    # Redis
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_ENABLED: bool = os.getenv('REDIS_ENABLED', 'False').lower() == 'true'
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    LOG_DIR: Path = BASE_DIR / 'logs'
    
    class Config:
        env_file = '.env'
        case_sensitive = True
    
    def __init__(self, **data):
        super().__init__(**data)
        # Créer le répertoire des logs s'il n'existe pas
        self.LOG_DIR.mkdir(exist_ok=True)


# Instance globale
settings = Settings()
