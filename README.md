# 🗂 `datacls`: Take the edge off `dataclass` 🗂

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


### [API Documentation](https://rec.github.io/datacls#datacls--api-documentation)
