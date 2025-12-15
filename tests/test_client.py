import pytest
from orangic import Orangic, AuthenticationError

def test_client_initialization():
    client = Orangic(api_key="test-key")
    assert client.api_key == "test-key"
    assert client.base_url == "https://api.orangic.tech"

def test_missing_api_key():
    with pytest.raises(AuthenticationError):
        Orangic()  # Should raise if no API key in env