# LOTR SDK design

LOTR SDK is a python SDK for [The One API](https://the-one-api.dev/).

This client supports all operations as synchronous only.

## Tenets

- Prefer simplicity of usage for consumers
- Prefer configurability of client for flexibility of consumer usage
- All methods shall be intuitive and self-documenting but explicit documentation and examples shall also be included
- SDK may not reflect 1-1 with API
- SDK and APIs shall evolve as individual entities. Documentation shall dictate what API versions are supported by the SDK shall support
- SDK shall not be backward incompatible when
- Deprecation shall be warned to consumer prior to removal from future SDK versions
- All methods shall have standard and visible interfaces and outputs for consumers.
- SDK shall clearly state if it's API are synchronous / blocking to avoid adverse behavior for consumers
- SDK shall strive to be performant, avoiding unnecessary background API calls.
- SDK shall strive to self-handle errors through retries prior to bubbling up the error
- All behaviors methods shall be thoroughly unit and integration tested
- [P1] Beyond global Client configurations, SDK shall provide per method configurations

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
