from __future__ import annotations

from typing import assert_type

from dask import Delayed, compute, delayed
from dask.delayed import delayed as delayed_ctor


@delayed
def meaning() -> int:
    return 42


task = meaning()
assert_type(task, Delayed[int])
assert_type(task.compute(), int)

value_task = delayed(5)
assert_type(value_task, Delayed[int])

assert_type(compute(task), int)

decorated = delayed_ctor(lambda: "hi")
assert_type(decorated(), Delayed[str])
