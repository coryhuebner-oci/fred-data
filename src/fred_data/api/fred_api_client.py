from collections.abc import Callable, Generator
from urllib3 import BaseHTTPResponse, PoolManager

from fred_data.api.pagination import get_expected_item_count
from fred_data.api.pagination_tracker import PaginationTracker
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

    def get_all_pages(
        self,
        url: str,
        current_page_items_counter: Callable[[BaseHTTPResponse], int],
        *,
        query_string_params: dict[str, str] = {},
        maximum_offset_allowed: int = 25_000,  # Safety net to avoid infinite looping
        **kwargs,
    ) -> Generator[BaseHTTPResponse, None, None]:
        """A helper to loop through pages of an API route until there are no remaining pages. This is a generator
        that yields the latest fetch page back to the caller as it loops"""
        pagination_tracker: PaginationTracker | None = None
        while pagination_tracker is None or pagination_tracker.more_pages_to_read:
            previous_offset = (
                pagination_tracker.current_offset if pagination_tracker else 0
            )
            if previous_offset > maximum_offset_allowed:
                raise OverflowError(
                    f"The maximum offset of {maximum_offset_allowed} was exceeded calling {url}"
                )
            query_string_with_offset = {
                **query_string_params,
                "offset": previous_offset,
            }
            last_response = self.get(url, query_string_with_offset, **kwargs)
            yield last_response

            pagination_tracker = PaginationTracker(
                current_offset=previous_offset
                + current_page_items_counter(last_response),
                expected_item_count=get_expected_item_count(last_response),
            )
