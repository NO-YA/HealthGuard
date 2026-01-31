# Updater diabetes/loader.py
cat > backend/../ml/diabetes/loader.py << 'EOF'
"""
Loader pour le modèle de détection de diabète rétinopathique
"""
import json
from pathlib import Path
import numpy as np
from typing import Dict, Any


class DiabetesModelLoader:
    """Charge et gère le modèle ML de détection de diabète"""
    
    def __init__(self, model_dir: Path = None):
        if model_dir is None:
            model_dir = Path(__file__).parent
        
        self.model_dir = model_dir
        self.config = self._load_config()
        self.model = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration du modèle"""
        config_path = self.model_dir / 'config.json'
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def load_model(self):
        """Charge le modèle TensorFlow"""
        # TODO: Implémenter quand le modèle TensorFlow sera disponible
        pass
    
    def predict(self, image_data: np.ndarray) -> Dict[str, Any]:
        """Effectue une prédiction"""
        # Pour maintenant, retourner mock data
        # À remplacer par vraie prédiction
        return {
            'probability': 0.15,
            'confidence': 0.85,
            'severity': 'low',
            'recommendations': [
                'Schedule regular eye exams',
                'Monitor blood glucose levels'
            ]
        }
EOF