from datetime import date, datetime
from functools import reduce
from os import path
from urllib.parse import quote_plus

from fred_data.config import Config

QueryStringValue = str | int | date | datetime | bool | None


def _stringify_query_string_value(value: QueryStringValue) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime) or isinstance(value, date):
        return value.isoformat()
    return str(value)


def _join_to_single_query_string_value(
    url: str, key: str, value: QueryStringValue | None
) -> str:
    """Join the given key/value pair to the query string of the given url. This method takes
    into account whether a '?' or '&' delimeter should be used"""
    if value is None:
        return url
    delimeter = "&" if "?" in url else "?"
    stringified_value = _stringify_query_string_value(value)
    return f"{url}{delimeter}{quote_plus(key)}={quote_plus(stringified_value)}"


def _get_default_query_string_params() -> dict[str, str]:
    return {"api_key": Config.fred_api_key(), "file_type": "json"}


def _query_string_reducer(
    url: str, key_value_pair: tuple[str, QueryStringValue | None]
) -> str:
    key, value = key_value_pair
    return _join_to_single_query_string_value(url, key, value)


def _join_to_query_string(
    url: str, query_string_params: dict[str, QueryStringValue | None]
) -> str:
    """Join all provided query string parameters to the existing url"""
    return reduce(_query_string_reducer, query_string_params.items(), url)


def get_url(
    url: str, query_string_params: dict[str, QueryStringValue | None] = {}
) -> str:
    """Get the transformed url with:
    1. The API key placeholder replaced by the actual API key
    2. The file type query string parameter defaulted to json if no file_type provided
    3. If the 'url' is actually a relative path, prefix the configured FRED API URL"""
    absolute_url = (
        url if url.startswith("http") else path.join(Config.fred_api_url(), url)
    )
    query_string_with_defaults = {
        **_get_default_query_string_params(),
        **query_string_params,
    }
    transformed_url = _join_to_query_string(absolute_url, query_string_with_defaults)
    return (
        transformed_url
        if transformed_url.startswith("http")
        else path.join(Config.fred_api_url(), transformed_url)
    )
