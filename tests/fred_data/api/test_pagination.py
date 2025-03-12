from fred_data.api import has_all_data_been_loaded
from tests.fred_data.testing_utilities import create_http_json_response


def _create_test_response(total_item_count: int, limit: int, offset: int):
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
            "release_dates": [
                {
                    "release_id": 86,
                    "release_name": "Commercial Paper",
                    "release_last_updated": "2025-03-11 12:02:04-05",
                    "date": "2025-03-13",
                },
            ],
        }
    )


def test_has_all_data_been_loaded_false_when_more_data_remains():
    response = _create_test_response(1000, 10, 0)
    assert has_all_data_been_loaded(response) == False


def test_has_all_data_been_loaded_true_when_on_last_page_full_of_data():
    response = _create_test_response(1000, 5, 199)
    assert has_all_data_been_loaded(response) == True


def test_has_all_data_been_loaded_true_when_on_last_partial_page():
    response = _create_test_response(1000, 150, 6)
    assert has_all_data_been_loaded(response) == True
