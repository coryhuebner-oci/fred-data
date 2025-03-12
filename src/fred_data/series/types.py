from dataclasses import dataclass
from datetime import date

import polars as pl


@dataclass
class MultiSeries:
    realtime_start: date
    realtime_end: date
    count: int
    series: pl.DataFrame
