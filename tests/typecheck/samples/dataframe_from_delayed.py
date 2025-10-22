from __future__ import annotations

from typing import assert_type

from dask import dataframe, delayed


class Frame:
    def to_dict(self) -> dict[str, int]:
        return {"value": 1}


class SeriesLike:
    name = "values"

    def to_list(self) -> list[int]:
        return [1, 2, 3]


@delayed
def build_frame() -> Frame:
    return Frame()


@delayed
def build_series() -> SeriesLike:
    return SeriesLike()


df = dataframe.from_delayed([build_frame()], meta=Frame())
assert_type(df, dataframe.DataFrame[Frame])
assert_type(df.compute(), Frame)

series = dataframe.from_delayed([build_series()], meta=SeriesLike())
assert_type(series, dataframe.Series[SeriesLike])
assert_type(series.compute(), SeriesLike)
