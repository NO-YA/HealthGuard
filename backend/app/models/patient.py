cat > backend/app/models/patient.py << 'EOF'
"""Patient model for MongoDB"""
from mongoengine import Document, StringField, IntField, DateTimeField, EmailField
from datetime import datetime

class Patient(Document):
    """Patient data model"""
    
    email = EmailField(required=True, unique=True)
    first_name = StringField()
    last_name = StringField()
    age = IntField()
    gender = StringField(choices=['M', 'F', 'Other'])
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'patients',
        'indexes': [
            'email',
            'created_at'
        ]
    }
    
    def to_json(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'created_at': self.created_at.isoformat()
        }
    
    def __str__(self):
        return f"Patient({self.email})"
EOF