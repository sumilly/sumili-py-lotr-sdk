from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
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
