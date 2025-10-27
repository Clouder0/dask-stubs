from __future__ import annotations

from collections.abc import Iterator, MutableMapping, Sequence
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generator,
    Generic,
    Iterable,
    Literal,
    Mapping,
    ParamSpec,
    TypeVar,
    overload,
)

from dask.delayed import Delayed
from .scheduler import Scheduler
from .worker import Worker, WorkerPlugin

T = TypeVar("T")
U = TypeVar("U")
KT = TypeVar("KT")
P = ParamSpec("P")
T_co = TypeVar("T_co", covariant=True)
PersistableT = TypeVar("PersistableT")

class Future(Generic[T_co]):
    """Remote result managed by a Dask scheduler."""

    key: str
    status: str
    client: Client

    def cancel(self) -> bool: ...
    def cancelled(self) -> bool: ...
    def done(self) -> bool: ...
    def result(self, timeout: float | None = ..., **kwargs: Any) -> T_co: ...
    def exception(self, timeout: float | None = ...) -> BaseException | None: ...
    def add_done_callback(self, fn: Callable[[Future[T_co]], Any]) -> None: ...
    def release(self) -> None: ...
    def to_delayed(self) -> Delayed[T_co]: ...
    def __await__(self) -> Generator[Any, Any, T_co]: ...
    def __repr__(self) -> str: ...

class AsCompleted(Iterable[Future[Any]]):
    """Iterator that yields futures as they finish."""

    def __iter__(self) -> Iterator[Future[Any]]: ...
    def results(self, timeout: float | None = ...) -> list[Any]: ...

class Client:
    """Synchronous entry point to a Dask scheduler."""

    asynchronous: bool
    scheduler: str | None
    planner: str | None

    def __init__(
        self,
        address: str | None = ...,
        *,
        loop: Any = ...,
        asynchronous: bool | None = ...,
        timeout: float | None = ...,
        set_as_default: bool = ...,
        **kwargs: Any,
    ) -> None: ...
    def close(self, *, timeout: float | None = ...) -> None: ...
    def shutdown(self, *, timeout: float | None = ...) -> None: ...
    def restart(self, timeout: float | None = ...) -> None: ...
    def submit(self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> Future[T]: ...
    def map(
        self,
        func: Callable[..., T],
        *iterables: Iterable[Any],
        key: str | None = ...,
        **kwargs: Any,
    ) -> list[Future[T]]: ...
    @overload
    @overload
    def gather(
        self,
        futures: Future[T],
        *,
        errors: str = ...,
        direct: bool = ...,
        asynchronous: Literal[True],
    ) -> Awaitable[T]: ...
    @overload
    def gather(
        self,
        futures: Sequence[Future[T]],
        *,
        errors: str = ...,
        direct: bool = ...,
        asynchronous: Literal[True],
    ) -> Awaitable[list[T]]: ...
    @overload
    def gather(
        self,
        futures: Future[T],
        *,
        errors: str = ...,
        direct: bool = ...,
        asynchronous: Literal[False] | None = ...,
    ) -> T: ...
    @overload
    def gather(
        self,
        futures: Sequence[Future[T]],
        *,
        errors: str = ...,
        direct: bool = ...,
        asynchronous: Literal[False] | None = ...,
    ) -> list[T]: ...
    @overload
    def scatter(
        self,
        data: Mapping[KT, T],
        *,
        broadcast: bool = ...,
        direct: bool = ...,
        hash: bool | None = ...,
        asynchronous: Literal[True],
    ) -> Awaitable[MutableMapping[KT, Future[T]]]: ...
    @overload
    def scatter(
        self,
        data: Mapping[KT, T],
        *,
        broadcast: bool = ...,
        direct: bool = ...,
        hash: bool | None = ...,
        asynchronous: Literal[False] | None = ...,
    ) -> MutableMapping[KT, Future[T]]: ...
    @overload
    def scatter(
        self,
        data: Sequence[T],
        *,
        broadcast: bool = ...,
        direct: bool = ...,
        hash: bool | None = ...,
        asynchronous: Literal[True],
    ) -> Awaitable[list[Future[T]]]: ...
    @overload
    def scatter(
        self,
        data: Sequence[T],
        *,
        broadcast: bool = ...,
        direct: bool = ...,
        hash: bool | None = ...,
        asynchronous: Literal[False] | None = ...,
    ) -> list[Future[T]]: ...
    @overload
    def compute(
        self,
        collection: Delayed[T],
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
        asynchronous: Literal[True],
    ) -> Awaitable[T]: ...
    @overload
    def compute(
        self,
        collection: Any,
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
        asynchronous: Literal[True],
    ) -> Awaitable[Any]: ...
    @overload
    def compute(
        self,
        collection: Delayed[T],
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
        asynchronous: Literal[False] | None = ...,
    ) -> T: ...
    @overload
    def compute(
        self,
        collection: Any,
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
        asynchronous: Literal[False] | None = ...,
    ) -> Any: ...
    @overload
    def persist(
        self,
        collection: PersistableT,
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
        traverse: bool | None = ...,
        asynchronous: Literal[True],
    ) -> Awaitable[PersistableT]: ...
    @overload
    def persist(
        self,
        collection: PersistableT,
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
        traverse: bool | None = ...,
        asynchronous: Literal[False] | None = ...,
    ) -> PersistableT: ...
    def get_future(self, key: str) -> Future[Any]: ...
    def cancel(self, futures: Future[Any] | Sequence[Future[Any]]) -> None: ...
    def futures_of(self, collection: Any) -> list[Future[Any]]: ...
    def publish_dataset(self, name: str, data: Any, *, override: bool = ...) -> None: ...
    def list_datasets(self) -> Dict[str, str]: ...
    def get_dataset(self, name: str) -> Any: ...
    def run(self, function: Callable[..., U], *args: Any, **kwargs: Any) -> Dict[str, U]: ...
    def run_on_scheduler(self, function: Callable[..., U], *args: Any, **kwargs: Any) -> U: ...
    def wait_for_workers(self, n_workers: int = ..., timeout: float | None = ...) -> None: ...
    def sync(
        self,
        func: Callable[..., U],
        *args: Any,
        asynchronous: bool | None = ...,
        **kwargs: Any,
    ) -> U: ...
    def scheduler_info(self) -> Dict[str, Any]: ...
    def __await__(self) -> Generator[Any, Any, AsyncClient]: ...
    def __enter__(self) -> Client: ...
    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None: ...
    async def __aenter__(self) -> AsyncClient: ...
    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None: ...

class AsyncClient:
    """Async wrapper around :class:`Client`."""

    asynchronous: bool

    def __init__(
        self,
        address: str | None = ...,
        *,
        loop: Any = ...,
        timeout: float | None = ...,
        set_as_default: bool = ...,
        **kwargs: Any,
    ) -> None: ...
    async def submit(
        self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
    ) -> Future[T]: ...
    async def map(
        self,
        func: Callable[..., T],
        *iterables: Iterable[Any],
        key: str | None = ...,
        **kwargs: Any,
    ) -> list[Future[T]]: ...
    async def close(self, *, timeout: float | None = ...) -> None: ...
    async def shutdown(self, *, timeout: float | None = ...) -> None: ...
    @overload
    async def gather(
        self,
        futures: Future[T],
        *,
        errors: str = ...,
        direct: bool = ...,
    ) -> T: ...
    @overload
    async def gather(
        self,
        futures: Sequence[Future[T]],
        *,
        errors: str = ...,
        direct: bool = ...,
    ) -> list[T]: ...
    @overload
    async def scatter(
        self,
        data: Mapping[KT, T],
        *,
        broadcast: bool = ...,
        direct: bool = ...,
        hash: bool | None = ...,
    ) -> MutableMapping[KT, Future[T]]: ...
    @overload
    async def scatter(
        self,
        data: Sequence[T],
        *,
        broadcast: bool = ...,
        direct: bool = ...,
        hash: bool | None = ...,
    ) -> list[Future[T]]: ...
    @overload
    async def compute(
        self,
        collection: Delayed[T],
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
    ) -> T: ...
    @overload
    async def compute(
        self,
        collection: Any,
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
    ) -> Any: ...
    def persist(
        self,
        collection: PersistableT,
        *,
        optimize_graph: bool = ...,
        scheduler: str | None = ...,
        traverse: bool | None = ...,
    ) -> PersistableT: ...

class LocalCluster:
    """In-process cluster useful for tests and experimentation."""

    asynchronous: bool
    scheduler: Scheduler
    workers: MutableMapping[str, Worker]
    address: str

    def __init__(
        self,
        *,
        asynchronous: bool = ...,
        processes: bool = ...,
        n_workers: int | None = ...,
        threads_per_worker: int | None = ...,
        scheduler_port: int | str | None = ...,
        dashboard_address: str | None = ...,
        silence_logs: bool | str | None = ...,
        scheduler_kwargs: Mapping[str, Any] | None = ...,
        worker_kwargs: Mapping[str, Any] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    async def __aenter__(self) -> LocalCluster: ...
    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None: ...
    def __enter__(self) -> LocalCluster: ...
    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None: ...
    async def start(self, *args: Any, **kwargs: Any) -> LocalCluster: ...
    async def close(self, timeout: float | None = ...) -> None: ...
    def sync(
        self, func: Callable[..., T], *args: Any, asynchronous: bool | None = ..., **kwargs: Any
    ) -> T: ...

@overload
def wait(
    futures: Future[Any],
    *,
    return_when: str = ...,
    timeout: float | None = ...,
) -> Future[Any]: ...
@overload
def wait(
    futures: Sequence[Future[Any]],
    *,
    return_when: str = ...,
    timeout: float | None = ...,
) -> list[Future[Any]]: ...
def as_completed(
    futures: Iterable[Future[Any]],
    *,
    with_results: bool = ...,
) -> AsCompleted: ...
def default_client() -> Client: ...
def get_client() -> Client: ...

__all__ = [
    "AsyncClient",
    "AsCompleted",
    "Client",
    "Future",
    "LocalCluster",
    "Scheduler",
    "Worker",
    "WorkerPlugin",
    "as_completed",
    "default_client",
    "get_client",
    "wait",
]
