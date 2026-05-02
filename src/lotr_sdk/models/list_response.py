from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ListResponse(Generic[T]):
    """Paginated envelope returned by all list operations. Immutable.

    Fields:
        docs: The result items for this page.
        total: Total number of matching documents across all pages.
        limit: Max results per page.
        offset: Number of results skipped.
        page: Current page number (1-indexed).
        pages: Total number of pages.
    """

    docs: list[T]
    total: int
    limit: int
    offset: int
    page: int
    pages: int

    @classmethod
    def from_dict(cls, data: dict, item_factory: Callable[[dict], T]) -> "ListResponse[T]":
        """Construct from a raw API response dict.

        Args:
            data: Raw API response.
            item_factory: Callable that constructs each item from a dict (e.g. `Movie.from_dict`).
        """
        return cls(
            docs=[item_factory(d) for d in data["docs"]],
            total=data["total"],
            limit=data["limit"],
            offset=data["offset"],
            page=data["page"],
            pages=data["pages"],
        )
