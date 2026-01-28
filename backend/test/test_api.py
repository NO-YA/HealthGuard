# backend/tests/test_api.py
import pytest
from backend.app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test que /health retourne 200"""
    response = client.get('/health')
    assert response.status_code == 200
    assert b'healthy' in response.data

def test_predict_endpoint(client):
    """Test que /api/predict existe"""
    response = client.post('/api/predict')
    # Même si 400 (pas d'image), c'est OK pour JOUR 1
    assert response.status_code in [200, 400]