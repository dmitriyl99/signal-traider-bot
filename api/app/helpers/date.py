from datetime import datetime
from dateutil import relativedelta

import time


def diff_in_month(d1: datetime, d2: datetime) -> int:
    delta = relativedelta.relativedelta(d1, d2)
    return delta.months


def diff_in_days(d1: datetime, d2: datetime) -> int:
    delta = d1-d2
    return abs(delta.days)


def timestamp2seconds(timestamp):
    # is it already in seconds
    if len(str(timestamp)) == 10:
        return timestamp
    return timestamp // 1000


def timestamp2datetime(timestamp):
    # if in milliseconds, convert to seconds
    if len(str(timestamp)) == 13:
        timestamp = timestamp2seconds(timestamp)

    # convert to datetime string
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


def datetime2timestamp(datetime_str):
    if datetime_str:
        return int(time.mktime(time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')) * 1000)
    return datetime_str
