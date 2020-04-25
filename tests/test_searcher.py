import pytest

import time

from ytvsearch import Searcher
from ytvsearch import SearchOption


SLEEP_SEC = 1


@pytest.fixture()
def searcher():
    time.sleep(SLEEP_SEC)
    return Searcher()


@pytest.mark.parametrize('kw, broad, pref, oa, limit', [
    ('Baseball', [SearchOption.Broadcast.TERRESTRIAL], SearchOption.Prefecture.SAPPORO, 1, 0),
    ('Baseball', [
        SearchOption.Broadcast.TERRESTRIAL,
        SearchOption.Broadcast.BS,
        SearchOption.Broadcast.CS
    ], SearchOption.Prefecture.SAPPORO, 1, 10),
    ('Baseball', [SearchOption.Broadcast.TERRESTRIAL], SearchOption.Prefecture.SAPPORO, 0, 10),
])
def test_run_success(searcher, kw, broad, pref, oa, limit):
    programs = searcher.run(
        keyword=kw,
        broad_types=broad,
        prefecture=pref,
        oa=oa,
        fetch_limit=limit
    )

    assert type(programs) is list
    for program in programs:
        assert type(program.date) is dict
        assert program.date['start'] <= program.date['end']
        assert type(program.is_on_air) is bool
        assert program.title != ''
        assert type(program.is_repeated) is bool
        assert program.channel != ''
        assert type(program.genre) is dict
        assert 'parent' in program.genre
        assert 'child' in program.genre
        assert program.description != ''
        assert program.impression_num >= 0
        assert type(program.evaluation) is dict
        assert 0.0 <= program.evaluation['average_pts'] and program.evaluation['average_pts'] <= 5.0
        assert program.evaluation['total_num_vote'] >= 0
        assert program.mitai_num >= 0


@pytest.mark.parametrize('kw, broad, pref, oa', [
    ('', [SearchOption.Broadcast.TERRESTRIAL], SearchOption.Prefecture.SAPPORO, 1),
])
def test_run_raise_with_no_keyword(searcher, kw, broad, pref, oa):
    with pytest.raises(RuntimeError):
        searcher.run(
            keyword=kw,
            broad_types=broad,
            prefecture=pref,
            oa=oa,
            fetch_limit=0
        )


@pytest.mark.parametrize('kw, broad, pref, oa', [
    ('Baseball', SearchOption.Broadcast.TERRESTRIAL, SearchOption.Prefecture.SAPPORO, 1),
    ('Baseball', 1, SearchOption.Prefecture.SAPPORO, 1),
    ('Baseball', [SearchOption.Broadcast.TERRESTRIAL], 1, 1),
])
def test_run_raise_with_bad_type_of_argument(searcher, kw, broad, pref, oa):
    with pytest.raises(TypeError):
        searcher.run(
            keyword=kw,
            broad_types=broad,
            prefecture=pref,
            oa=oa,
            fetch_limit=0
        )
