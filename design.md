# LOTR SDK design

LOTR SDK is a synchronous python SDK for [The One API](https://the-one-api.dev/).

## Functional requirements

- The SDK shall support APIs in the [The One API](https://the-one-api.dev/)
- Authentication is through API keys that consumers sign up for. The SDK shall not provide a default API key for demo purposes.
- The SDK may not reflect the API 1-1. The SDK shall provide abstractions that are idiomatic and intuitive for consumers regardless of the underlying API structure.
- The SDK and its supported APIs shall evolve as independent entities. The SDK documentation shall explicitly state which API versions are supported.

## Non-functional requirements

- Reliability
  - The SDK shall have provisions to handle errors. This includes mechanisms like retries, backoffs, jitter, timeouts. These shall be configurable based on consumers' preferences but they shall have defaults to start to avoid adverse behavior with explicit configuration.

- Consistency
  - The SDK shall use consistent, predictable interfaces and conventions for methods, parameters and errors.

- Usability
  - The SDK shall prefer simplicity of usgae for consumers over other factors.
  - The SDK shall have self-documenting methods and params with consistent conventions.
  - The SDK shall have explicit documentation including functionality, params and example usages. It shall be kept up-to-date as future iterations are released
  - The SDK shall warn consumers when functionality is planned to be deprecated in future iterations. It shall be explicit on the last supported version and alternatives consumers should be migrating to, when available.
  - The SDK shall not introduce backward-incompatible changes without prior deprecation warnings to consumers.
  - The SDK shall clearly communicate that its operations are synchronous and blocking to avoid adverse consumer behaviors.

- Performance
  - The SDK shall not encourage patterns beyond what the API supports. When such patterns are necessary, the SDK shall be transparent about performance implications like N+1 queries and over-fetching.
  - The SDK shall reduce unnecessary API calls by limiting infinite pagination and not fetching future content unless consumers need it.

- Security & Privacy
  - The SDK shall not record consumer credentials or sensitive information to logs or local storage. Even when explicitly requested by consumers, such information shall be redacted.
  - The SDK shall be secure by default respecting TLS and other protocols without consumer configuration.

- Observability
  - The SDK shall not silently consume errors unless for operations like internal retries.
  - The SDK shall provide consumers with ways to inspect and log underlying behaviors of the SDK, if they desire.
  - The SDK shall emit telemetry metrics non-invasively and only when consented by consumers explicitly by enabling telemetry.

- Configurability
  - The SDK shall not assume consumers' access patterns or execution environment. It shall provide configurability for consumers to change parameters.
  - Beyond global Client configuration, the SDK shall provide per-method configuration overrides for consumers with more granular needs.

- Quality
  - All SDK behaviors and methods shall be thoroughly covered by unit and integration tests.

## Out of scope

- Idempotency
  - Since LOTR APIs are read only, no idempotency is required.

- Asynchronous behaviors
  - This SDK only supports synchronous and blocking behaviors. Asynchronous behaviors shall be provided in a separate library with similar methods and models.

## Design

Refer to domain.md for documentation on APIs.

### Models

All list endpoints return a paginated envelope. The `docs` field contains the items.

**ListResponse**

| Field    | Type      | Description                        |
| -------- | --------- | ---------------------------------- |
| `docs`   | `list[T]` | The result items                   |
| `total`  | `int`     | Total number of matching documents |
| `limit`  | `int`     | Max results per page               |
| `offset` | `int`     | Number of results skipped          |
| `page`   | `int`     | Current page number                |
| `pages`  | `int`     | Total number of pages              |

**Movie**

| Field                            | Type    | Description                         |
| -------------------------------- | ------- | ----------------------------------- |
| `id`                             | `str`   | Unique identifier (`_id` from API)  |
| `name`                           | `str`   | Movie title                         |
| `runtime_in_minutes`             | `int`   | Total runtime in minutes            |
| `budget_in_millions`             | `float` | Production budget in millions USD   |
| `box_office_revenue_in_millions` | `float` | Box office revenue in millions USD  |
| `academy_award_nominations`      | `int`   | Number of Academy Award nominations |
| `academy_award_wins`             | `int`   | Number of Academy Award wins        |
| `rotten_tomatoes_score`          | `float` | Rotten Tomatoes score (0–100)       |

**Quote**

| Field          | Type  | Description                             |
| -------------- | ----- | --------------------------------------- |
| `id`           | `str` | Unique identifier (`_id` from API)      |
| `dialog`       | `str` | The spoken quote text                   |
| `movie_id`     | `str` | ID of the movie the quote is from       |
| `character_id` | `str` | ID of the character who spoke the quote |

### Filtering

Filtering is done via a `Filter` builder class. Each method appends a condition and returns `self`, allowing chaining. Call `.build()` at the end to produce the query parameter dict to pass to a request.

```python
class Filter:
    def match(self, field: str, value: str) -> "Filter": ...
    def not_match(self, field: str, value: str) -> "Filter": ...
    def include(self, field: str, *values: str) -> "Filter": ...
    def exclude(self, field: str, *values: str) -> "Filter": ...
    def exists(self, field: str) -> "Filter": ...
    def not_exists(self, field: str) -> "Filter": ...
    def regex(self, field: str, pattern: str) -> "Filter": ...
    def not_regex(self, field: str, pattern: str) -> "Filter": ...
    def lt(self, field: str, value: float) -> "Filter": ...
    def gt(self, field: str, value: float) -> "Filter": ...
    def gte(self, field: str, value: float) -> "Filter": ...
    def lte(self, field: str, value: float) -> "Filter": ...
    def build(self) -> dict[str, str]: ...
```

Each method maps to an API filtering operator:

| Method       | API operator            | Example                                       |
| ------------ | ----------------------- | --------------------------------------------- |
| `match`      | `field=value`           | `Filter().match("name", "Gandalf")`           |
| `not_match`  | `field!=value`          | `Filter().not_match("name", "Frodo")`         |
| `include`    | `field=v1,v2`           | `Filter().include("race", "Hobbit", "Human")` |
| `exclude`    | `field!=v1,v2`          | `Filter().exclude("race", "Orc", "Goblin")`   |
| `exists`     | `field`                 | `Filter().exists("name")`                     |
| `not_exists` | `!field`                | `Filter().not_exists("name")`                 |
| `regex`      | `field=/pattern/flags`  | `Filter().regex("name", "/foot/i")`           |
| `not_regex`  | `field!=/pattern/flags` | `Filter().not_regex("name", "/foot/i")`       |
| `lt`         | `field<value`           | `Filter().lt("budgetInMillions", 100)`        |
| `gt`         | `field>value`           | `Filter().gt("academyAwardWins", 0)`          |
| `gte`        | `field>=value`          | `Filter().gte("runtimeInMinutes", 160)`       |
| `lte`        | `field<=value`          | `Filter().lte("runtimeInMinutes", 200)`       |

**Example usage**

```python
f = (
    Filter()
    .gt("academyAwardWins", 0)
    .gte("runtimeInMinutes", 160)
    .build()
)

client.list_movies(filter=f)
```

Multiple conditions are combined as independent query parameters (AND semantics, matching the API's behaviour).
