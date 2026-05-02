# sumili-sdk

A Python SDK for [The One API](https://the-one-api.dev/) — the Lord of the Rings API.

## Requirements

- Python 3.10+
- An API key from [the-one-api.dev](https://the-one-api.dev/)

## Installation

```bash
pip install requests
```

## Quick start

```python
from client import Client
from config import ClientConfig

client = Client(config=ClientConfig(api_key="your-api-key"))
```

## Configuration

`ClientConfig` accepts the following options. Only `api_key` is required.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `api_key` | `str` | — | Your API key |
| `base_url` | `str` | `https://the-one-api.dev/v2` | API base URL |
| `timeout_ms` | `int` | `30000` | Request timeout in milliseconds |
| `max_retries` | `int` | `3` | Number of retries on failure |
| `retry_strategy` | `RetryStrategy` | `EXPONENTIAL_BACKOFF` | `EXPONENTIAL_BACKOFF`, `LINEAR`, or `NONE` |
| `max_jitter_ms` | `int` | `500` | Max random jitter added to retry delays |
| `log_level` | `LogLevel` | `INFO` | `DEBUG`, `INFO`, `WARN`, or `ERROR` |
| `telemetry` | `bool` | `False` | Enable telemetry |

```python
from config import ClientConfig, LogLevel, RetryStrategy

config = ClientConfig(
    api_key="your-api-key",
    timeout_ms=5_000,
    max_retries=2,
    retry_strategy=RetryStrategy.LINEAR,
    log_level=LogLevel.DEBUG,
)

client = Client(config=config)
```

## Movies

### List all movies

```python
response = client.movies.list()

for movie in response.docs:
    print(movie.name, movie.rotten_tomatoes_score)
```

### Get a movie by ID

```python
movie = client.movies.get("5cd95395de30eff6ebccde56")
print(movie.name)
print(movie.runtime_in_minutes)
print(movie.academy_award_wins)
```

### List quotes for a movie

Only works for the LotR trilogy.

```python
response = client.movies.list_quotes("5cd95395de30eff6ebccde56")

for quote in response.docs:
    print(quote.dialog)
```

## Quotes

### List all quotes

```python
response = client.quotes.list()

for quote in response.docs:
    print(quote.dialog)
```

### Get a quote by ID

```python
quote = client.quotes.get("5cd96e05de30eff6ebcce7e9")
print(quote.dialog)
```

## Pagination

All list methods accept `limit`, `page`, and `offset` parameters.

```python
# First page of 10 results
response = client.movies.list(limit=10, page=1)

# Skip the first 20 results
response = client.quotes.list(limit=10, offset=20)

# Navigate pages using response metadata
print(response.page)   # current page
print(response.pages)  # total pages
print(response.total)  # total matching documents
```

## Sorting

All list methods accept a `sort` parameter in the format `field:asc` or `field:desc`.

```python
response = client.movies.list(sort="name:asc")
response = client.quotes.list(sort="character:desc")
```

## Models

### Movie

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique identifier |
| `name` | `str` | Movie title |
| `runtime_in_minutes` | `int` | Total runtime |
| `budget_in_millions` | `float` | Production budget (USD millions) |
| `box_office_revenue_in_millions` | `float` | Box office revenue (USD millions) |
| `academy_award_nominations` | `int` | Number of nominations |
| `academy_award_wins` | `int` | Number of wins |
| `rotten_tomatoes_score` | `float` | Rotten Tomatoes score (0–100) |

### Quote

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique identifier |
| `dialog` | `str` | The spoken quote |
| `movie_id` | `str` | ID of the movie |
| `character_id` | `str` | ID of the character |

### ListResponse[T]

Returned by all list methods.

| Field | Type | Description |
|-------|------|-------------|
| `docs` | `list[T]` | The result items |
| `total` | `int` | Total matching documents |
| `limit` | `int` | Max results per page |
| `offset` | `int` | Number of results skipped |
| `page` | `int` | Current page |
| `pages` | `int` | Total pages |
