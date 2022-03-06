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


def test_replace():
    o = One()
    o2 = o.replace(one='seven', three={'nine': 9})
    assert o2 == One('seven', 2, {'nine': 9})


def test_frozen():
    o = One()
    try:
        o.one = 'three'
    except AttributeError:
        pass
    else:
        raise AttributeError('Was mutable!')

    om = OneMutable()
    om.one = 'three'
    assert str(om) == "OneMutable(one='three', two=2, three={})"


@dataclass
class Overloads:
    one: str = 'one'
    asdict: int = 1
    astuple: int = 1
    fields: int = 1
    replace: int = 1


def test_overloads():
    ov = Overloads()
    assert ov.one == 'one'
    assert ov.asdict == 1
    assert ov.astuple == 1
    assert ov.fields == 1
    assert ov.replace == 1

    d = {'asdict': 1, 'astuple': 1, 'fields': 1, 'one': 'one', 'replace': 1}
    assert dataclass.asdict(ov) == d
    assert dataclass.astuple(ov) == ('one', 1, 1, 1, 1)
