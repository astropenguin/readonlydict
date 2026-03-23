__all__ = ["ReadonlyDict"]
__version__ = "1.0.0rc1"

# standard library
from collections.abc import Iterable, Iterator, Mapping
from typing import TYPE_CHECKING, Any, TypeVar, overload

# dependencies
from typing_extensions import Self

# type hints
K = TypeVar("K")
V = TypeVar("V")
K2 = TypeVar("K2")
V2 = TypeVar("V2")
Tuples = Iterable[tuple[K, V]]


class ReadonlyDict(Mapping[K, V]):
    """Drop-in read-only dictionary with typing and runtime compatibility.

    - ``ReadonlyDict()`` -> New empty read-only dictionary.
    - ``ReadonlyDict(mapping)`` -> New read-only dictionary
      initialized from a mapping object's ``(key, value)`` pairs.
    - ``ReadonlyDict(iterable)`` -> New read-only dictionary
      initialized as if via: ``d = {}; for k, v in iterable: d[k] = v``.
    - ``ReadonlyDict(**kwargs)`` -> New read-only dictionary
      initialized with the ``name=value`` pairs in the keyword argument list.
      For example: ``ReadonlyDict(one=1, two=2)``.

    """

    _data: dict[K, V]
    _hash: int | None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # methods for initialization
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    if TYPE_CHECKING:

        @overload
        def __new__(cls, mapping: Mapping[K, V], /) -> Self: ...  # pyright: ignore
        @overload
        def __new__(cls, iterable: Tuples[K, V], /) -> Self: ...  # pyright: ignore
        @overload
        def __new__(cls, **kwargs: V) -> "ReadonlyDict[str, V]": ...

        # fmt: off
        @overload
        def __new__(cls, mapping: Mapping[K, V], /, **kwargs: V2) -> "ReadonlyDict[K | str, V | V2]": ...
        @overload
        def __new__(cls, iterable: Tuples[K, V], /, **kwargs: V2) -> "ReadonlyDict[K | str, V | V2]": ...
        # fmt: on

        def __new__(cls, *args: Any, **kwargs: Any) -> Any:  # type: ignore[misc]
            return super().__new__(cls)

    else:

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize ``self``. See ``help(type(self))`` for accurate signature."""
            self._data = dict(*args, **kwargs)
            self._hash = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # methods for immutability
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __copy__(self) -> Self:
        """Return ``self`` for a shallow copy."""
        return self

    def __hash__(self) -> int:
        """Return ``hash(self)``."""
        if self._hash is None:
            self._hash = hash(frozenset(self._data.items()))

        return self._hash

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # methods for instantiation
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __getitem__(self, key: K, /) -> V:
        """Return ``self[key]``."""
        return self._data[key]

    def __iter__(self) -> Iterator[K]:
        """Return ``iter(self).``"""
        return iter(self._data)

    def __len__(self) -> int:
        """Return ``len(self)``."""
        return len(self._data)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # methods to be compatible with built-in dictionary
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def copy(self) -> Self:
        """Return a shallow copy of ``self``."""
        return self

    # fmt: off
    @overload
    @classmethod
    def fromkeys(cls, iterable: Iterable[K2], /) -> "ReadonlyDict[K2, None]": ...
    @overload
    @classmethod
    def fromkeys(cls, iterable: Iterable[K2], value: V2, /) -> "ReadonlyDict[K2, V2]": ...
    # fmt: on

    @classmethod
    def fromkeys(cls, iterable: Iterable[Any], value: Any = None, /) -> Any:
        """Create a new read-only dictionary with keys from ``iterable`` and values set to ``value``."""
        return cls(dict.fromkeys(iterable, value))

    def __or__(self, other: Mapping[K2, V2], /) -> "ReadonlyDict[K | K2, V | V2]":
        """Return ``self|value``."""
        if not isinstance(other, Mapping):  # pyright: ignore
            return NotImplemented

        return self.__class__(self._data | dict(other))  # pyright: ignore

    def __ror__(self, other: Mapping[K2, V2], /) -> dict[K | K2, V | V2]:
        """Return ``value|self``."""
        if not isinstance(other, Mapping):  # pyright: ignore
            return NotImplemented

        return dict(other) | self._data

    def __repr__(self) -> str:
        """Return ``repr(self)``."""
        return f"{self.__class__.__name__}({self._data!r})"

    def __reversed__(self) -> Iterator[K]:
        """Return ``reversed(self)``."""
        return reversed(self._data)
