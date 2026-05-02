# LOTR API

### Base URL

https://the-one-api.dev/v2

### Authentication

via API Keys

All routes except `/book` and `/book/{id}` require authentication. Send the access key as a bearer token in the `Authorization` header:

```
Authorization: Bearer your-api-key-123
```

Rate limit: 100 requests per 10 minutes per authenticated user.

### Response Format

JSON for all endpoints.

### Supported APIs

1. GET /movie
   List of all movies, including the "The Lord of the Rings" and the "The Hobbit" trilogies
   Needs api key: yes

JSON response:

```
{
  "docs": [
    {
      "_id": "5cd95395de30eff6ebccde56",
      "name": "The Lord of the Rings Series",
      "runtimeInMinutes": 558,
      "budgetInMillions": 281,
      "boxOfficeRevenueInMillions": 2917,
      "academyAwardNominations": 30,
      "academyAwardWins": 17,
      "rottenTomatoesScore": 94
    },
    ...
  ],
  "total": 8,
  "limit": 1000,
  "offset": 0,
  "page": 1,
  "pages": 1
}
```

2. GET /movie/{id}
   Request one specific movie
   Needs api key: yes

JSON Response:

```
{
  "docs": [
    {
      "_id": "5cd95395de30eff6ebccde56",
      "name": "The Lord of the Rings Series",
      "runtimeInMinutes": 558,
      "budgetInMillions": 281,
      "boxOfficeRevenueInMillions": 2917,
      "academyAwardNominations": 30,
      "academyAwardWins": 17,
      "rottenTomatoesScore": 94
    }
  ],
  "total": 1,
  "limit": 1000,
  "offset": 0,
  "page": 1,
  "pages": 1
}
```

3. /movie/{id}/quote
   Request all movie quotes for one specific movie (only working for the LotR trilogy)
   Needs api key: yes

JSON response

```
{
  "docs": [
    {
      "_id": "5cd96e05de30eff6ebcce7e9",
      "dialog": "Deagol!!",
      "movie": "5cd95395de30eff6ebccde5d",
      "character": "5cd99d4bde30eff6ebccfe9e",
      "id": "5cd96e05de30eff6ebcce7e9"
    },
    ...
  ],
  "total": 872,
  "limit": 1000,
  "offset": 0,
  "page": 1,
  "pages": 1
}
```

4. /quote
   List of all movie quotes
   Needs api key: yes

JSON response

```
{
  "docs": [
    {
      "_id": "5cd96e05de30eff6ebcce7e9",
      "dialog": "Deagol!!",
      "movie": "5cd95395de30eff6ebccde5d",
      "character": "5cd99d4bde30eff6ebccfe9e",
      "id": "5cd96e05de30eff6ebcce7e9"
    },
    ...
  ],
  "total": 2383,
  "limit": 10,
  "offset": 0,
  "page": 1,
  "pages": 239
}
```

5. /quote/{id}
   Request one specific movie quote
   Needs api key: yes

JSON response

```
{
  "docs": [
    {
      "_id": "5cd96e05de30eff6ebcce7e9",
      "dialog": "Deagol!!",
      "movie": "5cd95395de30eff6ebccde5d",
      "character": "5cd99d4bde30eff6ebccfe9e",
      "id": "5cd96e05de30eff6ebcce7e9"
    }
  ],
  "total": 1,
  "limit": 1000,
  "offset": 0,
  "page": 1,
  "pages": 1
}
```

### Pagination

All list endpoints support pagination via query parameters.

| Option   | Example                | Notes                                |
| -------- | ---------------------- | ------------------------------------ |
| `limit`  | `/character?limit=100` | Number of results per page           |
| `page`   | `/character?page=2`    | Page number (default limit is 10)    |
| `offset` | `/character?offset=3`  | Skip N results (default limit is 10) |

### Sorting

Append `?sort=<field>:<asc|desc>` to any list endpoint.

Examples:

- `/character?sort=name:asc`
- `/quote?sort=character:desc`

### Filtering

Filtering translates URL parameter expressions into MongoDB lookup expressions. Can be applied to any key on the data models.

| Option                   | Example                        |
| ------------------------ | ------------------------------ |
| Match                    | `/character?name=Gandalf`      |
| Negate match             | `/character?name!=Frodo`       |
| Include (any of)         | `/character?race=Hobbit,Human` |
| Exclude                  | `/character?race!=Orc,Goblin`  |
| Exists                   | `/character?name`              |
| Doesn't exist            | `/character?!name`             |
| Regex                    | `/character?name=/foot/i`      |
| Negate regex             | `/character?name!=/foot/i`     |
| Less than                | `/movie?budgetInMillions<100`  |
| Greater than             | `/movie?academyAwardWins>0`    |
| Greater than or equal to | `/movie?runtimeInMinutes>=160` |
