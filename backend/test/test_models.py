import pytest
from app.models import Patient, Analysis

def test_create_patient():
    patient = Patient(email='test@example.com', age=30)
    patient.save()
    assert patient.id is not None

def test_get_patient():
    patient = Patient.objects(email='test@example.com').first()
    assert patient is not None