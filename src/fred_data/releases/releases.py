from dataclasses import dataclass
from datetime import date

import polars as pl

from fred_data.api import FredApiClient, get_json_on_success


@dataclass
class Releases:
    realtime_start: date
    realtime_end: date
    count: int
    releases: pl.DataFrame


def get_releases(
    api_client: FredApiClient,
    *,
    realtime_start: date | None = None,
    realtime_end: date | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> Releases:
    """Get all releases matching the given filter criteria"""
    releases_response = api_client.get(
        "fred/releases",
        {
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
        },
    )
    releases_json = get_json_on_success(releases_response)

    releases_df = pl.from_dicts(releases_json["releases"]).with_columns(
        pl.col("realtime_start", "realtime_end").str.to_date(),
    )
    return Releases(
        realtime_start=date.fromisoformat(releases_json["realtime_start"]),
        realtime_end=date.fromisoformat(releases_json["realtime_end"]),
        count=releases_json["count"],
        releases=releases_df,
    )
