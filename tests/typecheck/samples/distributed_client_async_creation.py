from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Mapping, assert_type

from dask import delayed
from dask.delayed import Delayed
from dask.distributed import Client

if TYPE_CHECKING:
    from dask.distributed import AsyncClient
else:
    AsyncClient = Client

if TYPE_CHECKING:
    DelayedInt = Delayed[int]
else:
    DelayedInt = Delayed

_LOCAL_CLUSTER_KWARGS: Mapping[str, Any] = {
    "processes": False,
    "scheduler_port": 0,
    "threads_per_worker": 1,
    "timeout": "2s",
    "dashboard_address": None,
}


@delayed
def _produce_value() -> int:
    return 1


class ClusterUnavailable(RuntimeError):
    """Raised when a local in-process cluster cannot be started."""


def _raise_cluster_failed(exc: Exception) -> None:
    raise ClusterUnavailable("local cluster unavailable for async client sample") from exc


async def await_client_creation() -> None:
    try:
        async_client = await Client(asynchronous=True, **_LOCAL_CLUSTER_KWARGS)
    except OSError as exc:
        _raise_cluster_failed(exc)
    except RuntimeError as exc:
        if "Cluster failed to start" in str(exc):
            _raise_cluster_failed(exc)
        raise
    else:
        assert_type(async_client, AsyncClient)
        await async_client.close()


async def use_async_context_manager() -> None:
    try:
        async with Client(asynchronous=True, **_LOCAL_CLUSTER_KWARGS) as async_client:
            assert_type(async_client, AsyncClient)
    except OSError as exc:
        _raise_cluster_failed(exc)
    except RuntimeError as exc:
        if "Cluster failed to start" in str(exc):
            _raise_cluster_failed(exc)
        raise


async def persist_without_await() -> None:
    try:
        async_client = await Client(asynchronous=True, **_LOCAL_CLUSTER_KWARGS)
    except OSError as exc:
        _raise_cluster_failed(exc)
    except RuntimeError as exc:
        if "Cluster failed to start" in str(exc):
            _raise_cluster_failed(exc)
        raise
    else:
        try:
            delayed_value: Delayed[int] = _produce_value()
            persisted = async_client.persist(delayed_value)
            assert_type(persisted, DelayedInt)

            result = await async_client.compute(persisted)
            assert_type(result, int)
            assert result == 1
        finally:
            await async_client.close()


def create_sync_client() -> None:
    asyncio.run(await_client_creation())
    try:
        client = Client(**_LOCAL_CLUSTER_KWARGS)
    except OSError as exc:
        _raise_cluster_failed(exc)
    except RuntimeError as exc:
        if "Cluster failed to start" in str(exc):
            _raise_cluster_failed(exc)
        raise
    else:
        assert_type(client, Client)
        client.close()
