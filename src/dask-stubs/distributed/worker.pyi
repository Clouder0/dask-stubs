from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Protocol

from .scheduler import Scheduler

class WorkerPlugin(Protocol):
    def setup(self, worker: Worker) -> None: ...
    def teardown(self, worker: Worker) -> None: ...

class Worker:
    """Execute tasks dispatched by a :class:`Scheduler`."""

    address: str
    scheduler: Scheduler
    nthreads: int

    def __init__(
        self,
        scheduler: str | Scheduler,
        *,
        nthreads: int | None = ...,
        name: str | None = ...,
        loop: Any | None = ...,
        resources: dict[str, float] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    async def start(self) -> Worker: ...
    async def finished(self) -> None: ...
    async def close(self, *, safe: bool = ..., fast: bool = ...) -> None: ...
    def start_http_server(self, *args: Any, **kwargs: Any) -> None: ...
    def execute(self, key: str) -> Awaitable[Any]: ...
    def add_plugin(self, plugin: WorkerPlugin, name: str | None = ...) -> None: ...
    def log_event(self, topic: str, msg: Any) -> None: ...

__all__ = ["Worker", "WorkerPlugin"]
