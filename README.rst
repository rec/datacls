========================================================
``datacls``: a slightly improved dataclasses
========================================================

The Python built-in module
`dataclasses <https://docs.python.org/3/library/dataclasses.html>`_ is almost
perfect.

``datacls`` is a thin wrapper around ``dataclasses``,
completely backward-compatible, that makes common use cases a little easier.

---------------------------------

``@datacls.mutable`` is exactly like
`@dataclasses.dataclass()
<https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass>`_
except that the resulting dataclass has four new methods:

* three new instance methods:

  * ``self.asdict()``, like `dataclasses.asdict() <https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict>`_
  * ``self.astuple()``, like `dataclasses.astuple() <https://docs.python.org/3/library/dataclasses.html#dataclasses.astuple>`_
  * ``self.replace()``, like `dataclasses.replace() <https://docs.python.org/3/library/dataclasses.html#dataclasses.replace>`_

* ...and one new class method:

  * ``cls.fields()``, like `dataclasses.fields() <https://docs.python.org/3/library/dataclasses.html#dataclasses.fields>`_

The new methods are only added if they do not exist on the target dataclass,
so it should be impossible for ``datacls`` to override or shadow user methods or
members by mistake.

-----------------------------------

``@datacls.immutable``, or just ``@datacls``, is exactly like
``datacls.mutable`` except ``frozen=True`` by default, so members can't
be changed after construction (without deliberately subverting the immutability).

-----------------------------------

``datacls.field()`` is just like
`dataclasses.field() <https://docs.python.org/3/library/dataclasses.html#dataclasses.field>`_
except the very common ``default_factory`` argument is now also the first and only
positional parameter.

``datacls.make_dataclass()`` is just like
`dataclasses.make_dataclass() <https://docs.python.org/3/library/dataclasses.html#dataclasses.make_dataclass>`_
except that the class created also has the four new methods listed above.

``datacls.cached_property`` is exactly like ``functools.cached_property`` from
Python 3.8, except with a backport in Python 3.7.

``datacls.dtyper`` is the ``dtyper.dataclass`` decorator, lazily loaded:
https://github.com/rec/dtyper


Usage examples
==================

.. code-block:: python

    import datacls
    from typing import Dict

    @datacls
    class One:
        one: str = 'one'
        two: int = 2
        three: Dict = datacls.field(dict)

    #
    # Three new instance methods: asdict(), astuple(), replace()
    #
    o = One()
    assert o.asdict() == {'one': 'one', 'two': 2, 'three': {}}

    # Same as:
    #
    # import dataclasses
    #
    # assert dataclasses.asdict(o) == {'one': 'one', 'two': 2, 'three': {}}

    assert o.astuple() == ('one', 2, {})

    o2 = o.replace(one='seven', three={'nine': 9})
    assert o2 == One('seven', 2, {'nine': 9})

    #
    # One new class method: fields()
    #
    assert [f.name for f in One.fields()] == ['one', 'two', 'three']

    #
    # @datacls is immutable: use @datacls.mutable for mutable classes
    #
    try:
        o.one = 'three'
    except AttributeError:
        pass
    else:
        raise AttributeError('Was mutable!')

    @datacls.mutable
    class OneMutable:
        one: str = 'one'
        two: int = 2
        three: Dict = datacls.field(dict)

    om = OneMutable()
    om.one = 'three'
    assert str(om) == "OneMutable(one='three', two=2, three={})"

    #
    # These four new methods won't break your old dataclass by mistake:
    #
    @datacls
    class Overloads:
        one: str = 'one'
        asdict: int = 1
        astuple: int = 1
        fields: int = 1
        replace: int = 1

    o = Overloads()

    assert datacls.astuple(ov) == ('one', 1, 1, 1, 1)

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
