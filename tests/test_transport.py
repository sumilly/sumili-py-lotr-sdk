import pytest
import requests

from lotr_sdk import AuthenticationError, ClientConfig, NetworkError, NotFoundError, RateLimitError, RetryStrategy, ServerError
from lotr_sdk.core.transport import Transport


BASE_URL = "https://the-one-api.dev/v2/movie"


@pytest.fixture
def transport():
    return Transport(ClientConfig(api_key="test-key"))


def _ok_response(mocker):
    resp = mocker.MagicMock()
    resp.ok = True
    return resp


def _error_response(mocker, status_code: int):
    resp = mocker.MagicMock()
    resp.ok = False
    resp.status_code = status_code
    return resp


# --- Auth & config ---

def test_auth_header(transport):
    assert transport._session.headers["Authorization"] == "Bearer test-key"


def test_timeout_applied(transport, mocker):
    mock_resp = _ok_response(mocker)
    mock_call = mocker.patch.object(transport._session, "request", return_value=mock_resp)
    transport.request("GET", BASE_URL)
    _, kwargs = mock_call.call_args
    assert kwargs["timeout"] == 30.0


def test_returns_response(transport, mocker):
    mock_resp = _ok_response(mocker)
    mocker.patch.object(transport._session, "request", return_value=mock_resp)
    assert transport.request("GET", BASE_URL) is mock_resp


# --- HTTP error mapping ---

def test_401_raises_authentication_error(transport, mocker):
    mocker.patch.object(transport._session, "request", return_value=_error_response(mocker, 401))
    with pytest.raises(AuthenticationError) as exc:
        transport.request("GET", BASE_URL)
    assert exc.value.status_code == 401


def test_404_raises_not_found_error(transport, mocker):
    mocker.patch.object(transport._session, "request", return_value=_error_response(mocker, 404))
    with pytest.raises(NotFoundError) as exc:
        transport.request("GET", BASE_URL)
    assert exc.value.status_code == 404


def test_429_raises_rate_limit_error(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=0))
    mocker.patch.object(t._session, "request", return_value=_error_response(mocker, 429))
    with pytest.raises(RateLimitError) as exc:
        t.request("GET", BASE_URL)
    assert exc.value.status_code == 429


def test_500_raises_server_error(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=0))
    mocker.patch.object(t._session, "request", return_value=_error_response(mocker, 500))
    with pytest.raises(ServerError) as exc:
        t.request("GET", BASE_URL)
    assert exc.value.status_code == 500


def test_timeout_raises_network_error(transport, mocker):
    mocker.patch.object(transport._session, "request", side_effect=requests.Timeout)
    mocker.patch("lotr_sdk.core.transport.time.sleep")
    with pytest.raises(NetworkError, match="timed out"):
        transport.request("GET", BASE_URL)


def test_connection_error_raises_network_error(transport, mocker):
    mocker.patch.object(transport._session, "request", side_effect=requests.ConnectionError)
    mocker.patch("lotr_sdk.core.transport.time.sleep")
    with pytest.raises(NetworkError, match="Connection failed"):
        transport.request("GET", BASE_URL)


# --- Retry behaviour ---

def test_401_and_404_are_not_retried(mocker):
    for status in (401, 404):
        t = Transport(ClientConfig(api_key="test-key", max_retries=3))
        mock_req = mocker.patch.object(t._session, "request", return_value=_error_response(mocker, status))
        with pytest.raises(Exception):
            t.request("GET", BASE_URL)
        assert mock_req.call_count == 1  # no retry


def test_429_is_retried(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2))
    mock_req = mocker.patch.object(t._session, "request", return_value=_error_response(mocker, 429))
    mocker.patch("lotr_sdk.core.transport.time.sleep")
    with pytest.raises(RateLimitError):
        t.request("GET", BASE_URL)
    assert mock_req.call_count == 3  # 1 initial + 2 retries


def test_5xx_is_retried(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2))
    mock_req = mocker.patch.object(t._session, "request", return_value=_error_response(mocker, 500))
    mocker.patch("lotr_sdk.core.transport.time.sleep")
    with pytest.raises(ServerError):
        t.request("GET", BASE_URL)
    assert mock_req.call_count == 3


def test_retries_on_network_error_then_succeeds(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2))
    mock_resp = _ok_response(mocker)
    mocker.patch.object(t._session, "request", side_effect=[
        requests.ConnectionError,
        requests.ConnectionError,
        mock_resp,
    ])
    mocker.patch("lotr_sdk.core.transport.time.sleep")
    assert t.request("GET", BASE_URL) is mock_resp


def test_raises_network_error_after_max_retries(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2))
    mocker.patch.object(t._session, "request", side_effect=requests.Timeout)
    mocker.patch("lotr_sdk.core.transport.time.sleep")
    with pytest.raises(NetworkError):
        t.request("GET", BASE_URL)


def test_retry_count_matches_max_retries(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=3))
    mock_req = mocker.patch.object(t._session, "request", side_effect=requests.Timeout)
    mocker.patch("lotr_sdk.core.transport.time.sleep")
    with pytest.raises(NetworkError):
        t.request("GET", BASE_URL)
    assert mock_req.call_count == 4  # 1 initial + 3 retries


def test_no_retry_on_success(transport, mocker):
    mock_resp = _ok_response(mocker)
    mock_req = mocker.patch.object(transport._session, "request", return_value=mock_resp)
    transport.request("GET", BASE_URL)
    assert mock_req.call_count == 1


def test_sleep_called_between_retries(mocker):
    t = Transport(ClientConfig(api_key="test-key", max_retries=2, retry_strategy=RetryStrategy.NONE, max_jitter_ms=0))
    mocker.patch.object(t._session, "request", side_effect=requests.Timeout)
    mock_sleep = mocker.patch("lotr_sdk.core.transport.time.sleep")
    with pytest.raises(NetworkError):
        t.request("GET", BASE_URL)
    assert mock_sleep.call_count == 2


# --- Backoff strategies ---

def test_exponential_backoff_delay():
    t = Transport(ClientConfig(api_key="k", retry_strategy=RetryStrategy.EXPONENTIAL_BACKOFF, max_jitter_ms=0))
    assert t._backoff_delay(0) == 1.0
    assert t._backoff_delay(1) == 2.0
    assert t._backoff_delay(2) == 4.0


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
        assert 1.0 <= delay <= 1.5
