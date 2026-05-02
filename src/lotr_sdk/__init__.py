"""lotr-sdk: Python SDK for The One API (the-one-api.dev)."""

from .client import Client
from .config import ClientConfig, LogLevel, RetryStrategy
from .core.filter import Filter
from .errors import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    LOTRSDKError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from .models import ListResponse, Movie, Quote

__version__ = "1.0.0"

__all__ = [
    "APIError",
    "AuthenticationError",
    "Client",
    "ClientConfig",
    "ConfigurationError",
    "Filter",
    "ListResponse",
    "LOTRSDKError",
    "LogLevel",
    "Movie",
    "NetworkError",
    "NotFoundError",
    "Quote",
    "RateLimitError",
    "RetryStrategy",
    "ServerError",
]
