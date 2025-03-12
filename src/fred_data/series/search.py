from datetime import date
from typing import Any, Literal

import polars as pl

from fred_data.api import FredApiClient, get_json_on_success
from fred_data.api.pagination import get_item_counter
from fred_data.series.types import MultiSeries

SearchType = Literal["full_text", "series_id"]
SearchRank = Literal["search_rank", "series_id", "title", "last_updated"]


def _combine_multi_series(a: MultiSeries, b: MultiSeries) -> MultiSeries:
    combined_series = pl.concat([a.series, b.series])
    return MultiSeries(
        realtime_start=min(a.realtime_start, b.realtime_start),
        realtime_end=max(a.realtime_end, b.realtime_end),
        count=a.count,
        series=combined_series,
    )


def _get_series_df(series_response_json: Any) -> pl.DataFrame:
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


def get_search_results(
    api_client: FredApiClient,
    search_text: str,
    *,
    realtime_start: date | None = None,
    realtime_end: date | None = None,
    limit: int | None = None,
    search_type: SearchType = "full_text",
    search_rank: SearchRank = "search_rank",
) -> MultiSeries:
    all_series: MultiSeries | None = None
    for search_response in api_client.get_all_pages(
        url="fred/series/search",
        current_page_items_counter=get_item_counter("seriess"),
        query_string_params={
            "search_text": search_text,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "search_type": search_type,
            "search_rank": search_rank,
        },
    ):
        search_response_json = get_json_on_success(search_response)
        series_df = _get_series_df(search_response_json)
        multi_series = MultiSeries(
            realtime_start=date.fromisoformat(search_response_json["realtime_start"]),
            realtime_end=date.fromisoformat(search_response_json["realtime_end"]),
            count=search_response_json["count"],
            series=series_df,
        )
        all_series = (
            multi_series
            if all_series is None
            else _combine_multi_series(all_series, multi_series)
        )

    return all_series
