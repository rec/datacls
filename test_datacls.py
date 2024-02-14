from typing import Dict

import datacls


@datacls
class One:
    one: str = 'one'
    two: int = 2
    three: Dict = datacls.field(dict)


@datacls(frozen=False)
class OneMutable:
    one: str = 'one'
    two: int = 2
    three: Dict = datacls.field(dict)


def test_datacls():
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


@datacls
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
    assert datacls.asdict(ov) == d
    assert datacls.astuple(ov) == ('one', 1, 1, 1, 1)


@datacls
class Hidden:
    one: str = 'one'
    two: str = datacls.hidden()
    three: str = datacls.hidden()

    def __post_init__(self):
        super().__setattr__('two', self.one + self.one)
        super().__setattr__('three', self.two + self.one)


def test_hidden():
    assert str(Hidden()) == "Hidden(one='one')"

    g, h = Hidden(), Hidden()
    assert g.two == h.two
    assert g == h
    assert hash(g) == hash(h)

    object.__setattr__(h, 'two', 'ninety nine')
    assert g.two != h.two
    assert g == h
    assert hash(g) == hash(h)

    object.__setattr__(h, 'three', 'ninety nine')
    assert g.three != h.three
    assert g == h
    assert hash(g) == hash(h)

    try:
        Hidden(two='two')
    except TypeError:
        pass
    else:
        raise ValueError
    try:
        Hidden('1', 'two')
    except TypeError:
        pass
    else:
        raise ValueError


@datacls
class Default:
    one: str = datacls.field(default='one')


def test_default():
    assert Default().one == 'one'


def test_make_dataclass():
    # https://docs.python.org/3/library/dataclasses.html
    #    #dataclasses.make_dataclass
    C = datacls.make_dataclass(
        'C',
        [('x', int), 'y', ('z', int, datacls.field(default=5))],
        namespace={'add_one': lambda self: self.x + 1},
    )

    assert sorted(c.name for c in C.fields()) == ['x', 'y', 'z']
