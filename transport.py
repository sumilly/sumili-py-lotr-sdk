import random
import time

import requests

from config import ClientConfig, RetryStrategy


class Transport:
    def __init__(self, config: ClientConfig):
        self._config = config
        self._session = requests.Session()
        self._session.headers["Authorization"] = f"Bearer {config.api_key}"

    # TODO add support for standardized errors
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
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
        jitter = random.uniform(0, self._config.max_jitter_ms / 1000)
        if self._config.retry_strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            return (2 ** attempt) + jitter
        if self._config.retry_strategy == RetryStrategy.LINEAR:
            return (attempt + 1) + jitter
        return 0
