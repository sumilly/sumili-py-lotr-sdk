import pytest
import requests

from config import ClientConfig, RetryStrategy
from core.transport import Transport


BASE_URL = "https://the-one-api.dev/v2/movie"


@pytest.fixture
def transport():
    return Transport(ClientConfig(api_key="test-key"))


def _mock_response(mocker, transport, *, side_effect=None, status_code=200):
    mock_resp = mocker.MagicMock()
    mock_resp.status_code = status_code
    mock_resp.raise_for_status.return_value = None
    if side_effect:
        mocker.patch.object(transport._session, "request", side_effect=side_effect)
    else:
        mocker.patch.object(transport._session, "request", return_value=mock_resp)
    return mock_resp


# --- Auth & config ---

def test_auth_header(transport):
    assert transport._session.headers["Authorization"] == "Bearer test-key"


def test_timeout_applied(transport, mocker):
    mock_req = _mock_response(mocker, transport)
    mock_call = mocker.patch.object(transport._session, "request", return_value=mock_req)
    transport.request("GET", BASE_URL)
    _, kwargs = mock_call.call_args
    assert kwargs["timeout"] == 30.0


def test_returns_response(transport, mocker):
    mock_resp = _mock_response(mocker, transport)
    result = transport.request("GET", BASE_URL)
    assert result is mock_resp


# --- Retries ---

def test_retries_on_failure_then_succeeds(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2))
    mock_resp = mocker.MagicMock()
    mock_resp.raise_for_status.return_value = None
    mocker.patch.object(t._session, "request", side_effect=[
        requests.RequestException("fail"),
        requests.RequestException("fail"),
        mock_resp,
    ])
    mocker.patch("core.transport.time.sleep")

    result = t.request("GET", BASE_URL)
    assert result is mock_resp


def test_raises_after_max_retries_exhausted(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2))
    mocker.patch.object(t._session, "request", side_effect=requests.RequestException("fail"))
    mocker.patch("core.transport.time.sleep")

    with pytest.raises(requests.RequestException):
        t.request("GET", BASE_URL)


def test_retry_count_matches_max_retries(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=3))
    mock_req = mocker.patch.object(t._session, "request", side_effect=requests.RequestException("fail"))
    mocker.patch("core.transport.time.sleep")

    with pytest.raises(requests.RequestException):
        t.request("GET", BASE_URL)

    assert mock_req.call_count == 4  # 1 initial + 3 retries


def test_no_retry_on_success(transport, mocker):
    mock_resp = _mock_response(mocker, transport)
    mock_req = mocker.patch.object(transport._session, "request", return_value=mock_resp)
    transport.request("GET", BASE_URL)
    assert mock_req.call_count == 1


# --- Backoff strategies ---

def test_exponential_backoff_delay():
    t = Transport(ClientConfig(api_key="k", retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF, max_jitter_ms=0))
    assert t._backoff_delay(0) == 1.0   # 2^0
    assert t._backoff_delay(1) == 2.0   # 2^1
    assert t._backoff_delay(2) == 4.0   # 2^2


def test_linear_backoff_delay():
    t = Transport(ClientConfig(api_key="k", retry_strategy=RetryStrategy.LINEAR, max_jitter_ms=0))
    assert t._backoff_delay(0) == 1.0
    assert t._backoff_delay(1) == 2.0
    assert t._backoff_delay(2) == 3.0


def test_none_strategy_no_delay():
    t = Transport(ClientConfig(api_key="k", retry_strategy=RetryStrategy.NONE, max_jitter_ms=0))
    assert t._backoff_delay(0) == 0
    assert t._backoff_delay(1) == 0


def test_jitter_within_bounds():
    t = Transport(ClientConfig(api_key="k", retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF, max_jitter_ms=500))
    for _ in range(50):
        delay = t._backoff_delay(0)
        assert 1.0 <= delay <= 1.5  # 2^0=1, jitter up to 0.5s


def test_sleep_called_between_retries(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2, retry_strategy=RetryStrategy.NONE, max_jitter_ms=0))
    mocker.patch.object(t._session, "request", side_effect=requests.RequestException("fail"))
    mock_sleep = mocker.patch("core.transport.time.sleep")

    with pytest.raises(requests.RequestException):
        t.request("GET", BASE_URL)

    assert mock_sleep.call_count == 2  # sleeps between attempt 0→1 and 1→2, not after last
