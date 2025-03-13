from typing import Any
import polars as pl

from fred_data.observations.types import Observations


def combine_observations(a: Observations, b: Observations) -> Observations:
    combined_observations = pl.concat([a.series, b.series])
    return Observations(
        realtime_start=min(a.realtime_start, b.realtime_start),
        realtime_end=max(a.realtime_end, b.realtime_end),
        count=a.count,
        series=combined_observations,
    )


def get_observations_df(observations_response_json: Any) -> pl.DataFrame:
    observations = observations_response_json["observations"]
    if not observations:
        return pl.DataFrame()

    original_observations_df = pl.from_dicts(observations)
    return original_observations_df.with_columns(
        pl.col("realtime_start", "realtime_end", "date").str.to_date(),
        pl.col("value").cast(pl.Float64),
    )
