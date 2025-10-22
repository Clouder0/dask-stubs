from __future__ import annotations

from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Iterable,
    ParamSpec,
    TypeVar,
    overload,
)

T = TypeVar("T")
R = TypeVar("R")
S = TypeVar("S")
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
def delayed(__func: Callable[P, R], /) -> Callable[P, Delayed[R]]: ...  # type: ignore[overload-overlap]
@overload
def delayed(__func: Callable[P, R], /, *args: P.args, **kwargs: P.kwargs) -> Delayed[R]: ...

# ``delayed`` accepts both callables and plain values. Because Python's type system
# cannot express "non-callable object" today, the following value overload overlaps
# with the callable overloads above. We keep the richer typing and silence mypy.
@overload
def delayed(
    __value: S,
    /,
    *,
    pure: bool | None = ...,
    traverse: bool = ...,
    name: str | None = ...,
    nout: int | None = ...,
) -> Delayed[S]: ...
@overload
def compute(
    __value: Delayed[T],
    /,
    *,
    scheduler: str | None = ...,
    optimize_graph: bool = ...,
    traverse: bool | None = ...,
    **kwargs: Any,
) -> T: ...
@overload
def compute(
    *__values: Delayed[Any],
    scheduler: str | None = ...,
    optimize_graph: bool = ...,
    traverse: bool | None = ...,
    **kwargs: Any,
) -> tuple[Any, ...]: ...
@overload
def persist(__value: Delayed[T], /, **kwargs: Any) -> Delayed[T]: ...
@overload
def persist(*__values: Delayed[Any], **kwargs: Any) -> tuple[Delayed[Any], ...]: ...

__all__ = ["Delayed", "compute", "delayed", "persist"]
