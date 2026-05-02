from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    """A single movie from the API. Immutable.

    Fields:
        id: Unique identifier.
        name: Movie title.
        runtime_in_minutes: Total runtime.
        budget_in_millions: Production budget (USD millions).
        box_office_revenue_in_millions: Box office gross (USD millions).
        academy_award_nominations: Number of nominations.
        academy_award_wins: Number of wins.
        rotten_tomatoes_score: Score out of 100.
    """

    id: str
    name: str
    runtime_in_minutes: int
    budget_in_millions: float
    box_office_revenue_in_millions: float
    academy_award_nominations: int
    academy_award_wins: int
    rotten_tomatoes_score: float

    @classmethod
    def from_dict(cls, data: dict) -> "Movie":
        """Construct from a raw API response dict."""
        return cls(
            id=data["_id"],
            name=data["name"],
            runtime_in_minutes=data["runtimeInMinutes"],
            budget_in_millions=data["budgetInMillions"],
            box_office_revenue_in_millions=data["boxOfficeRevenueInMillions"],
            academy_award_nominations=data["academyAwardNominations"],
            academy_award_wins=data["academyAwardWins"],
            rotten_tomatoes_score=data["rottenTomatoesScore"],
        )
