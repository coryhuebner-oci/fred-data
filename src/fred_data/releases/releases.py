from dataclasses import dataclass
from datetime import date

import polars as pl

from fred_data.api import FredApiClient, get_json_on_success
from fred_data.api.pagination import get_item_counter


@dataclass
class Releases:
    realtime_start: date
    realtime_end: date
    count: int
    releases: pl.DataFrame


def _combine_releases(a: Releases, b: Releases) -> Releases:
    combined_release_dates = pl.concat([a.release_dates, b.release_dates])
    return Releases(
        realtime_start=min(a.realtime_start, b.realtime_start),
        realtime_end=max(a.realtime_end, b.realtime_end),
        count=a.count,
        release_dates=combined_release_dates,
    )


def get_releases(
    api_client: FredApiClient,
    *,
    realtime_start: date | None = None,
    realtime_end: date | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> Releases:
    """Get all releases matching the given filter criteria"""
    all_releases: Releases | None = None
    for releases_response in api_client.get_all_pages(
        "fred/releases",
        current_page_items_counter=get_item_counter("releases"),
        query_string_params={
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
        },
    ):
        releases_json = get_json_on_success(releases_response)

        releases_df = pl.from_dicts(releases_json["releases"]).with_columns(
            pl.col("realtime_start", "realtime_end").str.to_date(),
        )
        releases = Releases(
            realtime_start=date.fromisoformat(releases_json["realtime_start"]),
            realtime_end=date.fromisoformat(releases_json["realtime_end"]),
            count=releases_json["count"],
            releases=releases_df,
        )
        return (
            releases
            if all_releases is None
            else _combine_releases(all_releases, releases)
        )

    return all_releases
