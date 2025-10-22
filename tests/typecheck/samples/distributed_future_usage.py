from __future__ import annotations

from typing import Awaitable, MutableMapping, assert_type

from dask import Delayed, delayed
from dask.distributed import AsyncClient, Client, Future


@delayed
def produce_value() -> int:
    return 4


def use_client(client: Client) -> None:
    def add_one(x: int) -> int:
        return x + 1

    future = client.submit(add_one, 2)
    assert_type(future, Future[int])

    gathered_sync = client.gather([future], asynchronous=False)
    assert_type(gathered_sync, list[int])

    gathered_async = client.gather(future, asynchronous=True)
    assert_type(gathered_async, Awaitable[int])

    scattered = client.scatter({"value": 3}, asynchronous=True)
    assert_type(scattered, Awaitable[MutableMapping[str, Future[int]]])

    delayed_value = produce_value()
    computed = client.compute(delayed_value, asynchronous=False)
    assert_type(computed, int)

    awaited = client.compute(delayed_value, asynchronous=True)
    assert_type(awaited, Awaitable[int])

    delayed_future = future.to_delayed()
    assert_type(delayed_future, Delayed[int])


async def use_async_client(client: AsyncClient) -> None:
    future = await client.submit(lambda: "hello")
    assert_type(future, Future[str])

    gathered = await client.gather([future])
    assert_type(gathered, list[str])

    result = await client.compute(produce_value())
    assert_type(result, int)
