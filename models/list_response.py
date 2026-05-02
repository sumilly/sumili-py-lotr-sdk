from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ListResponse(Generic[T]):
    docs: list[T]
    total: int
    limit: int
    offset: int
    page: int
    pages: int

    @classmethod
    def from_dict(cls, data: dict, item_factory: Callable[[dict], T]) -> "ListResponse[T]":
        return cls(
            docs=[item_factory(d) for d in data["docs"]],
            total=data["total"],
            limit=data["limit"],
            offset=data["offset"],
            page=data["page"],
            pages=data["pages"],
        )
