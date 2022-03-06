========================================================
``dataclass``: a slightly improved dataclasses
========================================================

The Python built-in
`dataclass <https://docs.python.org/3/library/dataclasses.html>`_ is almost
perfect, and this module just adds a little bit on top of it to smooth the
rough edges a bit.

``dataclass.mutable()`` is
`dataclasses.dataclass()
<https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass>`_
, except:

* three new instance method added to each dataclass
  * ``asdict()`` like `dataclasses.asdict()
<https://docs.python.org/3/library/dataclasses.html#dataclasses.asdict>`_
  * ``astuple()`` like `dataclasses.astuple()
<https://docs.python.org/3/library/dataclasses.html#dataclasses.astuple>`_
  * ``replace()`` like `dataclasses.replace()
<https://docs.python.org/3/library/dataclasses.html#dataclasses.replace>`_
* ...and one new class method,
  * ``fields()`` like `dataclasses.fields()
<https://docs.python.org/3/library/dataclasses.html#dataclasses.fields>`_
* ``xmod`` -ed for less cruft


``dataclass.immutable()`` is like ``dataclass.mutable`` except
``frozen=True`` by default.

``dataclass.field`` just like `dataclasses.field
<https://docs.python.org/3/library/dataclasses.html#dataclasses.field>`_
except ``default_factory`` is now (also) a positional parameter.

``dataclass.immutable()`` is also known as just ``dataclass()``!  You can get
this just by calling the module, to encourage the use of immutable data
structures by default.


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

    #
    # Three new instance methods
    #
    o = One()
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

    @dataclass.mutable
    class OneMutable:
        one: str = 'one'
        two: int = 2
        three: Dict = dataclass.field(dict)

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

    # In this case, you can access them as functions on `dataclass`:
    assert (
        dataclass.asdict(ov) ==
        {'asdict': 1, 'astuple': 1, 'fields': 1, 'one': 'one', 'replace': 1}
    )

    assert dataclass.astuple(ov) == ('one', 1, 1, 1, 1)
