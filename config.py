from dataclasses import dataclass, field
from enum import Enum


class RetryStrategy(Enum):
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR = "linear"
    NONE = "none"


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


@dataclass(frozen=True)
class ClientConfig:
    api_key: str
    base_url: str = "https://the-one-api.dev/v2"
    timeout_ms: int = 30_000
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    max_jitter_ms: int = 500
    log_level: LogLevel = LogLevel.INFO
    telemetry: bool = False
