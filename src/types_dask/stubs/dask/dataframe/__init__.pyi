from __future__ import annotations

from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    Protocol,
    Sequence,
    TypeVar,
    overload,
)

from ..delayed import Delayed

class _DataFrameLike(Protocol):
    def to_dict(self, *args: Any, **kwargs: Any) -> Mapping[str, Any]: ...

class _SeriesLike(Protocol):
    name: Any

    def to_list(self, *args: Any, **kwargs: Any) -> Sequence[Any]: ...

_FrameT_co = TypeVar("_FrameT_co", bound=_DataFrameLike, covariant=True)
_SeriesT_co = TypeVar("_SeriesT_co", bound=_SeriesLike, covariant=True)
_FrameT = TypeVar("_FrameT", bound=_DataFrameLike)
_SeriesT = TypeVar("_SeriesT", bound=_SeriesLike)

class DataFrame(Generic[_FrameT_co], Iterable[Any]):
    """Distributed tabular collection backed by pandas."""

    @property
    def columns(self) -> Any: ...
    def compute(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> _FrameT_co: ...
    def persist(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> DataFrame[_FrameT_co]: ...
    def head(self, n: int = ...) -> _FrameT_co: ...
    def to_delayed(self) -> list[Delayed[_FrameT_co]]: ...
    def __iter__(self) -> Iterator[Any]: ...

class Series(Generic[_SeriesT_co], Iterable[Any]):
    """Distributed one-dimensional labelled data."""

    name: Any

    def compute(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> _SeriesT_co: ...
    def persist(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> Series[_SeriesT_co]: ...
    def to_delayed(self) -> list[Delayed[_SeriesT_co]]: ...
    def __iter__(self) -> Iterator[Any]: ...

@overload
def from_delayed(
    dfs: Sequence[Delayed[_FrameT]] | Delayed[_FrameT],
    *,
    meta: _FrameT | None = ...,
    divisions: Sequence[Any] | None = ...,
    sort: bool = ...,
    verify_meta: bool = ...,
) -> DataFrame[_FrameT]: ...
@overload
def from_delayed(
    series: Sequence[Delayed[_SeriesT]] | Delayed[_SeriesT],
    *,
    meta: _SeriesT,
    divisions: Sequence[Any] | None = ...,
    sort: bool = ...,
    verify_meta: bool = ...,
) -> Series[_SeriesT]: ...

__all__ = ["DataFrame", "Series", "from_delayed"]
