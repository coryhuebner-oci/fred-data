from datetime import date


from fred_data.api import FredApiClient, get_json_on_success
from fred_data.dates import to_date, to_datetime
from fred_data.series.types import Series


def get_series_by_id(
    api_client: FredApiClient,
    series_id: int,
    *,
    realtime_start: date | None = None,
    realtime_end: date | None = None,
    limit: int | None = None,
) -> Series:
    series_response = api_client.get(
        url="fred/series",
        query_string_params={
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
        },
    )
    response_json = get_json_on_success(series_response)
    series_length = len(response_json["seriess"]) if "seriess" in response_json else 0
    if series_length != 1:
        raise KeyError(
            f"Expected exactly 1 series, but found {series_length} for series id {series_id}"
        )
    series = response_json["seriess"][0]
    return Series(
        id=series["id"],
        title=series["title"],
        realtime_start=to_date(series["realtime_start"]),
        realtime_end=to_date(series["realtime_end"]),
        observation_start=to_date(series["observation_start"]),
        observation_end=to_date(series["observation_end"]),
        frequency=series["frequency"],
        frequency_short=series["frequency_short"],
        units=series["units"],
        units_short=series["units_short"],
        seasonal_adjustment=series["seasonal_adjustment"],
        seasonal_adjustment_short=series["seasonal_adjustment_short"],
        last_updated=to_datetime(series["last_updated"]),
        popularity=series["popularity"],
        notes=series["notes"],
    )
