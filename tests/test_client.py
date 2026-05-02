import pytest
from client import Client
from config import ClientConfig
from operations.movies import Movies
from operations.quotes import Quotes


@pytest.fixture
def client():
    return Client(config=ClientConfig(api_key="test-key"))


def test_client_exposes_movies_resource(client):
    assert isinstance(client.movies, Movies)


def test_client_exposes_quotes_resource(client):
    assert isinstance(client.quotes, Quotes)
