from lotr_sdk import Filter
from lotr_sdk.operations._utils import build_request_url

BASE = "https://the-one-api.dev/v2/movie"


def test_no_params_no_filter():
    assert build_request_url(BASE, {}) == BASE


def test_params_only():
    assert build_request_url(BASE, {"limit": 10, "page": 2}) == f"{BASE}?limit=10&page=2"


def test_filter_only():
    f = Filter().gt("academyAwardWins", 0)
    assert build_request_url(BASE, {}, f) == f"{BASE}?academyAwardWins>0"


def test_params_and_filter():
    f = Filter().gt("academyAwardWins", 0)
    result = build_request_url(BASE, {"limit": 5}, f)
    assert result == f"{BASE}?limit=5&academyAwardWins>0"


def test_empty_filter_ignored():
    assert build_request_url(BASE, {}, Filter()) == BASE


def test_multiple_filter_conditions():
    f = Filter().gt("academyAwardWins", 0).gte("runtimeInMinutes", 160)
    result = build_request_url(BASE, {}, f)
    assert result == f"{BASE}?academyAwardWins>0&runtimeInMinutes>=160"


def test_params_and_multiple_filter_conditions():
    f = Filter().gt("academyAwardWins", 0).lt("budgetInMillions", 100)
    result = build_request_url(BASE, {"limit": 5, "page": 1}, f)
    assert result == f"{BASE}?limit=5&page=1&academyAwardWins>0&budgetInMillions<100"
