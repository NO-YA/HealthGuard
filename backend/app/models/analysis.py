cat > backend/app/models/analysis.py << 'EOF'
"""Analysis model for MongoDB"""
from mongoengine import Document, StringField, ReferenceField, DictField, ListField, DateTimeField, FloatField, BooleanField
from datetime import datetime
from app.models.patient import Patient

class Analysis(Document):
    """Medical analysis results"""
    
    patient = ReferenceField(Patient, required=True)
    image_path = StringField(required=True)
    image_name = StringField()
    
    # Status: pending, processing, completed, error
    status = StringField(
        choices=['pending', 'processing', 'completed', 'error'],
        default='pending'
    )
    
    # ML Results
    results = DictField()  # {diabetes: {...}, anemia: {...}, deficiency: {...}}
    error_message = StringField()
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    completed_at = DateTimeField()
    processing_time_ms = FloatField()
    
    meta = {
        'collection': 'analyses',
        'indexes': [
            'patient',
            'status',
            'created_at'
        ]
    }
    
    def to_json(self):
        return {
            'id': str(self.id),
            'patient_id': str(self.patient.id),
            'image_name': self.image_name,
            'status': self.status,
            'results': self.results,
            'error': self.error_message,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'processing_time_ms': self.processing_time_ms
        }
    
    def __str__(self):
        return f"Analysis({self.patient.email})"
EOF