from os import path
import re
from fred_data.config import Config

api_key_placeholder = "<apiKey>"


def _replace_api_key(url: str) -> str:
    """Replace the API key placeholder with the actual API key value"""
    return url.replace(api_key_placeholder, Config.fred_api_key())


def _join_to_query_string(url: str, key: str, value: str) -> str:
    """Join the given key/value pair to the query string of the given url. This method takes
    into account whether a '?' or '&' delimeter should be used"""
    delimeter = "&" if "?" in url else "?"
    return f"{url}{delimeter}{key}={value}"


def _with_defaulted_file_type(url: str) -> str:
    """Default the file_type query string parameter if one wasn't provided"""
    return (
        url
        if re.search(r"file_type=\w+", url)
        else _join_to_query_string(url, "file_type", "json")
    )


def get_url(url: str) -> str:
    """Get the transformed url with:
    1. The API key placeholder replaced by the actual API key
    2. The file type query string parameter defaulted to json if no file_type provided
    3. If the 'url' is actually a relative path, prefix the configured FRED API URL"""
    transformed_url: str = _with_defaulted_file_type(_replace_api_key(url))
    return (
        transformed_url
        if transformed_url.startswith("http")
        else path.join(Config.fred_api_url(), transformed_url)
    )
