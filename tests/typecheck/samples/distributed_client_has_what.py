from __future__ import annotations

from typing import Mapping, Sequence, assert_type

from dask.distributed import AsyncClient, Client


def use_client_has_what(client: Client, worker: str, workers: Sequence[str]) -> None:
    mapping_all = client.has_what()
    assert_type(mapping_all, Mapping[str, list[str]])

    mapping_single = client.has_what(worker)
    assert_type(mapping_single, Mapping[str, list[str]])

    mapping_many = client.has_what(workers)
    assert_type(mapping_many, Mapping[str, list[str]])


async def use_async_client_has_what(
    client: AsyncClient,
    worker: str,
    workers: Sequence[str],
) -> None:
    mapping_all = await client.has_what()
    assert_type(mapping_all, Mapping[str, list[str]])

    mapping_single = await client.has_what(worker)
    assert_type(mapping_single, Mapping[str, list[str]])

    mapping_many = await client.has_what(workers)
    assert_type(mapping_many, Mapping[str, list[str]])
