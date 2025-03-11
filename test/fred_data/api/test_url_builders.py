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
    "input",
    [
        ("https://wombatsinbusinesssuits.com?file_type=xml"),
        ("https://wombatsinbusinesssuits.com/?file_type=json"),
        (
            "https://wombatsinbusinesssuits.com?now=withqs&file_type=json&params=exclamationpoint"
        ),
    ],
)
def get_url_leaves_complete_urls_untouched(input, monkey_patch_env):
    monkey_patch_env(_api_key_env_var)
    assert get_url(input) == input


@pytest.mark.parametrize(
    "input, output",
    [
        (
            "https://wombatsinbusinesssuits.com?api_key=<apiKey>&file_type=json",
            f"https://wombatsinbusinesssuits.com?api_key={_api_key}&file_type=json",
        ),
        (
            "https://wombatsinbusinesssuits.com/?api_key=<apiKey>&file_type=xml",
            f"https://wombatsinbusinesssuits.com/?api_key={_api_key}&file_type=xml",
        ),
        (
            "https://wombatsinbusinesssuits.com?now=withqs&api_key=<apiKey>&file_type=json&params=exclamationpoint",
            f"https://wombatsinbusinesssuits.com?now=withqs&api_key={_api_key}&file_type=json&params=exclamationpoint",
        ),
    ],
)
def test_get_url_replaces_api_key(input, output, monkey_patch_env):
    monkey_patch_env(_api_key_env_var)
    assert get_url(input) == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
            "https://wombatsinbusinesssuits.com?api_key=<apiKey>",
            f"https://wombatsinbusinesssuits.com?api_key={_api_key}&file_type=json",
        ),
        (
            "https://wombatsinbusinesssuits.com/?api_key=<apiKey>",
            f"https://wombatsinbusinesssuits.com/?api_key={_api_key}&file_type=json",
        ),
        (
            "https://wombatsinbusinesssuits.com?now=withqs&api_key=<apiKey>&params=exclamationpoint",
            f"https://wombatsinbusinesssuits.com?now=withqs&api_key={_api_key}&params=exclamationpoint&file_type=json",
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
            "fred/releases?api_key=<apiKey>&file_type=json",
            f"https://api.stlouisfed.org/fred/releases?api_key={_api_key}&file_type=json",
        ),
        (
            "fred/categories?api_key=<apiKey>&file_type=xml",
            f"https://api.stlouisfed.org/fred/categories?api_key={_api_key}&file_type=xml",
        ),
    ],
)
def test_get_url_prefixes_relative_paths_with_base_fred_url(
    input, output, monkey_patch_env
):
    monkey_patch_env(_api_key_env_var)
    assert get_url(input) == output
