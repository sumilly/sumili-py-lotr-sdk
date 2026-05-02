from dataclasses import dataclass, field
from enum import Enum


class RetryStrategy(Enum):
    """Strategy used to space out retry attempts on request failure.

    - EXPONENTIAL_BACKOFF: delay doubles each attempt (2^n seconds)
    - LINEAR: delay increases linearly (n+1 seconds)
    - NONE: retry immediately with no delay
    """

    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR = "linear"
    NONE = "none"


class LogLevel(Enum):
    """Controls verbosity of SDK log output.

    - DEBUG: all internal activity
    - INFO: standard operational messages
    - WARN: recoverable issues
    - ERROR: failures only
    """

    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


@dataclass(frozen=True)
class ClientConfig:
    """Immutable configuration for the SDK client.

    Only `api_key` is required. All other fields have defaults.

    Args:
        api_key: Bearer token from the-one-api.dev. Required.
        base_url: API base URL.
        timeout_ms: Request timeout in milliseconds.
        max_retries: Number of retry attempts on failure.
        retry_strategy: Delay strategy between retries.
        max_jitter_ms: Max random jitter added to retry delays (ms).
        log_level: Minimum log level to emit.
        telemetry: Emit telemetry metrics. Off by default; requires explicit opt-in.
    """

    api_key: str
    base_url: str = "https://the-one-api.dev/v2"
    timeout_ms: int = 30_000
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    max_jitter_ms: int = 500
    log_level: LogLevel = LogLevel.INFO
    telemetry: bool = False
