import pytest 
from utilities.websub import WebSub
from unittest.mock import patch, MagicMock
import os 

@patch("requests.get")
def test_get_ngrock_url_success(mock_get):
    """Test get ngrock url function - success"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "tunnels": [
            {"proto":"https", "public_url": "https://mocked-ngrok-url.com"}
        ]
    }

    mock_get.return_value = mock_response

    websub = WebSub()
    result = websub.get_grok_url()

    assert result == "https://mocked-ngrok-url.com/youtube-callback"

@patch("requests.post")
@patch("requests.get")
def test_subscribe_to_channel_success(mock_get, mock_post):
    """Test subscribe to a chennel function - success"""
    mock_get_response = MagicMock()
    mock_get_response.json.return_value = {
        "tunnels": [{"proto": "https", "public_url": "https://mock-ngrok.com"}]
    }
    mock_get.return_value = mock_get_response

    mock_post_response = MagicMock()
    mock_post_response.status_code = 202
    mock_post.return_value = mock_post_response

    websub =WebSub()
    response_code = websub.subscribe_to_channel("UC123")

    assert response_code == 201
