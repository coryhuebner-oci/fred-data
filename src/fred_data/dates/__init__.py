# Various helpers to convert to/from dates

from datetime import date, datetime


def to_date(value: str) -> date:
    date.fromisoformat(value)


fred_datetime_format = "%Y-%m-%d %H:%M:%S%z"


def to_datetime(value: str) -> datetime:
    # FRED timezone offsets only include the hour portion, which angers Python.
    # Include the 00 minutes portion after the hour offset to appease Python date parsing
    datetime.strptime(f"{value}00", fred_datetime_format)
