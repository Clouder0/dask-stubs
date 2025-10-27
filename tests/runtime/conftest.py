from __future__ import annotations

from collections.abc import Iterator

import dask.config
import pytest
from distributed.scheduler import Scheduler
from distributed.worker import Worker


@pytest.fixture(autouse=True)
def configure_inproc_runtime(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Force inproc comms and skip HTTP server start for runtime tests."""

    monkeypatch.setattr(Scheduler, "start_http_server", lambda self, *_, **__: None)
    monkeypatch.setattr(Worker, "start_http_server", lambda self, *_, **__: None)
    with dask.config.set(
        {
            "distributed.comm.default-scheme": "inproc",
            "distributed.scheduler.allowed-failures": 0,
            "distributed.admin.tick.interval": "10ms",
        }
    ):
        yield
