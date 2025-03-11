from dataclasses import dataclass
from datetime import date

import polars as pl

from fred_data.api.fred_api_client import FredApiClient
from fred_data.api.responses import get_json_on_success


@dataclass
class ReleaseDates:
    realtime_start: date
    realtime_end: date
    count: int
    release_dates: pl.DataFrame


def get_release_dates(
    api_client: FredApiClient,
    *,
    realtime_start: date | None = None,
    realtime_end: date | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> ReleaseDates:
    release_dates_response = api_client.get(
        "fred/releases/dates",
        {
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
        },
    )
    release_dates_json = get_json_on_success(release_dates_response)
    release_dates_df = pl.from_dicts(release_dates_json["release_dates"]).with_columns(
        pl.col("date").str.to_date()
    )
    return ReleaseDates(
        realtime_start=date.fromisoformat(release_dates_json["realtime_start"]),
        realtime_end=date.fromisoformat(release_dates_json["realtime_end"]),
        count=release_dates_json["count"],
        release_dates=release_dates_df,
    )
