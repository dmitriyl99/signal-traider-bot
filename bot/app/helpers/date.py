from datetime import datetime


def diff_in_days(d1: datetime, d2: datetime) -> int:
    delta = d1 - d2
    return abs(delta.days)
