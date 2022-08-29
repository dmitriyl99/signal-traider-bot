from datetime import datetime
from dateutil import relativedelta


def diff_in_month(d1: datetime, d2: datetime) -> int:
    delta = relativedelta.relativedelta(d1, d2)
    return delta.months


def diff_in_days(d1: datetime, d2: datetime) -> int:
    delta = d1-d2
    return abs(delta.days)
