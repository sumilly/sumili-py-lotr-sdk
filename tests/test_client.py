import pytest
from client import Client


@pytest.fixture
def client():
    return Client(api_key="test-key")


def test_list_movies(client):
    raise NotImplementedError


def test_get_movie(client):
    raise NotImplementedError


def test_list_movie_quotes(client):
    raise NotImplementedError


def test_list_all_movie_quotes(client):
    raise NotImplementedError


def test_get_quote(client):
    raise NotImplementedError
