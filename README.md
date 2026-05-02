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
movie = client.movies.get("<movie-id>")
print(movie.name)
print(movie.runtime_in_minutes)
print(movie.academy_award_wins)
```

### List quotes for a movie

Only works for the LotR trilogy.

```python
response = client.movies.list_quotes("<movie-id>")

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
quote = client.quotes.get("<quote-id>")
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

## Filtering

All list methods accept a `filter_` parameter built with the `Filter` class. Conditions are chained and applied together (AND semantics).

```python
from core.filter import Filter
```

### Operators

| Method | Effect | Example |
|--------|--------|---------|
| `match(field, value)` | Field equals value | `Filter().match("name", "Gandalf")` |
| `not_match(field, value)` | Field does not equal value | `Filter().not_match("name", "Frodo")` |
| `include(field, *values)` | Field is one of the values | `Filter().include("race", "Hobbit", "Human")` |
| `exclude(field, *values)` | Field is none of the values | `Filter().exclude("race", "Orc", "Goblin")` |
| `exists(field)` | Field is present | `Filter().exists("name")` |
| `not_exists(field)` | Field is absent | `Filter().not_exists("name")` |
| `regex(field, pattern)` | Field matches regex | `Filter().regex("name", "/foot/i")` |
| `not_regex(field, pattern)` | Field does not match regex | `Filter().not_regex("name", "/foot/i")` |
| `lt(field, value)` | Field less than value | `Filter().lt("budgetInMillions", 100)` |
| `gt(field, value)` | Field greater than value | `Filter().gt("academyAwardWins", 0)` |
| `gte(field, value)` | Field greater than or equal | `Filter().gte("runtimeInMinutes", 160)` |
| `lte(field, value)` | Field less than or equal | `Filter().lte("runtimeInMinutes", 200)` |

### Examples

```python
# Movies with at least one Academy Award win
response = client.movies.list(
    filter_=Filter().gt("academyAwardWins", 0)
)

# Long, award-winning movies
response = client.movies.list(
    filter_=Filter()
    .gt("academyAwardWins", 0)
    .gte("runtimeInMinutes", 160)
)

# Quotes that are not empty
response = client.quotes.list(
    filter_=Filter().exists("dialog").not_match("dialog", "")
)

# Combining filters with pagination and sorting
response = client.movies.list(
    limit=5,
    sort="name:asc",
    filter_=Filter().gt("rottenTomatoesScore", 90),
)
```

## Models

### ID Format

All `id` fields are **MongoDB ObjectIds** — 24-character hex strings. Example format: `507f1f77bcf86cd799439011`.

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
