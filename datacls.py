from dataclasses import asdict, astuple, fields, replace
import dataclasses
import functools
import xmod

__all__ = (
    'asdict', 'astuple', 'frozen', 'field', 'fields', 'mutable', 'replace'
)
__version__ = '0.9.3'

_METHODS = 'asdict', 'astuple', 'fields', 'replace'
_CLASS_METHODS = {'fields'}


@functools.wraps(dataclasses.dataclass)
def mutable(cls=None, **kwargs):
    """
      Like dataclasses.dataclass, except:
        * Adds three new instance methods: `asdict()`, `astuple()`, `replace()`
        * ...and one new class method, `fields()`
        * `frozen=True` is now the default!
        * `xmod`-ed for less cruft
    """
    if not cls:
        return functools.partial(mutable, **kwargs)

    dcls = dataclasses.dataclass(cls, **kwargs)
    methods = (m for m in _METHODS if not hasattr(dcls, m))
    for m in methods:
        method = getattr(dataclasses, m)
        if m in _CLASS_METHODS:
            method = classmethod(method)
        setattr(dcls, m, method)

    return dcls


@functools.wraps(dataclasses.dataclass)
@xmod
def frozen(cls=None, **kwargs):
    kwargs.setdefault('frozen', True)
    return mutable(cls, **kwargs)


@functools.wraps(dataclasses.field)
def field(default_factory=None, **kwargs):
    """
      Like dataclasses.field, except:
        * `default_factory` is now also a positional parameter
    """
    return dataclasses.field(default_factory=default_factory, **kwargs)
