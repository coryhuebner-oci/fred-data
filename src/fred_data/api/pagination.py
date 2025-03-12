from typing import Any, Callable
from urllib3 import BaseHTTPResponse

from fred_data.api.responses import get_json_on_success

_count_field = "count"
_limit_field = "limit"
_offset_field = "offset"


def _find_missing_fields(response_json: Any) -> list[str]:
    return [
        field
        for field in [_count_field, _limit_field, _offset_field]
        if field not in response_json
    ]


def has_all_data_been_loaded(response: BaseHTTPResponse) -> bool:
    """Determine if all data has been loaded for a paginated resource in the FRED API"""
    response_json = get_json_on_success(response)
    missing_fields = _find_missing_fields(response_json)
    if missing_fields:
        raise KeyError(
            f"The following field(s) were not found in the response; pagination check cannot occur without them: {",".join(missing_fields)}"
        )

    paginated_fetch_count = int(response_json["offset"])
    total_item_count = int(response_json["count"])
    return paginated_fetch_count >= total_item_count


def get_offset(response: BaseHTTPResponse) -> int:
    return int(response.json()[_offset_field])


def get_expected_item_count(response: BaseHTTPResponse) -> int:
    return int(response.json()[_count_field])


def count_items_in_field(response: BaseHTTPResponse, field_name: str) -> int:
    """Get a count of all items in the given field of the HTTP response (assumes response is JSON)"""
    response_json = response.json()
    if field_name not in response_json:
        raise KeyError(f"Field not found in response: {field_name}")
    return len(response_json[field_name])


def get_item_counter(field_name: str) -> Callable[[BaseHTTPResponse], int]:
    """Get an item counter capable of counting the items in the given field from the JSON HTTP response"""

    def item_counter(response: BaseHTTPResponse):
        return count_items_in_field(response, field_name)

    return item_counter
