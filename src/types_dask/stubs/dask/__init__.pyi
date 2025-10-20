from __future__ import annotations

from types import ModuleType
from typing import Any, Callable, Generator, Generic, Iterable, ParamSpec, TypeVar, overload

T = TypeVar("T")
P = ParamSpec("P")

class Delayed(Generic[T]):
    """Deferred computation produced by ``dask.delayed``."""

    def compute(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> T: ...
    def persist(
        self,
        *,
        scheduler: str | None = ...,
        optimize_graph: bool = ...,
        traverse: bool | None = ...,
        **kwargs: Any,
    ) -> Delayed[T]: ...
    def __await__(self) -> Generator[Any, Any, T]: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Delayed[Any]: ...
    def __iter__(self) -> Iterable[T]: ...
    def __repr__(self) -> str: ...

@overload
def delayed(__func: Callable[P, T], /) -> Callable[P, Delayed[T]]: ...
@overload
def delayed(__func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> Delayed[T]: ...
@overload
def delayed(*args: Any, **kwargs: Any) -> Delayed[Any]: ...  # pyright: ignore[reportOverlappingOverload]
def compute(*args: Delayed[Any], **kwargs: Any) -> tuple[Any, ...]: ...
def persist(*args: Delayed[Any], **kwargs: Any) -> tuple[Delayed[Any], ...]: ...

bag: ModuleType
array: ModuleType
dataframe: ModuleType

__all__ = ["Delayed", "delayed", "compute", "persist", "bag", "array", "dataframe"]
