from __future__ import annotations

from importlib import util
from pathlib import Path

import pytest
from dask.distributed import LocalCluster
from distributed.scheduler import Scheduler
from distributed.worker import Worker

_SAMPLE_MODULE_NAME = "distributed_scheduler_worker_usage_runtime"
_SAMPLE_PATH = (
    Path(__file__).resolve().parents[1]
    / "typecheck"
    / "samples"
    / "distributed_scheduler_worker_usage.py"
)


def _load_sample_module() -> object:
    spec = util.spec_from_file_location(_SAMPLE_MODULE_NAME, _SAMPLE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load sample module from {_SAMPLE_PATH}")

    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


try:
    _sample = _load_sample_module()
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
    raise RuntimeError(f"Runtime Dask/Distributed required: {exc}") from exc

ensure_scheduler_pass_through = getattr(_sample, "ensure_scheduler_pass_through")
ensure_worker_handles_http = getattr(_sample, "ensure_worker_handles_http")


@pytest.mark.asyncio
async def test_scheduler_worker_sample() -> None:
    async with LocalCluster(
        processes=False,
        asynchronous=True,
        n_workers=1,
        threads_per_worker=1,
        dashboard_address=None,
        scheduler_port=0,
        silence_logs="error",
    ) as cluster:
        scheduler = cluster.scheduler
        worker = next(iter(cluster.workers.values()))

        assert isinstance(scheduler, Scheduler)
        assert isinstance(worker, Worker)

        assert ensure_scheduler_pass_through(scheduler) is scheduler
        assert ensure_worker_handles_http(worker) is worker
