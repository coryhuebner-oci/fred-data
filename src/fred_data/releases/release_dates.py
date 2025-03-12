from dataclasses import dataclass
from datetime import date, timedelta

import polars as pl

from fred_data.api import FredApiClient, get_json_on_success
from fred_data.api.pagination import get_item_counter


@dataclass
class ReleaseDates:
    realtime_start: date
    realtime_end: date
    count: int
    release_dates: pl.DataFrame


def _combine_release_dates(a: ReleaseDates, b: ReleaseDates) -> ReleaseDates:
    combined_release_dates = pl.concat([a.release_dates, b.release_dates])
    return ReleaseDates(
        realtime_start=min(a.realtime_start, b.realtime_start),
        realtime_end=max(a.realtime_end, b.realtime_end),
        count=a.count,
        release_dates=combined_release_dates,
    )


def _validate_release_dates(realtime_start: date, realtime_end: date):
    if realtime_end - realtime_start > timedelta(days=100):
        raise ValueError(f"For now, a maximum of 100 days are supported")


def get_release_dates(
    api_client: FredApiClient,
    realtime_start: date = date.today() - timedelta(days=7),
    realtime_end: date = date.today() + timedelta(days=7),
    *,
    limit: int | None = None,
    include_release_dates_with_no_data: bool = False,
) -> ReleaseDates:
    _validate_release_dates(realtime_start, realtime_end)

    all_release_dates: ReleaseDates | None = None
    for release_dates_response in api_client.get_all_pages(
        url="fred/releases/dates",
        current_page_items_counter=get_item_counter("release_dates"),
        query_string_params={
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "include_release_dates_with_no_data": include_release_dates_with_no_data,
        },
    ):
        release_dates_json = get_json_on_success(release_dates_response)
        original_release_dates_df = pl.from_dicts(release_dates_json["release_dates"])
        release_dates_df = original_release_dates_df.with_columns(
            pl.col("date").str.to_date(),
            pl.col("release_last_updated").str.to_datetime(
                format="%Y-%m-%d %H:%M:%S%#z"
            ),
        ).sort(["release_name", "date", "release_last_updated"])
        release_dates = ReleaseDates(
            realtime_start=date.fromisoformat(release_dates_json["realtime_start"]),
            realtime_end=date.fromisoformat(release_dates_json["realtime_end"]),
            count=release_dates_json["count"],
            release_dates=release_dates_df,
        )
        all_release_dates = (
            release_dates
            if all_release_dates is None
            else _combine_release_dates(all_release_dates, release_dates)
        )

    return all_release_dates
