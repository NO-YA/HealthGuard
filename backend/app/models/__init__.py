cat > backend/app/models/__init__.py << 'EOF'
from app.models.patient import Patient
from app.models.analysis import Analysis

__all__ = ['Patient', 'Analysis']
EOF