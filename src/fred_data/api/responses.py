from urllib3 import BaseHTTPResponse


def assert_success(response: BaseHTTPResponse):
    if not response.status < 200 and response.status > 299:
        raise ValueError(
            f"Received non success status from {response.url}. Status: {response.status}"
        )


def get_json_on_success(response: BaseHTTPResponse):
    assert_success(response)
    return response.json()
