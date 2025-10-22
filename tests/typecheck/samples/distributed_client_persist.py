from __future__ import annotations

from typing import Awaitable, Protocol, assert_type

from dask import Delayed, delayed
from dask.array import Array
from dask.bag import Bag
from dask.dataframe import DataFrame
from dask.distributed import AsyncClient, Client, Future


class _FrameLike(Protocol):
    def to_dict(self, *args: object, **kwargs: object) -> dict[str, object]: ...


@delayed
def produce_value() -> int:
    return 1


def use_client_persist(
    client: Client,
    future: Future[int],
    bag: Bag[int],
    array: Array[int],
    dataframe: DataFrame[_FrameLike],
) -> None:
    delayed_value = produce_value()

    persisted_delayed = client.persist(delayed_value)
    assert_type(persisted_delayed, Delayed[int])

    persisted_list = client.persist([delayed_value])
    assert_type(persisted_list, list[Delayed[int]])

    persisted_future = client.persist(future)
    assert_type(persisted_future, Future[int])

    awaited = client.persist(delayed_value, asynchronous=True)
    assert_type(awaited, Awaitable[Delayed[int]])

    persisted_bag = client.persist(bag)
    assert_type(persisted_bag, Bag[int])

    persisted_array = client.persist(array)
    assert_type(persisted_array, Array[int])

    persisted_dataframe = client.persist(dataframe)
    assert_type(persisted_dataframe, DataFrame[_FrameLike])

    array_list: list[Array[int]] = [array]
    persisted_array_list = client.persist(array_list)
    assert_type(persisted_array_list, list[Array[int]])


async def use_async_client_persist(
    client: AsyncClient,
    future: Future[int],
    bag: Bag[int],
    array: Array[int],
    dataframe: DataFrame[_FrameLike],
) -> None:
    delayed_value = produce_value()

    awaited_delayed = await client.persist(delayed_value)
    assert_type(awaited_delayed, Delayed[int])

    awaited_future = await client.persist(future)
    assert_type(awaited_future, Future[int])

    awaited_bag = await client.persist(bag)
    assert_type(awaited_bag, Bag[int])

    awaited_list = await client.persist([delayed_value])
    assert_type(awaited_list, list[Delayed[int]])

    awaited_array = await client.persist(array)
    assert_type(awaited_array, Array[int])

    awaited_dataframe = await client.persist(dataframe)
    assert_type(awaited_dataframe, DataFrame[_FrameLike])

    array_list: list[Array[int]] = [array]
    awaited_array_list = await client.persist(array_list)
    assert_type(awaited_array_list, list[Array[int]])
