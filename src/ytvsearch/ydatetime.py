import datetime
from datetime import timedelta, timezone, tzinfo
import re


REGEXES = {
    'date': r'^(\d{1,2})\/(\d{1,2})',
    'time': r'^(\d{1,2}):(\d{1,2})[^\d]+(\d{1,2}):(\d{1,2})$',
}
DEFAULT_TIMEDELTA = 9


def convert_to_datetimes(
    ydate: str,
    ytime: str,
    tz: tzinfo = timezone(timedelta(hours=DEFAULT_TIMEDELTA))
) -> list:
    if not ydate or not ytime:
        raise ValueError('ydate and ytime are required')

    _date = _str2date(ydate, tz)
    _deltas = _str2timedeltas(ytime)

    return [
        datetime.datetime(
            _date.year,
            _date.month,
            _date.day,
            tzinfo=tz
        ) + _deltas[0],
        datetime.datetime(
            _date.year,
            _date.month,
            _date.day,
            tzinfo=tz
        ) + _deltas[1],
    ]


def _str2date(ydate: str, tz: tzinfo) -> datetime.date:
    year = datetime.datetime.now(tz=tz).year
    matches = re.match(REGEXES['date'], ydate).groups()
    month, day = int(matches[0]), int(matches[1])

    return datetime.date(year, month, day)


def _str2timedeltas(ytime: str) -> list:
    matches = re.match(REGEXES['time'], ytime).groups()
    start = {'hour': int(matches[0]), 'minute': int(matches[1])}
    end = start if len(matches) != 4 else {
        'hour': int(matches[2]), 'minute': int(matches[3])
    }

    return [
        timedelta(hours=start['hour'], minutes=start['minute']),
        timedelta(hours=end['hour'], minutes=end['minute']),
    ]
