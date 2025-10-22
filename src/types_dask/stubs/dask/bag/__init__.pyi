from __future__ import annotations

from typing import Any, Generic, Iterable, Iterator, Sequence, TypeVar

from ..delayed import Delayed

T_co = TypeVar("T_co", covariant=True)

class Bag(Generic[T_co], Iterable[T_co]):
    """Distributed collection of Python objects."""

    def compute(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> list[T_co]: ...
    def persist(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> Bag[T_co]: ...
    def to_delayed(self) -> list[Delayed[list[T_co]]]: ...
    def __iter__(self) -> Iterator[T_co]: ...

def from_delayed(
    bags: Sequence[Delayed[Iterable[T_co]]],
    *,
    length: int | None = ...,
) -> Bag[T_co]: ...

__all__ = ["Bag", "from_delayed"]
