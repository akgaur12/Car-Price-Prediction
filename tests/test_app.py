import pytest
from app import app, model_manager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Flask-Talisman redirects to HTTPS by default.
        # We tell the client to follow redirects.
        client.environ_base['HTTP_X_FORWARDED_PROTO'] = 'https'
        yield client

def test_index_page(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Car Price Prediction" in response.data

def test_predict_missing_data(client):
    """Test prediction with missing data returns 400."""
    response = client.post('/predict', data={})
    assert response.status_code == 400
    assert b"Missing input data" in response.data

def test_predict_valid_data(client):
    """Test prediction with valid data (mocking or using actual model)."""
    # Note: This depends on the actual model and dataset being present.
    # In a real CI environment, you might mock the model_manager.predict.
    data = {
        'company': 'Hyundai',
        'model': 'Hyundai Santro Xing',
        'year': '2007',
        'fuel_type': 'Petrol',
        'kms': '45000'
    }
    response = client.post('/predict', data=data)
    assert response.status_code == 200
    # The output should be a numeric string
    try:
        float(response.data.decode('utf-8'))
        assert True
    except ValueError:
        pytest.fail("Prediction output is not a number")

def test_404(client):
    """Test 404 handler."""
    response = client.get('/non-existent-page')
    assert response.status_code == 404
    assert b"Page not found" in response.data
