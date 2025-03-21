from datetime import date
from typing import Literal


from fred_data.api import FredApiClient, get_json_on_success
from fred_data.api.pagination import get_item_counter
from fred_data.series.transformations import combine_multi_series, get_series_df
from fred_data.series.types import MultiSeries

SearchType = Literal["full_text", "series_id"]
SearchRank = Literal["search_rank", "series_id", "title", "last_updated"]


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
