import pytest
from lotr_sdk import Filter, ListResponse, Quote as QuoteModel
from lotr_sdk.operations.quotes import Quotes

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
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/quote")

    def test_returns_list_response(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        result = quotes.list()
        assert isinstance(result, ListResponse)
        assert isinstance(result.docs[0], QuoteModel)

    def test_pagination_params(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(limit=10, page=3)
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/quote?limit=10&page=3")

    def test_sort_param(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(sort="character:desc")
        transport.request.assert_called_once_with("GET", f"{BASE_URL}/quote?sort=character%3Adesc")

    def test_none_params_excluded(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(offset=5)
        url = transport.request.call_args[0][1]
        assert "limit" not in url
        assert "page" not in url

    def test_filter_not_match(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(filter_=Filter().not_match("dialog", "Deagol"))
        url = transport.request.call_args[0][1]
        assert "dialog!=Deagol" in url

    def test_filter_chained(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(filter_=Filter().exists("dialog").not_match("dialog", ""))
        url = transport.request.call_args[0][1]
        assert "dialog" in url

    def test_filter_combined_with_pagination(self, quotes, transport):
        transport.request.return_value.json.return_value = LIST_QUOTES_RESPONSE
        quotes.list(limit=10, filter_=Filter().not_match("dialog", "Deagol"))
        url = transport.request.call_args[0][1]
        assert "limit=10" in url
        assert "dialog!=Deagol" in url


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
