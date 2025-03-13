from dataclasses import dataclass
from datetime import date, datetime

import polars as pl


@dataclass
class Series:
    id: str
    realtime_start: date
    realtime_end: date
    title: str
    observation_start: date
    observation_end: date
    frequency: str
    frequency_short: str
    units: str
    units_short: str
    seasonal_adjustment: str
    seasonal_adjustment_short: str
    last_updated: datetime
    popularity: int
    notes: str


@dataclass
class MultiSeries:
    realtime_start: date
    realtime_end: date
    count: int
    series: pl.DataFrame
