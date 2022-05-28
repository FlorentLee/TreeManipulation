from datetime import datetime as dt
from datetime import timedelta
import time


def toDateTime(date):
    if len(date) == 10:
        date += " 12:00:00"
    elif len(date) == 7:
        date += "-01 12:00:00"
    elif len(date) == 4:
        date += "-01-01 12:00:00"
    return dt.strptime(date, '%Y-%m-%d %H:%M:%S')


def toDateDecimal(date):
    def sinceEpoch(date):
        # return seconds since epoch
        return time.mktime(date.timetuple())

    s = sinceEpoch

    year = date.year
    startOfThisYear = dt(year=year, month=1, day=1)
    startOfNextYear = dt(year=year + 1, month=1, day=1)

    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed / yearDuration

    return date.year + fraction


def decimalToTimeStamp(decimal):
    year = int(decimal)
    rem = decimal - year
    base = dt(year, 1, 1)
    result = base + timedelta(seconds=(base.replace(year=base.year + 1) - base).total_seconds() * rem)
    return str(result)
