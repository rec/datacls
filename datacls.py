from dataclasses import (
    MISSING,
    asdict,
    astuple,
    dataclass,
    field as _field,
    fields,
    make_dataclass,
    replace,
)
import functools
import xmod

__all__ = (
    'add_methods',
    'asdict',
    'astuple',
    'field',
    'fields',
    'hidden',
    'immutable',
    'make_dataclass',
    'mutable',
    'replace',
)
__version__ = '4.2.1'

_METHODS = 'asdict', 'astuple', 'fields', 'replace'
_CLASS_METHODS = {'field_names', 'fields'}
_NONE = object()
_DEFAULTS = 'default', 'default_factory'
_DFLT_ERR = 'Just one of default, default_factory and default_value may be set'


@functools.wraps(dataclass)
def mutable(cls=None, **kwargs):
    """
      Like dataclass, except:
        * Adds three new instance methods: `asdict()`, `astuple()`, `replace()`
        * ...and one new class method, `fields()`
        * `frozen=True` is now the default!
        * `xmod`-ed for less cruft
    """
    if not cls:
        return functools.partial(mutable, **kwargs)

    return add_methods(dataclass(cls, **kwargs))


@functools.wraps(_field)
def field(default_factory=MISSING, **kwargs):
    return _field(default_factory=default_factory, **kwargs)


def add_methods(dcls):
    methods = (m for m in _METHODS if not hasattr(dcls, m))
    for m in methods:
        method = globals()[m]
        if m in _CLASS_METHODS:
            method = classmethod(method)
        setattr(dcls, m, method)
    return dcls


hidden = functools.partial(field, compare=False, init=False, repr=False)
immutable = functools.partial(mutable, frozen=True)
xmod(immutable, 'datacls')
