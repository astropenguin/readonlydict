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
    """Drop-in read-only dictionary with typing and runtime compatibility."""

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
            self._data = dict(*args, **kwargs)
            self._hash = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # methods for hashable
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(frozenset(self._data.items()))

        return self._hash

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # methods for mapping
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __getitem__(self, key: K, /) -> V:
        return self._data[key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # methods to be compatible with built-in dictionary
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def copy(self) -> Self:
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
        return cls(dict.fromkeys(iterable, value))

    def __or__(self, other: Mapping[K2, V2], /) -> "ReadonlyDict[K | K2, V | V2]":
        if not isinstance(other, Mapping):  # pyright: ignore
            return NotImplemented

        return self.__class__(self._data | dict(other))  # pyright: ignore

    def __ror__(self, other: Mapping[K2, V2], /) -> dict[K | K2, V | V2]:
        if not isinstance(other, Mapping):  # pyright: ignore
            return NotImplemented

        return dict(other) | self._data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def __reversed__(self) -> Iterator[K]:
        return reversed(self._data)
