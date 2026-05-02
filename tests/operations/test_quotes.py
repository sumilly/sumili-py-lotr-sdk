import pytest
from models import ListResponse
from models import Quote as QuoteModel
from operations.quotes import Quotes

from .conftest import BASE_URL, LIST_QUOTES_RESPONSE, SINGLE_QUOTE_RESPONSE

QUOTE_ID = "5cd96e05de30eff6ebcce7e9"


@pytest.fixture
def transport(mocker):
    t = mocker.MagicMock()
    t.base_url = BASE_URL
    return t


@pytest.fixture
def quotes(transport):
    return Quotes(transport)


class TestList:
    def test_calls_correct_url(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list()
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/quote", params={})

    def test_returns_list_response(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        result = quotes.list()
        assert isinstance(result, ListResponse)
        assert isinstance(result.docs[0], QuoteModel)

    def test_pagination_params(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(limit=10, page=3)
        _, kwargs = transport.request.call_args
        assert kwargs["params"] == {"limit": 10, "page": 3}

    def test_sort_param(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(sort="character:desc")
        _, kwargs = transport.request.call_args
        assert kwargs["params"]["sort"] == "character:desc"

    def test_none_params_excluded(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(offset=5)
        _, kwargs = transport.request.call_args
        assert "limit" not in kwargs["params"]


class TestGet:
    def test_calls_correct_url(self, quotes, transport):
        transport.request.return_value.json.return_value = SINGLE_QUOTE_RESPONSE
        quotes.get(QUOTE_ID)
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/quote/{QUOTE_ID}")

    def test_returns_quote(self, quotes, transport):
        transport.request.return_value.json.return_value = SINGLE_QUOTE_RESPONSE
        result = quotes.get(QUOTE_ID)
        assert isinstance(result, QuoteModel)
        assert result.id == QUOTE_ID
        assert result.dialog == "Deagol!!"
