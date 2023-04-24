import pytest
import app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client

def test_get_system_data(client):
    response = client.get('/get_system_data')
    assert response.status_code == 200
    assert response.is_json

def test_query_gpt4(client):
    response = client.get('/query_gpt4')
    assert response.status_code == 200
    assert response.is_json
