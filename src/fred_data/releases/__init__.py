from dataclasses import dataclass
from datetime import date

import polars as pl

from fred_data.api.fred_api_client import FredApiClient


@dataclass
class Releases:
    realtime_start: date
    realtime_end: date
    count: int
    releases: pl.DataFrame


def get_releases(
    api_client: FredApiClient,
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
    if not releases_response.status == 200:
        raise ValueError(
            f"Received non success status from {releases_response.url}. Status: {releases_response.status}"
        )
    releases_json = releases_response.json()

    return Releases(
        realtime_start=date.fromisoformat(releases_json["realtime_start"]),
        realtime_end=date.fromisoformat(releases_json["realtime_end"]),
        count=releases_json["count"],
        releases=pl.from_dicts(releases_json["releases"]),
    )
