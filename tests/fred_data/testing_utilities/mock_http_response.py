import io
import json
from typing import Any
from urllib3 import HTTPResponse


def create_http_json_response(
    body: Any,
    *,
    status_code: int = 200,
    response_headers: dict[str, str] = {},
    request_method: str = "GET",
) -> HTTPResponse:
    """Create a JSON response emulating the response of an HTTP request"""
    body = json.dumps(body).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
        **response_headers,
    }

    return HTTPResponse(
        body=io.BytesIO(body),
        headers=headers,
        status=status_code,
        version=1.1,
        preload_content=False,
        request_method=request_method,
    )
