import pytest
from lotr_sdk import ClientConfig, ConfigurationError, LogLevel, RetryStrategy


def test_defaults():
    config = ClientConfig(api_key="my-key")

    assert config.api_key == "my-key"
    assert config.base_url == "https://the-one-api.dev/v2"
    assert config.timeout_ms == 30_000
    assert config.max_retries == 3
    assert config.retry_strategy == RetryStrategy.EXPONENTIAL_BACKOFF
    assert config.max_jitter_ms == 500
    assert config.log_level == LogLevel.INFO
    assert config.telemetry is False


def test_overrides():
    config = ClientConfig(
        api_key="my-key",
        base_url="https://custom.api.dev/v2",
        timeout_ms=5_000,
        max_retries=1,
        retry_strategy=RetryStrategy.LINEAR,
        max_jitter_ms=100,
        log_level=LogLevel.DEBUG,
        telemetry=True,
    )

    assert config.base_url == "https://custom.api.dev/v2"
    assert config.timeout_ms == 5_000
    assert config.max_retries == 1
    assert config.retry_strategy == RetryStrategy.LINEAR
    assert config.max_jitter_ms == 100
    assert config.log_level == LogLevel.DEBUG
    assert config.telemetry is True


def test_config_is_immutable():
    config = ClientConfig(api_key="my-key")
    with pytest.raises(Exception):
        config.api_key = "other-key"


# --- API key validation ---

def test_empty_api_key_raises_configuration_error():
    with pytest.raises(ConfigurationError, match="api_key"):
        ClientConfig(api_key="")


def test_whitespace_api_key_raises_configuration_error():
    with pytest.raises(ConfigurationError, match="api_key"):
        ClientConfig(api_key="   ")


def test_configuration_error_is_also_value_error():
    with pytest.raises(ValueError):
        ClientConfig(api_key="")
