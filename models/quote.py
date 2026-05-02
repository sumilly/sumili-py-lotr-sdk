from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    id: str
    dialog: str
    movie_id: str
    character_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        return cls(
            id=data["_id"],
            dialog=data["dialog"],
            movie_id=data["movie"],
            character_id=data["character"],
        )
