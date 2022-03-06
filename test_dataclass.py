import dataclass
from typing import Dict


@dataclass
class One:
    one: str = 'one'
    two: int = 2
    three: Dict = dataclass.field(dict)


@dataclass(frozen=False)
class OneMutable:
    one: str = 'one'
    two: int = 2
    three: Dict = dataclass.field(dict)


def test_dataclass():
    o = One()
    assert o.asdict() == {'one': 'one', 'two': 2, 'three': {}}
    assert o.astuple() == ('one', 2, {})

    assert [f.name for f in One.fields()] == ['one', 'two', 'three']


def test_frozen():
    o = One()
    try:
        o.one = 'three'
    except AttributeError:
        pass
    else:
        raise AttributeError('Was mutable!')


def test_mutable():
    om = OneMutable()
    om.one = 'three'
    assert str(om) == "OneMutable(one='three', two=2, three={})"
