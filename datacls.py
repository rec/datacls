from dataclasses import asdict, astuple, fields, replace
import dataclasses
import functools
import xmod

__all__ = (
    'asdict',
    'astuple',
    'field',
    'fields',
    'hidden',
    'immutable',
    'mutable',
    'replace',
)
__version__ = '3.0.0'

_METHODS = 'asdict', 'astuple', 'fields', 'replace'
_CLASS_METHODS = {'field_names', 'fields'}
_NONE = object()
_DEFAULTS = 'default', 'default_factory'
_DFLT_ERR = 'Just one of default, default_factory and default_value may be set'


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
        method = globals()[m]
        if m in _CLASS_METHODS:
            method = classmethod(method)
        setattr(dcls, m, method)

    return dcls


@functools.wraps(dataclasses.dataclass)
@xmod
def immutable(cls=None, **kwargs):
    kwargs.setdefault('frozen', True)
    return mutable(cls, **kwargs)


@functools.wraps(dataclasses.field)
def field(default_value=_NONE, *, hidden=False, **kwargs):
    """
      This is dataclasses.field() with two new parameters:
        * `default` can be either a value or a callable
        * `hidden` turns off init, repr, compare
    """
    if hidden:
        for k in 'compare', 'init', 'repr':
            kwargs.setdefault(k, False)

    if default_value is not _NONE:
        if any(d in kwargs for d in _DEFAULTS):
            raise ValueError(_DFLT_ERR)
        default_name = _DEFAULTS[callable(default_value)]
        kwargs[default_name] = default_value

    return dataclasses.field(**kwargs)


hidden = functools.partial(field, hidden=True)
