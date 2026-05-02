import pytest
from lotr_sdk import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    LOTRSDKError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
)


# --- Hierarchy ---

def test_all_errors_inherit_from_base():
    assert issubclass(ConfigurationError, LOTRSDKError)
    assert issubclass(NetworkError, LOTRSDKError)
    assert issubclass(APIError, LOTRSDKError)
    assert issubclass(AuthenticationError, APIError)
    assert issubclass(NotFoundError, APIError)
    assert issubclass(RateLimitError, APIError)
    assert issubclass(ServerError, APIError)


def test_configuration_error_is_also_value_error():
    assert issubclass(ConfigurationError, ValueError)


def test_api_errors_can_be_caught_as_base():
    with pytest.raises(LOTRSDKError):
        raise AuthenticationError("bad key", 401)

    with pytest.raises(APIError):
        raise NotFoundError("not found", 404)


# --- APIError attributes ---

def test_api_error_attributes():
    resp = object()
    err = APIError("something went wrong", 400, resp)
    assert str(err) == "something went wrong"
    assert err.status_code == 400
    assert err.response is resp


def test_api_error_response_defaults_to_none():
    err = APIError("oops", 500)
    assert err.response is None


# --- NetworkError attributes ---

def test_network_error_attributes():
    cause = ConnectionError("refused")
    err = NetworkError("Connection failed.", cause=cause)
    assert str(err) == "Connection failed."
    assert err.cause is cause


def test_network_error_cause_defaults_to_none():
    err = NetworkError("timed out")
    assert err.cause is None
