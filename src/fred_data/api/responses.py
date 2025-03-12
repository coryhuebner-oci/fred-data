from urllib3 import BaseHTTPResponse


def _get_error_message(response: BaseHTTPResponse) -> str:
    """Get the error message from a response by:
    1. Attempting to extract it from the JSON response body (if applicable)
    2. Return a standard url/status failure message if JSON message parsing is not applicable
    """
    if response.headers.get("content-type").startswith("application/json"):
        parsed_json = response.json()
        if "error_message" in parsed_json:
            return parsed_json["error_message"]

    return f"Received non success status from {response.url}. Status: {response.status}"


def assert_success(response: BaseHTTPResponse):
    if not response.status < 200 and response.status > 299:
        raise ValueError(_get_error_message(response))


def get_json_on_success(response: BaseHTTPResponse):
    assert_success(response)
    return response.json()
