import random
import time

import requests

from ..config import ClientConfig, RetryStrategy


class Transport:
    """Internal HTTP layer used by all SDK operations.

    Responsibilities:
    - Attaches the `Authorization: Bearer` header to every request.
    - Applies timeout from config.
    - Retries failed requests using the configured strategy and jitter.
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

    # TODO add support for standardized errors
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Execute an HTTP request with automatic retries.

        Args:
            method: HTTP verb (e.g. `"GET"`).
            url: Fully-constructed URL including any query string.
            **kwargs: Passed through to `requests.Session.request`.

        Returns:
            The successful `requests.Response`.

        Raises:
            requests.RequestException: After all retry attempts are exhausted.
        """
        kwargs.setdefault("timeout", self._config.timeout_ms / 1000)

        last_exc: Exception | None = None
        for attempt in range(self._config.max_retries + 1):
            try:
                response = self._session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                last_exc = e
                if attempt < self._config.max_retries:
                    time.sleep(self._backoff_delay(attempt))

        raise last_exc

    def _backoff_delay(self, attempt: int) -> float:
        """Seconds to wait before the next retry attempt, including random jitter."""
        jitter = random.uniform(0, self._config.max_jitter_ms / 1000)
        if self._config.retry_strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            return (2 ** attempt) + jitter
        if self._config.retry_strategy == RetryStrategy.LINEAR:
            return (attempt + 1) + jitter
        return 0
