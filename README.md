# dataclass
Slightly improved dataclasses

* `dataclass`: like `dataclasses.dataclass`, except:
      * Adds three new instance methods to each dataclass
        * `asdict()`, `astuple()`, `replace()`
      * ...and one new class method,
        * `fields()`
      * `frozen=True` is now the default!
      * `xmod`ed for less cruft

* `dataclass.field`: Like `dataclasses.field`, except:
      * `default_factory` is now a positional parameter
      * perfectly backward compatible
