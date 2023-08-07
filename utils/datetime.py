from datetime import datetime
from typing import Optional

import pytz


def get_now_utc_datetime(timezone: Optional[str] = None) -> datetime:
    if timezone is None:
        timezone = "UTC"
    return datetime.now(tz=pytz.timezone(timezone))
