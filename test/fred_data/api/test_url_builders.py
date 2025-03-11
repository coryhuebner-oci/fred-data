from datetime import date
import pytest


from src.fred_data.api import get_url

_api_key = "this-here-is-my-secret"
_api_key_env_var = {"FRED_API_KEY": _api_key}


@pytest.fixture(scope="function")
def monkey_patch_env(monkeypatch):
    def _patch_env(values: dict[str, str]):
        for key, value in values.items():
            monkeypatch.setenv(key, value)

    return _patch_env


@pytest.mark.parametrize(
    "input, output",
    [
        (
            "https://wombatsinbusinesssuits.com",
            f"https://wombatsinbusinesssuits.com?api_key={_api_key}&file_type=json",
        ),
        (
            "https://wombatsinbusinesssuits.com/",
            f"https://wombatsinbusinesssuits.com/?api_key={_api_key}&file_type=json",
        ),
    ],
)
def test_get_url_sets_api_key(input, output, monkey_patch_env):
    monkey_patch_env(_api_key_env_var)
    assert get_url(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
            "https://wombatsinbusinesssuits.com",
            f"https://wombatsinbusinesssuits.com?api_key={_api_key}&file_type=json",
        ),
        (
            "https://wombatsinbusinesssuits.com/",
            f"https://wombatsinbusinesssuits.com/?api_key={_api_key}&file_type=json",
        ),
    ],
)
def test_get_url_defaults_file_type(input, output, monkey_patch_env):
    monkey_patch_env(_api_key_env_var)
    assert get_url(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
            "fred/releases",
            f"https://api.stlouisfed.org/fred/releases?api_key={_api_key}&file_type=json",
        ),
        (
            "fred/categories",
            f"https://api.stlouisfed.org/fred/categories?api_key={_api_key}&file_type=json",
        ),
    ],
)
def test_get_url_prefixes_relative_paths_with_base_fred_url(
    input, output, monkey_patch_env
):
    monkey_patch_env(_api_key_env_var)
    assert get_url(input) == output


def test_get_url_with_specific_query_string_parameters():
    starting_url = "https://chowdertime.gov"
    result = get_url(
        starting_url,
        {
            "im": "a lonely parameter",
            "api_key": "override!",
            "numeric": 123,
            "date": date(2024, 2, 28),
            "empty": None,  # Empty should get filtered out
        },
    )
    assert (
        result
        == "https://chowdertime.gov?api_key=override%21&file_type=json&im=a+lonely+parameter&numeric=123&date=2024-02-28"
    )
