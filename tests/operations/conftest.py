import pytest

BASE_URL = "https://the-one-api.dev/v2"

MOVIE_DICT = {
    "_id": "5cd95395de30eff6ebccde56",
    "name": "The Lord of the Rings Series",
    "runtimeInMinutes": 558,
    "budgetInMillions": 281.0,
    "boxOfficeRevenueInMillions": 2917.0,
    "academyAwardNominations": 30,
    "academyAwardWins": 17,
    "rottenTomatoesScore": 94.0,
}

QUOTE_DICT = {
    "_id": "5cd96e05de30eff6ebcce7e9",
    "dialog": "Deagol!!",
    "movie": "5cd95395de30eff6ebccde5d",
    "character": "5cd99d4bde30eff6ebccfe9e",
}

LIST_MOVIES_RESPONSE = {
    "docs": [MOVIE_DICT],
    "total": 8,
    "limit": 1000,
    "offset": 0,
    "page": 1,
    "pages": 1,
}

LIST_QUOTES_RESPONSE = {
    "docs": [QUOTE_DICT],
    "total": 2383,
    "limit": 10,
    "offset": 0,
    "page": 1,
    "pages": 239,
}

SINGLE_MOVIE_RESPONSE = {**LIST_MOVIES_RESPONSE, "docs": [MOVIE_DICT], "total": 1}
SINGLE_QUOTE_RESPONSE = {**LIST_QUOTES_RESPONSE, "docs": [QUOTE_DICT], "total": 1}


def make_transport(mocker, json_response: dict):
    t = mocker.MagicMock()
    t.base_url = BASE_URL
    t.request.return_value.json.return_value = json_response
    return t
