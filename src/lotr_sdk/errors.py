"""SDK error hierarchy.

All exceptions raised by the SDK inherit from `LOTRSDKError`, so consumers
can catch the base class or any specific subclass.

Hierarchy:
    LOTRSDKError
    ├── ConfigurationError   — invalid SDK configuration
    ├── NetworkError         — connection failures, timeouts
    └── APIError             — API returned an HTTP error
        ├── AuthenticationError  (401)
        ├── NotFoundError        (404)
        ├── RateLimitError       (429)
        └── ServerError          (5xx)
"""


class LOTRSDKError(Exception):
    """Base class for all SDK exceptions."""


class ConfigurationError(LOTRSDKError, ValueError):
    """Raised for invalid SDK configuration (e.g. empty API key)."""


class NetworkError(LOTRSDKError):
    """Raised on connection failures, timeouts, and other transport-level issues.

    Attributes:
        cause: The underlying exception that triggered this error.
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class APIError(LOTRSDKError):
    """Raised when the API returns an HTTP error response.

    Attributes:
        status_code: HTTP status code returned by the API.
        response: The raw `requests.Response` object.
    """

    def __init__(self, message: str, status_code: int, response=None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(APIError):
    """401 — Invalid or missing API key."""


class NotFoundError(APIError):
    """404 — The requested resource does not exist."""


class RateLimitError(APIError):
    """429 — Rate limit exceeded. Max 100 requests per 10 minutes."""


class ServerError(APIError):
    """5xx — The API returned a server-side error."""
