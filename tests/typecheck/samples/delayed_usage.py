from __future__ import annotations

from typing import assert_type

from dask import Delayed, delayed


@delayed
def meaning() -> int:
    return 42


task = meaning()
assert_type(task, Delayed[int])
assert_type(task.compute(), int)
