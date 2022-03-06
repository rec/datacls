========================================================
``dataclass``: slightly improved dataclasses
========================================================

* ``dataclass``: like ``dataclasses.dataclass``, except:
    * Adds three new instance methods to each dataclass
        * ``asdict()``, ``astuple()``, ``replace()``
    * ...and one new class method,
        * ``fields()``
    * ``frozen=True`` is now the default!
    * ``xmod`` -ed for less cruft

* ``dataclass.field``: Like ``dataclasses.field``, except:
      * ``default_factory`` is now a positional parameter
      * perfectly backward compatible


Usage examples
==================

.. code-block:: python

    import dataclass
    from typing import Dict

    @dataclass
    class One:
        one: str = 'one'
        two: int = 2
        three: Dict = dataclass.field(dict)  # Simplified `field`

    @dataclass(frozen=False)
    class OneMutable:
        one: str = 'one'
        two: int = 2
        three: Dict = dataclass.field(dict)

    o = One()

    #
    # Three new instance methods
    #
    assert o.asdict() == {'one': 'one', 'two': 2, 'three': {}}
    assert o.astuple() == ('one', 2, {})

    o2 = o.replace(one='seven', three={'nine': 9})
    assert o2 == One('seven', 2, {'nine': 9})

    #
    # A new class method
    #
    assert [f.name for f in One.fields()] == ['one', 'two', 'three']

    #
    # Immutable by default
    #
    try:
        o.one = 'three'
    except AttributeError:
        pass
    else:
        raise AttributeError('Was mutable!')

    om = OneMutable()
    om.one = 'three'
    assert str(om) == "OneMutable(one='three', two=2, three={})"

    #
    # These four new methods won't break your old dataclasses:
    #
    @dataclass
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

    # In this case, you can access them functions on dataclass:
    assert (
        dataclass.asdict(ov) ==
        {'asdict': 1, 'astuple': 1, 'fields': 1, 'one': 'one', 'replace': 1}
    )

    assert dataclass.astuple(ov) == ('one', 1, 1, 1, 1)
