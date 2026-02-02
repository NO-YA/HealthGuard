from app.ml_service import MLService
import os

def test_ml_service_loads():
    ml = MLService()
    assert ml.diabetes_loader is not None
    assert ml.anemia_loader is not None
    assert ml.deficiency_loader is not None

def test_predict_returns_dict():
    ml = MLService()
    # Use a test image
    test_image = 'path/to/test/image.jpg'
    if os.path.exists(test_image):
        results = ml.predict_all(test_image)
        assert 'diabetes' in results
        assert 'anemia' in results
        assert 'deficiency' in results