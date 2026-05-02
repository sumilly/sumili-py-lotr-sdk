import pytest
from core.filter import Filter
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
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie")

    def test_returns_list_response(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        result = movies.list()
        assert isinstance(result, ListResponse)
        assert isinstance(result.docs[0], MovieModel)

    def test_pagination_params(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(limit=5, page=2, offset=10)
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie?limit=5&page=2&offset=10")

    def test_sort_param(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(sort="name:asc")
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie?sort=name%3Aasc")

    def test_none_params_excluded(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(limit=5)
        url = transport.request.call_args[0][1]
        assert "page" not in url
        assert "offset" not in url

    def test_filter_match(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(filter_=Filter().match("name", "The Fellowship of the Ring"))
        url = transport.request.call_args[0][1]
        assert "name=The%20Fellowship%20of%20the%20Ring" in url

    def test_filter_numeric(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(filter_=Filter().gt("academyAwardWins", 0).gte("runtimeInMinutes", 160))
        url = transport.request.call_args[0][1]
        assert "academyAwardWins>0" in url
        assert "runtimeInMinutes>=160" in url

    def test_filter_combined_with_pagination(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_MOVIES_RESPONSE
        movies.list(limit=5, filter_=Filter().gt("academyAwardWins", 0))
        url = transport.request.call_args[0][1]
        assert "limit=5" in url
        assert "academyAwardWins>0" in url


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
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie/{MOVIE_ID}/quote")

    def test_returns_list_response(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        result = movies.list_quotes(MOVIE_ID)
        assert isinstance(result, ListResponse)
        assert isinstance(result.docs[0], QuoteModel)

    def test_pagination_params(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        movies.list_quotes(MOVIE_ID, limit=5, page=2)
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/movie/{MOVIE_ID}/quote?limit=5&page=2")

    def test_none_params_excluded(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        movies.list_quotes(MOVIE_ID, limit=5)
        url = transport.request.call_args[0][1]
        assert "page" not in url

    def test_filter(self, movies, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        movies.list_quotes(MOVIE_ID, filter_=Filter().match("dialog", "You shall not pass"))
        url = transport.request.call_args[0][1]
        assert "dialog=You%20shall%20not%20pass" in url
