import io
import pytest
from backend.app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'healthy'


def test_predict_valid_image(client):
    data = {'file': (io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00'*100), 'test.png')}
    r = client.post('/api/predict', data=data, content_type='multipart/form-data')
    assert r.status_code == 200
    json = r.get_json()
    assert json['success'] is True
    assert 'diagnosis' in json


def test_predict_invalid_format(client):
    data = {'file': (io.BytesIO(b'notanimage'), 'test.txt')}
    r = client.post('/api/predict', data=data, content_type='multipart/form-data')
    assert r.status_code == 400


def test_predict_oversized_image(client):
    big = b'\xff' * (2 * 1024 * 1024 + 1)
    data = {'file': (io.BytesIO(big), 'big.jpg')}
    r = client.post('/api/predict', data=data, content_type='multipart/form-data')
    assert r.status_code == 413


def test_results_endpoint(client):
    data = {'file': (io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00'*100), 'test.png')}
    client.post('/api/predict', data=data, content_type='multipart/form-data')
    r = client.get('/api/results')
    assert r.status_code == 200
    json = r.get_json()
    assert json['count'] >= 1
    assert isinstance(json['results'], list)
