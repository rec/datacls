from dataclasses import (
    MISSING,
    asdict,
    astuple,
    dataclass,
    field as _field,
    fields,
    make_dataclass as _make_dataclass,
    replace,
)
import functools
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


@functools.wraps(_make_dataclass)
def make_dataclass(*a, **ka):
    return add_methods(_make_dataclass(*a, **ka))


hidden = functools.partial(field, compare=False, init=False, repr=False)
immutable = functools.partial(mutable, frozen=True)
dtyper = None


try:
    cached_property = functools.cached_property

except AttributeError:
    # from Python 3.8
    from _thread import RLock
    _NOT_FOUND = object()

    class cached_property:
        def __init__(self, func):
            self.func = func
            self.attrname = None
            self.__doc__ = func.__doc__
            self.lock = RLock()

        def __set_name__(self, owner, name):
            if self.attrname is None:
                self.attrname = name
            elif name != self.attrname:
                raise TypeError(
                    "Cannot assign the same cached_property to two different names "
                    f"({self.attrname!r} and {name!r})."
                )

        def __get__(self, instance, owner=None):
            if instance is None:
                return self
            if self.attrname is None:
                raise TypeError(
                    "Cannot use cached_property instance without calling __set_name__ on it.")
            try:
                cache = instance.__dict__
            except AttributeError:  # not all objects have __dict__ (e.g. class defines slots)
                msg = (
                    f"No '__dict__' attribute on {type(instance).__name__!r} "
                    f"instance to cache {self.attrname!r} property."
                )
                raise TypeError(msg) from None
            val = cache.get(self.attrname, _NOT_FOUND)
            if val is _NOT_FOUND:
                with self.lock:
                    # check if another thread filled cache while we awaited lock
                    val = cache.get(self.attrname, _NOT_FOUND)
                    if val is _NOT_FOUND:
                        val = self.func(instance)
                        try:
                            cache[self.attrname] = val
                        except TypeError:
                            msg = (
                                f"The '__dict__' attribute on {type(instance).__name__!r} instance "
                                f"does not support item assignment for caching {self.attrname!r} property."
                            )
                            raise TypeError(msg) from None
            return val


class Datacls:
    __call__ = staticmethod(immutable)

    @cached_property
    def dtyper(self):
        import dtyper

        return dtyper.dataclass


xmod(Datacls(), 'datacls')
