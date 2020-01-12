import pytest

from datetime import datetime
from ytvsearch import ydatetime


@pytest.mark.parametrize('ydate, ytime, tzinfo', [
    ('1/1（水）', '0:00～1:00', None),
    ('1/1', '0:00～1:00', None),
    ('1/1（水）', '0:00 ～ 1:00', None),
    ('1/12（日）', '0:00～1:00', None),
    ('10/1（木）', '0:00～1:00', None),
    ('10/12（月）', '0:00～1:00', None),
    ('1/1（水）', '9:00～10:00', None),
    ('1/1（水）', '23:00～24:00', None),
    ('1/1（水）', '11:00～11:59', None),
])
def test_convert_to_datetimes_pass(ydate, ytime, tzinfo):
    now = datetime.now(tz=tzinfo)
    results = ydatetime.convert_to_datetimes(ydate, ytime, tz=tzinfo)
    assert type(results) is list
    for _datetime in results:
        assert type(_datetime) is datetime
        assert _datetime.year == now.year
    assert results[0].year == results[1].year
    assert results[0].month == results[1].month
    assert results[0].second == results[1].second
    assert results[0].tzinfo == results[1].tzinfo


def test_convert_to_datetimes_returns_are_valid():
    results = ydatetime.convert_to_datetimes('1/1（水）', '23:00～28:30')
    assert results[0].day == 1
    assert results[1].day == 2
    assert results[0].hour == 23
    assert results[1].hour == (28 - 24)
    assert results[0].minute == 0
    assert results[1].minute == 30
    assert (results[1] - results[0]).seconds == (28 - 23) * 60 * 60 + 30 * 60


@pytest.mark.parametrize('ydate, ytime', [
    ('', '4:10～4:13'),
    ('1/12（日）', ''),
])
def test_convert_to_datetimes_raise_when_arg_is_no_given(ydate, ytime):
    with pytest.raises(ValueError):
        ydatetime.convert_to_datetimes(ydate, ytime)


@pytest.mark.parametrize('ydate, ytime', [
    ('111/1（水）', '0:00～1:00'),
    ('1/111（水）', '0:00～1:00'),
    ('1/111(水)', '0:00～1:00'),
    ('1/1（水）', '000:0～1:00'),
    ('1/1（水）', '0:001:00'),
])
def test_convert_to_datetimes_raise_when_arg_is_invalid(ydate, ytime):
    with pytest.raises(ValueError):
        ydatetime.convert_to_datetimes(ydate, ytime)
