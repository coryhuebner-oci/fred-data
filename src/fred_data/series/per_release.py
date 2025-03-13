from dataclasses import dataclass
from datetime import date
from typing import Literal


from fred_data.api import FredApiClient, get_json_on_success
from fred_data.api.pagination import get_item_counter
from fred_data.series.transformations import combine_multi_series, get_series_df
from fred_data.series.types import MultiSeries

FilterVariable = Literal["frequency", "units", "seasonal_adjustment"]


@dataclass
class SeriesFilter:
    variable: FilterVariable
    value: str


def get_series_for_release(
    api_client: FredApiClient,
    release_id: int,
    *,
    realtime_start: date | None = None,
    realtime_end: date | None = None,
    limit: int | None = None,
    series_filter: SeriesFilter | None = None,
) -> MultiSeries:
    all_series: MultiSeries | None = None
    for search_response in api_client.get_all_pages(
        url="fred/release/series",
        current_page_items_counter=get_item_counter("seriess"),
        query_string_params={
            "release_id": release_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "filter_variable": series_filter.variable if series_filter else None,
            "filter_value": series_filter.value if series_filter else None,
        },
    ):
        search_response_json = get_json_on_success(search_response)
        series_df = get_series_df(search_response_json)
        multi_series = MultiSeries(
            realtime_start=date.fromisoformat(search_response_json["realtime_start"]),
            realtime_end=date.fromisoformat(search_response_json["realtime_end"]),
            count=search_response_json["count"],
            series=series_df,
        )
        all_series = (
            multi_series
            if all_series is None
            else combine_multi_series(all_series, multi_series)
        )

    return all_series
