from urllib3 import BaseHTTPResponse, PoolManager

from fred_data.api.url_builders import get_url


class FredApiClient:
    _pool_manager: PoolManager

    def __init__(self):
        self._pool_manager = PoolManager()

    def get(
        self, url: str, query_string_params: dict[str, str] = {}, **kwargs
    ) -> BaseHTTPResponse:
        """Run a "GET" against the provided url.
        1. The API key placeholder will be replaced in the query string with the actual api key
        2. If the url is relative, prefix with the FRED API base url to convert into an absolute url
        """
        transformed_url: str = get_url(url, query_string_params)
        return self._pool_manager.request("GET", transformed_url, **kwargs)
