from __future__ import annotations

from typing import Any, Iterable, Iterator, Literal, Sequence, TypeVar, overload

from ..delayed import Delayed

T_co = TypeVar("T_co", covariant=True)

class Array(Iterable[T_co]):
    """Distributed array-like collection."""

    def compute(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> T_co: ...
    def persist(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> Array[T_co]: ...
    def to_delayed(self) -> list[list[Delayed[T_co]]]: ...
    def __iter__(self) -> Iterator[T_co]: ...

_ShapeLike = Sequence[int] | tuple[int, ...]
_ChunksLike = Sequence[int] | tuple[int, ...] | Literal["auto"] | None

@overload
def from_delayed(
    value: Delayed[T_co],
    shape: _ShapeLike,
    dtype: Any,
    *,
    meta: Any = ...,
    name: str | None = ...,
    verify_meta: bool = ...,
    nout: None = ...,
    chunks: _ChunksLike = ...,
) -> Array[T_co]: ...
@overload
def from_delayed(
    values: Sequence[Delayed[T_co]],
    shape: _ShapeLike,
    dtype: Any,
    *,
    meta: Any = ...,
    name: str | None = ...,
    verify_meta: bool = ...,
    nout: int,
    chunks: _ChunksLike = ...,
) -> Array[T_co]: ...

__all__ = ["Array", "from_delayed"]
