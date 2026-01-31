cat > backend/app/api/__init__.py << 'EOF'
"""API blueprint"""
from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.api import routes
EOF