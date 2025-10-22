from __future__ import annotations

from typing import assert_type

from dask import array, delayed


class FakeArray:
    def __array__(self) -> object: ...


@delayed
def build_array() -> FakeArray:
    return FakeArray()


arr = array.from_delayed(build_array(), shape=(1,), dtype="f8")
assert_type(arr, array.Array[FakeArray])
assert_type(arr.compute(), FakeArray)
