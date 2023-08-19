import pytest
import pytz

from utils.datetime import get_now_utc_datetime


def test_get_now_utc_datetime_default():
    dt = get_now_utc_datetime()
    assert dt.tzinfo == pytz.UTC


# def test_get_now_utc_datetime_with_timezone():
#     timezone_str = "Asia/Tokyo"
#     dt = get_now_utc_datetime(timezone=timezone_str)
#     assert dt.tzinfo == pytz.timezone(timezone_str)


def test_get_now_utc_datetime_invalid_timezone():
    with pytest.raises(pytz.UnknownTimeZoneError):
        get_now_utc_datetime(timezone="InvalidTimeZone")
