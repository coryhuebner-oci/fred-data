from typing import Any
import polars as pl

from fred_data.series.types import MultiSeries


def combine_multi_series(a: MultiSeries, b: MultiSeries) -> MultiSeries:
    combined_series = pl.concat([a.series, b.series])
    return MultiSeries(
        realtime_start=min(a.realtime_start, b.realtime_start),
        realtime_end=max(a.realtime_end, b.realtime_end),
        count=a.count,
        series=combined_series,
    )


def get_series_df(series_response_json: Any) -> pl.DataFrame:
    series = series_response_json["seriess"]
    if not series:
        return pl.DataFrame()

    original_series_df = pl.from_dicts(series)
    return original_series_df.with_columns(
        pl.col(
            "realtime_start", "realtime_end", "observation_start", "observation_end"
        ).str.to_date(),
        pl.col("last_updated").str.to_datetime(format="%Y-%m-%d %H:%M:%S%#z"),
    ).sort(["title", "observation_start", "observation_end"])
