from app import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['healthy'] == True

def test_index(client):
    r = client.get('/')
    assert r.status_code == 200

def test_add_todo(client):
    r = client.post('/todos', json={'title': 'Test item'})
    assert r.status_code == 201

def test_get_todos(client):
    r = client.get('/todos')
    assert r.status_code == 200
