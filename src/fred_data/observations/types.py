from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Literal

import polars as pl

# Frequency codes for observations
# See documentation for more details: https://fred.stlouisfed.org/docs/api/fred/series_observations.html#:~:text=An%20optional%20parameter%20that%20indicates%20a%20lower%20frequency%20to%20aggregate%20values%20to
Frequency = Literal[
    "d",
    "w",
    "bw",
    "m",
    "q",
    "sa",
    "a",
    "wef",
    "weth",
    "wew",
    "wetu",
    "wem",
    "wesu",
    "wesa",
    "bwew",
    "bwem",
]

# Unit codes for observations; units are more like "transformations" in FRED land
# See documentation for more details: https://fred.stlouisfed.org/docs/api/fred/series_observations.html#:~:text=A%20key%20that%20indicates%20a%20data%20value%20transformation
Units = Literal["lin", "chg", "ch1", "pch", "pc1", "pca", "cch", "cca", "log"]

# The method for aggregating data when moving to a lower granularity that the source provides
# # See documentation for more details: https://fred.stlouisfed.org/docs/api/fred/series_observations.html#:~:text=A%20key%20that%20indicates%20the%20aggregation%20method%20used%20for%20frequency%20aggregation
AggregationMethod = Literal["avg", "sum", "eop"]


# The output type: allows seeing observations for all observations, real-time period only, new and revised only, etc.
class ObservationOutputType(Enum):
    realtime_period = 1
    all_observations_for_vintage_date = 2
    new_and_revised_observations_for_vintage_date = 3
    initial_release_only = 4


@dataclass
class Observations:
    realtime_start: date
    realtime_end: date
    observation_start: date
    observation_end: date
    units: Units
    output_type: ObservationOutputType
    count: int
    observations: pl.DataFrame
