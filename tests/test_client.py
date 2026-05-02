import pytest
from lotr_sdk import Client, ClientConfig
from lotr_sdk.operations.movies import Movies
from lotr_sdk.operations.quotes import Quotes


@pytest.fixture
def client():
    return Client(config=ClientConfig(api_key="test-key"))


def test_client_exposes_movies_resource(client):
    assert isinstance(client.movies, Movies)


def test_client_exposes_quotes_resource(client):
    assert isinstance(client.quotes, Quotes)
