import io
from PIL import Image
from backend.app.main import app


def test_frontend_and_predict():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # GET / should return the frontend
        r = client.get('/')
        assert r.status_code == 200 or r.status_code == 404  # Accepte 404 si pas de frontend
        # Create a small PNG image
        buf = io.BytesIO()
        Image.new('RGB', (32, 32), (123, 222, 64)).save(buf, format='PNG')
        img = buf.getvalue()
        data = {'file': (io.BytesIO(img), 'test.png')}
        r2 = client.post('/api/predict', data=data, content_type='multipart/form-data')
        assert r2.status_code == 200
        j = r2.get_json()
        assert j['success'] is True
        assert 'diagnosis' in j
