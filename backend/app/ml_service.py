cat > backend/app/ml_service.py << 'EOF'
"""Machine Learning service"""
from pathlib import Path
import numpy as np
import cv2
from typing import Dict, Any
import sys

# Add ml directory to path
ml_path = Path(__file__).parent.parent.parent / 'ml'
sys.path.insert(0, str(ml_path))

from diabetes.loader import DiabetesModelLoader
from anemia.loader import AnemiaModelLoader  
from deficiency.loader import DeficiencyModelLoader

class MLService:
    """Service for ML model predictions"""
    
    def __init__(self):
        """Initialize ML models"""
        self.diabetes_loader = DiabetesModelLoader()
        self.anemia_loader = AnemiaModelLoader()
        self.deficiency_loader = DeficiencyModelLoader()
        
        # Load models (if implemented)
        # self.diabetes_loader.load_model()
        # self.anemia_loader.load_model()
        # self.deficiency_loader.load_model()
    
    def predict_all(self, image_path: str) -> Dict[str, Any]:
        """
        Run all three ML models on image
        
        Args:
            image_path: Path to image file
        
        Returns:
            Dict with predictions from all 3 models
        """
        try:
            # Load and preprocess image
            image = self._load_image(image_path)
            
            # Run predictions
            results = {
                'diabetes': self.diabetes_loader.predict(image),
                'anemia': self.anemia_loader.predict(image),
                'deficiency': self.deficiency_loader.predict(image),
            }
            
            return results
            
        except Exception as e:
            raise Exception(f"ML prediction error: {e}")
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """
        Load and preprocess image
        
        Args:
            image_path: Path to image file
        
        Returns:
            Preprocessed image as numpy array
        """
        # Read image
        image = cv2.imread(image_path)
        
        if image is None:
            raise Exception(f"Could not load image: {image_path}")
        
        # Resize to standard size
        image = cv2.resize(image, (224, 224))
        
        # Normalize
        image = image.astype(np.float32) / 255.0
        
        return image
EOF