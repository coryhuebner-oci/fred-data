from dataclasses import dataclass
from datetime import date
from typing import Literal


from fred_data.api import FredApiClient, get_json_on_success
from fred_data.api.pagination import get_item_counter
from fred_data.observations.transformations import (
    combine_observations,
    get_observations_df,
)
from fred_data.observations.types import (
    AggregationMethod,
    Frequency,
    ObservationOutputType,
    Observations,
    Units,
)


def _to_date(value: str):
    return date.fromisoformat(value)


def get_observations_for_series(
    api_client: FredApiClient,
    series_id: str,
    observation_start: date,
    observation_end: date,
    *,
    realtime_start: date | None = None,
    realtime_end: date | None = None,
    limit: int | None = None,
    units: Units | None = None,
    frequency: Frequency | None = None,
    aggregation_method: AggregationMethod | None = None,
    output_type: ObservationOutputType | None = None,
) -> Observations:
    all_observations: Observations | None = None
    for response in api_client.get_all_pages(
        url="fred/series/observations",
        current_page_items_counter=get_item_counter("observations"),
        query_string_params={
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "observation_start": observation_start,
            "observation_end": observation_end,
            "limit": limit,
            "units": units,
            "frequency": frequency,
            "aggregation_method": aggregation_method,
            "output_type": output_type.value if output_type else None,
        },
    ):
        response_json = get_json_on_success(response)
        observations_df = get_observations_df(response_json)
        observations = Observations(
            realtime_start=_to_date(response_json["realtime_start"]),
            realtime_end=_to_date(response_json["realtime_end"]),
            observation_start=_to_date(response_json["observation_start"]),
            observation_end=_to_date(response_json["observation_end"]),
            count=response_json["count"],
            units=response_json["units"],
            output_type=ObservationOutputType(response_json["output_type"]),
            observations=observations_df,
        )
        all_observations = (
            observations
            if all_observations is None
            else combine_observations(all_observations, observations)
        )

    return all_observations
