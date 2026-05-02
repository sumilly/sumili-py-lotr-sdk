import pytest
from lotr_sdk import ListResponse, Movie, Quote


# --- Fixtures ---

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


# --- Movie ---

def test_movie_from_dict():
    movie = Movie.from_dict(MOVIE_DICT)
    assert movie.id == "5cd95395de30eff6ebccde56"
    assert movie.name == "The Lord of the Rings Series"
    assert movie.runtime_in_minutes == 558
    assert movie.budget_in_millions == 281.0
    assert movie.box_office_revenue_in_millions == 2917.0
    assert movie.academy_award_nominations == 30
    assert movie.academy_award_wins == 17
    assert movie.rotten_tomatoes_score == 94.0


def test_movie_is_immutable():
    movie = Movie.from_dict(MOVIE_DICT)
    with pytest.raises(Exception):
        movie.name = "other"


# --- Quote ---

def test_quote_from_dict():
    quote = Quote.from_dict(QUOTE_DICT)
    assert quote.id == "5cd96e05de30eff6ebcce7e9"
    assert quote.dialog == "Deagol!!"
    assert quote.movie_id == "5cd95395de30eff6ebccde5d"
    assert quote.character_id == "5cd99d4bde30eff6ebccfe9e"


def test_quote_is_immutable():
    quote = Quote.from_dict(QUOTE_DICT)
    with pytest.raises(Exception):
        quote.dialog = "other"


# --- ListResponse ---

def test_list_response_from_dict_with_movies():
    data = {
        "docs": [MOVIE_DICT],
        "total": 8,
        "limit": 1000,
        "offset": 0,
        "page": 1,
        "pages": 1,
    }
    result = ListResponse.from_dict(data, Movie.from_dict)
    assert result.total == 8
    assert result.limit == 1000
    assert result.offset == 0
    assert result.page == 1
    assert result.pages == 1
    assert len(result.docs) == 1
    assert isinstance(result.docs[0], Movie)
    assert result.docs[0].name == "The Lord of the Rings Series"


def test_list_response_from_dict_with_quotes():
    data = {
        "docs": [QUOTE_DICT, QUOTE_DICT],
        "total": 2383,
        "limit": 10,
        "offset": 0,
        "page": 1,
        "pages": 239,
    }
    result = ListResponse.from_dict(data, Quote.from_dict)
    assert len(result.docs) == 2
    assert all(isinstance(q, Quote) for q in result.docs)


def test_list_response_empty_docs():
    data = {"docs": [], "total": 0, "limit": 10, "offset": 0, "page": 1, "pages": 0}
    result = ListResponse.from_dict(data, Movie.from_dict)
    assert result.docs == []
    assert result.total == 0
