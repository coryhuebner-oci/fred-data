# A package containing modules for interacting with series data from FRED

from fred_data.series.search import get_search_results
from fred_data.series.per_release import get_series_for_release
from fred_data.series.by_id import get_series_by_id

__all__ = [
    get_search_results.__name__,
    get_series_for_release.__name__,
    get_series_by_id.__name__,
]
