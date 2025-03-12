from typing import Any
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

    paginated_fetch_count = int(response_json["limit"]) * int(
        response_json["offset"] + 1
    )
    total_item_count = int(response_json["count"])
    return paginated_fetch_count >= total_item_count
