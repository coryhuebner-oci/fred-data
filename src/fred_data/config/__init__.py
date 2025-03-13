# A package containing for getting configuration values

from os import getenv


def get_required(environment_variable: str) -> str:
    config_value = getenv(environment_variable)
    if not config_value:
        raise KeyError(
            f"A value must be provided for the {environment_variable} variable"
        )
    return config_value


class Config:
    """Configuration for the FRED API application"""

    @staticmethod
    def fred_api_key():
        return get_required("FRED_API_KEY")

    @staticmethod
    def fred_api_url():
        return getenv("FRED_API_URL", "https://api.stlouisfed.org")
