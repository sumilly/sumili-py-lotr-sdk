import pytest
from models import ListResponse
from models import Movie as MovieModel
from models import Quote as QuoteModel
from operations.movies import Movies

from .conftest import BASE_URL, LIST_MOVIES_RESPONSE, LIST_QUOTES_RESPONSE, SINGLE_MOVIE_RESPONSE

MOVIE_ID = "5cd95395de30eff6ebccde56"


@pytest.fixture
def transport(mocker):
    t = mocker.MagicMock()
    t.base_url = BASE_URL
    return t


@pytest.fixture
def movies(transport):
    return Movies(transport)


class TestList:
    def test_calls_correct_url(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list()
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie", params={})

    def test_returns_list_response(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        result = movies.list()
        assert isinstance(result, ListResponse)
        assert isinstance(result.docs[0], MovieModel)

    def test_pagination_params(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(limit=5, page=2, offset=10)
        _, kwargs = transport.request.call_args
        assert kwargs["params"] == {"limit": 5, "page": 2, "offset": 10}

    def test_sort_param(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(sort="name:asc")
        _, kwargs = transport.request.call_args
        assert kwargs["params"]["sort"] == "name:asc"

    def test_none_params_excluded(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(limit=5)
        _, kwargs = transport.request.call_args
        assert "page" not in kwargs["params"]


class TestGet:
    def test_calls_correct_url(self, movies, transport):
        transport.request.return_value.json.return_value = SINGLE_MOVIE_RESPONSE
        movies.get(MOVIE_ID)
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie/{MOVIE_ID}")

    def test_returns_movie(self, movies, transport):
        transport.request.return_value.json.return_value = SINGLE_MOVIE_RESPONSE
        result = movies.get(MOVIE_ID)
        assert isinstance(result, MovieModel)
        assert result.id == MOVIE_ID


class TestListQuotes:
    def test_calls_correct_url(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        movies.list_quotes(MOVIE_ID)
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie/{MOVIE_ID}/quote", params={})

    def test_returns_list_response(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        result = movies.list_quotes(MOVIE_ID)
        assert isinstance(result, ListResponse)
        assert isinstance(result.docs[0], QuoteModel)

    def test_pagination_params(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        movies.list_quotes(MOVIE_ID, limit=5, page=2)
        _, kwargs = transport.request.call_args
        assert kwargs["params"] == {"limit": 5, "page": 2}

    def test_none_params_excluded(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        movies.list_quotes(MOVIE_ID, limit=5)
        _, kwargs = transport.request.call_args
        assert "page" not in kwargs["params"]
