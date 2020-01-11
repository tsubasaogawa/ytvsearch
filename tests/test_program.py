import pytest

from ytvsearch import Program


@pytest.fixture()
def program():
    return Program()


def test_program(program):
    assert type(program.date) is str
    assert type(program.time) is str
    assert type(program.is_on_air) is bool
    assert type(program.title) is str
    assert type(program.is_repeated) is bool
    assert type(program.channel) is str
    assert type(program.genre) is dict
    assert type(program.description) is str
    assert type(program.impression_num) is int
    assert type(program.evaluation) is dict
    assert type(program.mitai_num) is int
