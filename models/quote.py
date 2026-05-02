from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    """A single movie quote from the API. Immutable.

    Fields:
        id: Unique identifier.
        dialog: The spoken text.
        movie_id: ID of the movie this quote is from.
        character_id: ID of the character who spoke it.
    """

    id: str
    dialog: str
    movie_id: str
    character_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        """Construct from a raw API response dict."""
        return cls(
            id=data["_id"],
            dialog=data["dialog"],
            movie_id=data["movie"],
            character_id=data["character"],
        )
