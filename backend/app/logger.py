"""
Configuration du logging pour HealthGuard
Support des logs structurés JSON et texte
"""
import logging
import logging.config
from pathlib import Path
from pythonjsonlogger import jsonlogger
from .config import settings


def setup_logging():
    """Configure le logging pour l'application"""
    
    # Créer le répertoire logs s'il n'existe pas
    log_dir = settings.LOG_DIR
    log_dir.mkdir(exist_ok=True)
    
    # Config de base
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': settings.LOG_LEVEL,
                'formatter': 'json' if settings.LOG_FORMAT == 'json' else 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': settings.LOG_LEVEL,
                'formatter': 'json' if settings.LOG_FORMAT == 'json' else 'detailed',
                'filename': log_dir / 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': log_dir / 'error.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # root logger
                'level': settings.LOG_LEVEL,
                'handlers': ['console', 'file', 'error_file']
            },
            'flask.app': {
                'level': settings.LOG_LEVEL,
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'werkzeug': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    }
    
    logging.config.dictConfig(config)
    return logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    """Obtenir un logger nommé"""
    return logging.getLogger(name)
