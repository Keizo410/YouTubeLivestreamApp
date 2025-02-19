import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app  # Import the app instance

import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": 'Backend System is Established!'}

def test_subscription_fail(client):
    response = client.post('/api/subscriptions',
                           json={'youtuber':'fake'})
    assert response.status_code==403

#this will fail because of ngrok tunnel 
def test_subscription_success(client):
    response = client.post('/api/subscriptions',
                           json={'youtuber':'@keizokato6333'})
    assert response.status_code==201