import dataclasses
import functools
import xmod

__all__ = 'field', 'dataclass'
__version__ = '0.9.0'

FROZEN = True
_METHODS = 'asdict', 'astuple', 'fields', 'replace'
_CLASS_METHODS = {'fields'}


@xmod
def dataclass(cls=None, **kwargs):
    """
      Like dataclasses.dataclass, except:
        * Adds three new instance methods: `asdict()`, `astuple()`, `replace()`
        * ...and one new class method, `fields()`
        * `frozen=True` is now the default!
        * xmoded for less cruft
    """
    if not cls:
        return functools.partial(dataclass, **kwargs)

    kwargs.setdefault('frozen', FROZEN)
    dcls = dataclasses.dataclass(cls, **kwargs)

    methods = (m for m in _METHODS if not hasattr(dcls, m))
    for m in methods:
        method = getattr(dataclasses, m)
        if m in _CLASS_METHODS:
            method = classmethod(method)
        setattr(dcls, m, method)

    return dcls


@functools.wraps(dataclasses.field)
def field(default_factory=None, **kwargs):
    """
      Like dataclasses.field, except:
        * `default_factory` is now a positional parameter
        * perfectly backward compatible
    """
    return dataclasses.field(default_factory=default_factory, **kwargs)
