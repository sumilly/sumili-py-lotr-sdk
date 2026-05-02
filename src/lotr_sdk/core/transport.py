import random
import time

import requests

from ..config import ClientConfig, RetryStrategy
from ..errors import (
    APIError,
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
)


class Transport:
    """Internal HTTP layer used by all SDK operations.

    Responsibilities:
    - Attaches the `Authorization: Bearer` header to every request.
    - Applies timeout from config.
    - Retries failed requests using the configured strategy and jitter.
    - Maps HTTP errors to typed SDK exceptions.
    - Exposes `base_url` so operations can construct endpoint URLs.

    Not intended for direct use by consumers — access via `Client.movies` / `Client.quotes`.
    """

    def __init__(self, config: ClientConfig):
        self._config = config
        self._session = requests.Session()
        self._session.headers["Authorization"] = f"Bearer {config.api_key}"

    @property
    def base_url(self) -> str:
        return self._config.base_url

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Execute an HTTP request with automatic retries.

        Non-retriable errors (401, 404) are raised immediately.
        Retriable errors (429, 5xx, network) are retried up to `max_retries` times.

        Args:
            method: HTTP verb (e.g. `"GET"`).
            url: Fully-constructed URL including any query string.
            **kwargs: Passed through to `requests.Session.request`.

        Returns:
            The successful `requests.Response`.

        Raises:
            AuthenticationError: On 401 — bad or missing API key.
            NotFoundError: On 404 — resource does not exist.
            RateLimitError: On 429 — after retries exhausted.
            ServerError: On 5xx — after retries exhausted.
            NetworkError: On connection failures or timeouts — after retries exhausted.
        """
        kwargs.setdefault("timeout", self._config.timeout_ms / 1000)

        last_exc: Exception | None = None
        for attempt in range(self._config.max_retries + 1):
            try:
                return self._execute(method, url, **kwargs)
            except (NetworkError, RateLimitError, ServerError) as e:
                last_exc = e
                if attempt < self._config.max_retries:
                    time.sleep(self._backoff_delay(attempt))

        raise last_exc

    def _execute(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make a single HTTP attempt and map errors to SDK exceptions.

        Non-retriable errors are raised directly; retriable errors propagate
        to `request()` which decides whether to retry.
        """
        try:
            response = self._session.request(method, url, **kwargs)
        except requests.Timeout as e:
            raise NetworkError("Request timed out.", cause=e) from e
        except requests.ConnectionError as e:
            raise NetworkError("Connection failed.", cause=e) from e
        except requests.RequestException as e:
            raise NetworkError(str(e), cause=e) from e

        if response.ok:
            return response

        raise self._make_api_error(response)

    def _make_api_error(self, response: requests.Response) -> APIError:
        status = response.status_code
        if status == 401:
            return AuthenticationError("Invalid or missing API key.", status, response)
        if status == 404:
            return NotFoundError("Resource not found.", status, response)
        if status == 429:
            return RateLimitError("Rate limit exceeded. Max 100 requests per 10 minutes.", status, response)
        if status >= 500:
            return ServerError(f"Server error ({status}).", status, response)
        return APIError(f"Unexpected API error ({status}).", status, response)

    def _backoff_delay(self, attempt: int) -> float:
        """Seconds to wait before the next retry attempt, including random jitter."""
        jitter = random.uniform(0, self._config.max_jitter_ms / 1000)
        if self._config.retry_strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            return (2 ** attempt) + jitter
        if self._config.retry_strategy == RetryStrategy.LINEAR:
            return (attempt + 1) + jitter
        return 0
