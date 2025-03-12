import pytest

from datetime import date, datetime, timedelta
from typing import TypedDict
from fred_data.api import has_all_data_been_loaded, count_items_in_field
from tests.fred_data.testing_utilities import create_http_json_response


class ReleaseDate(TypedDict):
    release_id: int
    release_name: str
    release_last_updated: str
    date: str


def _create_release_date(
    release_id: int, release_name: str, release_last_updated: datetime, date: date
) -> ReleaseDate:
    """For these tests, we're using 'release_dates' as our items collection.
    The pagination module accepts other field types, but just arbitrarily choosing that for tests
    """
    return {
        "release_id": release_id,
        "release_name": release_name,
        "release_last_updated": release_last_updated.strftime("%Y-%m-%d %H:%M:%S%z"),
        "date": date.isoformat(),
    }


def _create_test_response(
    total_item_count: int,
    limit: int,
    offset: int,
    release_dates: list[ReleaseDate] = [],
):
    """Create a dummy response including standard FRED pagination fields along with extra data to
    ensure no unexpected impact of that additional data"""
    return create_http_json_response(
        {
            "realtime_start": "2024-03-12",
            "realtime_end": "2025-03-13",
            "order_by": "release_date",
            "sort_order": "desc",
            "count": total_item_count,
            "limit": limit,
            "offset": offset,
            "release_dates": release_dates,
        }
    )


def test_has_all_data_been_loaded_false_when_no_data_fetched_yet():
    response = _create_test_response(1000, 10, 0)
    assert has_all_data_been_loaded(response) == False


def test_has_all_data_been_loaded_false_when_more_data_remains():
    response = _create_test_response(1000, 10, 50)
    assert has_all_data_been_loaded(response) == False


def test_has_all_data_been_loaded_true_when_on_last_page_full_of_data():
    response = _create_test_response(1000, 5, 1000)
    assert has_all_data_been_loaded(response) == True


def test_has_all_data_been_loaded_true_when_over_total_count():
    response = _create_test_response(1000, 150, 1001)
    assert has_all_data_been_loaded(response) == True


def test_count_items_in_field_empty_field():
    response = _create_test_response(1000, 50, 0, [])
    assert count_items_in_field(response, "release_dates") == 0


def test_count_items_in_field_with_items():
    release1 = _create_release_date(
        123, "blarp", datetime.now() - timedelta(days=1), datetime.now()
    )
    release2 = _create_release_date(
        123, "blarp", datetime.now() - timedelta(days=2), datetime.now()
    )
    release3 = _create_release_date(
        123,
        "blarp",
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(seconds=10),
    )
    release4 = _create_release_date(
        321, "carp", datetime.now() - timedelta(days=1), datetime.now()
    )
    response = _create_test_response(
        1000,
        50,
        0,
        [
            release1,
            release2,
            release3,
            release4,
        ],
    )
    assert count_items_in_field(response, "release_dates") == 4


def test_count_items_in_field_with_field_not_found():
    release1 = _create_release_date(
        123, "blarp", datetime.now() - timedelta(days=1), datetime.now()
    )
    release2 = _create_release_date(
        123, "blarp", datetime.now() - timedelta(days=2), datetime.now()
    )
    release3 = _create_release_date(
        123,
        "blarp",
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(seconds=10),
    )
    release4 = _create_release_date(
        321, "carp", datetime.now() - timedelta(days=1), datetime.now()
    )
    response = _create_test_response(
        1000,
        50,
        0,
        [
            release1,
            release2,
            release3,
            release4,
        ],
    )
    with pytest.raises(KeyError) as excinfo:
        count_items_in_field(response, "kaplow")
    assert "Field not found in response: kaplow" in str(excinfo)
