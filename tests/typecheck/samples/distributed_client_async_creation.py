from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, assert_type

from dask import delayed
from dask.delayed import Delayed
from dask.distributed import Client, Future

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
    "protocol": "inproc",
    "scheduler_kwargs": {"dashboard": False, "dashboard_address": None},
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

            who_has_all = await async_client.who_has()
            assert_type(who_has_all, Mapping[str, list[str]])

            result = await async_client.compute(persisted)
            assert_type(result, int)
            assert result == 1
        finally:
            await async_client.close()


async def futures_of_persisted_value() -> None:
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
            futures = async_client.futures_of(persisted)
            if TYPE_CHECKING:
                assert_type(futures, list[Future[Any]])
            assert isinstance(futures, list)
            assert all(isinstance(future, Future) for future in futures)

            results = await async_client.gather(futures)
            assert results == [1]

            who_has_all = await async_client.who_has()
            assert_type(who_has_all, Mapping[str, list[str]])
            who_has_subset = await async_client.who_has(futures)
            assert_type(who_has_subset, Mapping[str, list[str]])
            if futures:
                first_key = futures[0].key
                if first_key in who_has_subset:
                    assert isinstance(who_has_subset[first_key], list)
        finally:
            await async_client.close()


async def futures_of_submitted_future() -> None:
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
            future = await async_client.submit(lambda: 41)
            if TYPE_CHECKING:
                assert_type(future, Future[int])

            futures = async_client.futures_of(future)
            if TYPE_CHECKING:
                assert_type(futures, list[Future[Any]])
            assert isinstance(futures, list)
            assert all(isinstance(item, Future) for item in futures)
            assert future in futures or not futures

            result = await async_client.gather(future)
            assert isinstance(result, int)
            assert result == 41

            who_has_all = await async_client.who_has()
            assert_type(who_has_all, Mapping[str, list[str]])
            who_has_subset = await async_client.who_has([future])
            assert_type(who_has_subset, Mapping[str, list[str]])
            if futures and futures[0].key in who_has_subset:
                assert isinstance(who_has_subset[futures[0].key], list)
        finally:
            await async_client.close()


def create_sync_client() -> None:
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
        try:
            who_has_all = client.who_has()
            assert_type(who_has_all, Mapping[str, list[str]])
            assert isinstance(who_has_all, Mapping)
            future = client.submit(lambda: 2)
            subset = client.who_has([future])
            assert_type(subset, Mapping[str, list[str]])
            assert future.key in subset
            assert isinstance(subset[future.key], list)
            result = client.gather(future)
            assert result == 2
        finally:
            client.close()
