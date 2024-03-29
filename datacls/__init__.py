"""
# 🗂 `datacls`: take the edge off `dataclass` 🗂

`dataclasses` is almost perfect.

`datacls` is a tiny, thin wrapper around `dataclass.dataclasses` making it
a bit more self-contained, reflective, and saving a bit of typing.

`datacls` is exactly like `dataclass`, except:

  * Adds three new instance methods: `asdict()`, `astuple()`, `replace()`,
    and one new class method, `fields()`, all taken from the `dataclasses`
    module

  * `xmod`-ed for less cruft (so `datacls` is the same as `datacls.dataclass`)

  * The default class is `datacls.immutable` where `frozen=True`.

## Example

    import datacls

    @datacls
    class One:
        one: str = 'one'
        two: int = 2
        three: dict = datacls.field(dict)

    # `One` has three instance methods: asdict(), astuple(), replace()

    o = One()
    assert o.asdict() == {'one': 'one', 'two': 2, 'three': {}}

    import dataclasses
    assert dataclasses.asdict(o) == o.asdict()

    assert o.astuple() == ('one', 2, {})

    o2 = o.replace(one='seven', three={'nine': 9})
    assert o2 == One('seven', 2, {'nine': 9})

    # `One` has one new class method: fields()

    assert [f.name for f in One.fields()] == ['one', 'two', 'three']

    # @datacls is immutable.

    try:
        o.one = 'three'
    except AttributeError:
        pass
    else:
        raise AttributeError('Was mutable!')

    # Usec @datacls.mutable or @datacls(frozen=False)
    # for mutable classes

    @datacls.mutable
    class OneMutable:
        one: str = 'one'
        two: int = 2
        three: Dict = datacls.field(dict)

    om = OneMutable()
    om.one = 'three'
    assert str(om) == "OneMutable(one='three', two=2, three={})"

    # These four new methods won't break your old dataclass by mistake:
    @datacls
    class Overloads:
        one: str = 'one'
        asdict: int = 1
        astuple: int = 1
        fields: int = 1
        replace: int = 1

    o = Overloads()

    assert ov.one == 'one'
    assert ov.asdict == 1
    assert ov.astuple == 1
    assert ov.fields == 1
    assert ov.replace == 1

    # You can still access the methods as functions on `datacls`:
    assert (
        datacls.asdict(ov) ==
        {'asdict': 1, 'astuple': 1, 'fields': 1, 'one': 'one', 'replace': 1}
    )
"""

import dataclasses as dc
from dataclasses import (
    MISSING,
    asdict,
    astuple,
    dataclass,
    fields,
    replace,
)
from functools import cached_property, partial, wraps

import xmod

__all__ = (
    'add_methods',
    'asdict',
    'astuple',
    'cached_property',
    'dtyper',
    'field',
    'fields',
    'hidden',
    'immutable',
    'make_dataclass',
    'mutable',
    'replace',
)

_METHODS = 'asdict', 'astuple', 'fields', 'replace'
_CLASS_METHODS = {'field_names', 'fields'}
_NONE = object()
_DEFAULTS = 'default', 'default_factory'
_DFLT_ERR = 'Just one of default, default_factory and default_value may be set'


@wraps(dataclass)
def mutable(cls=None, **kwargs):
    if not cls:
        return partial(mutable, **kwargs)

    return add_methods(dataclass(cls, **kwargs))


@wraps(dc.field)
def field(default_factory=MISSING, **kwargs):
    return dc.field(default_factory=default_factory, **kwargs)


def add_methods(dcls):
    """Adds dataclasses functions as methods to a dataclass.

    Adds three new instance methods: `asdict()`, `astuple()`, `replace()`
    and one new class method, `fields()`
    """
    methods = (m for m in _METHODS if not hasattr(dcls, m))
    for m in methods:
        method = globals()[m]
        if m in _CLASS_METHODS:
            method = classmethod(method)
        setattr(dcls, m, method)
    return dcls


@wraps(dc.make_dataclass)
def make_dataclass(*a, **ka):
    return add_methods(dc.make_dataclass(*a, **ka))


hidden = partial(field, compare=False, init=False, repr=False)
immutable = partial(mutable, frozen=True)
dtyper = None


class Datacls:
    __call__ = staticmethod(immutable)

    @cached_property
    def dtyper(self):
        import dtyper

        return dtyper.dataclass


xmod.xmod(Datacls(), 'datacls')
