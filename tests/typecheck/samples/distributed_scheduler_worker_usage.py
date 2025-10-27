from __future__ import annotations

from typing import assert_type

from distributed import LocalCluster
from distributed.scheduler import Scheduler
from distributed.worker import Worker


def ensure_scheduler_pass_through(scheduler: Scheduler) -> Scheduler:
    scheduler.start_http_server()
    return scheduler


def ensure_worker_handles_http(worker: Worker) -> Worker:
    worker.start_http_server()
    return worker


async def use_local_cluster() -> None:
    async with LocalCluster(processes=False, asynchronous=True, n_workers=1) as cluster:
        scheduler = ensure_scheduler_pass_through(cluster.scheduler)
        worker = ensure_worker_handles_http(next(iter(cluster.workers.values())))
        assert_type(scheduler, Scheduler)
        assert_type(worker, Worker)
