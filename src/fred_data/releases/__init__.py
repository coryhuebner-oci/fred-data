from dataclasses import dataclass
from datetime import date

from fred_data.api.fred_api_client import FredApiClient


@dataclass
class Releases:
    realtime_start: date
    realtime_end: date
    count: int


def get_releases(
    api_client: FredApiClient,
    realtime_start: date | None,
    realtime_end: date | None,
    page_size: int | None,
    offset: int | None,
):
    """Get all releases matching the given filter criteria"""
