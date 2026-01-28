# Fichier 3: backend/app/ml_service.py - La Logique IA
class MLService:
    """Service qui simule l'analyse ML"""
    
    def analyze_image(self, image_path):
        """Simule l'analyse d'une image médicale"""
        # Jour 1: Simulation simple
        # Jour 3: Remplacer par du vrai TensorFlow
        
        import random
        return {
            "conditions": {
                "diabetic_retinopathy": {
                    "probability": random.uniform(0.1, 0.4),
                    "confidence": 0.85
                },
                "anemia": {
                    "probability": random.uniform(0.05, 0.3),
                    "confidence": 0.78
                }
            },
            "recommendations": [
                "Consult an ophthalmologist",
                "Schedule a blood test"
            ]
        }