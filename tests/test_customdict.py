# standard library
from collections.abc import Iterable, Mapping
from copy import copy
from typing import TYPE_CHECKING, Any, TypeVar, overload

# dependencies
from readonlydict import ReadonlyDict, Tuples
from typing_extensions import assert_type

# type variables
K = TypeVar("K")
V = TypeVar("V")
K2 = TypeVar("K2")
V2 = TypeVar("V2")


class CustomDict(ReadonlyDict[K, V]):
    if TYPE_CHECKING:

        # fmt:off
        @overload
        def __new__(cls, **kwargs: V) -> "CustomDict[str, V]": ...
        @overload
        def __new__(cls, mapping: Mapping[K, V], /, **kwargs: V2) -> "CustomDict[K | str, V | V2]": ...
        @overload
        def __new__(cls, iterable: Tuples[K, V], /, **kwargs: V2) -> "CustomDict[K | str, V | V2]": ...
        def __new__(cls, *args: Any, **kwargs: Any) -> Any: ... # type: ignore[misc]

        @overload
        @classmethod
        def fromkeys(cls, iterable: Iterable[K2], /) -> "CustomDict[K2, None]": ...
        @overload
        @classmethod
        def fromkeys(cls, iterable: Iterable[K2], value: V2, /) -> "CustomDict[K2, V2]": ...
        @classmethod
        def fromkeys(cls, *args: Any, **kwargs: Any) -> Any: ...

        def __or__(self, other: Mapping[K2, V2], /) -> "CustomDict[K | K2, V | V2]": ...
        # fmt: on


# static-type tests
assert_type(CustomDict(a=0), CustomDict[str, int])
assert_type(CustomDict({"a": 0}), CustomDict[str, int])
assert_type(CustomDict({"a": 0}, b="1"), CustomDict[str, int | str])
assert_type(CustomDict({"a": 0}.items()), CustomDict[str, int])
assert_type(CustomDict({"a": 0}.items(), b="1"), CustomDict[str, int | str])
assert_type(CustomDict.fromkeys(["a", "b"]), CustomDict[str, None])
assert_type(CustomDict.fromkeys(["a", "b"], 0), CustomDict[str, int])
assert_type(CustomDict({"a": "0"}) | {"b": 1}, CustomDict[str, int | str])
assert_type({"a": "0"} | CustomDict(b=1), dict[str, int | str])


# runtime tests
def test_copy() -> None:
    ret = CustomDict(a=0, b=1).copy()
    assert ret.copy() is ret
    assert copy(ret) is ret


def test_fromkeys() -> None:
    ret_0 = CustomDict.fromkeys(["a", "b"])
    assert ret_0 == dict.fromkeys(["a", "b"])
    assert isinstance(ret_0, CustomDict)

    ret_1 = CustomDict.fromkeys(["a", "b"], 0)
    assert ret_1 == dict.fromkeys(["a", "b"], 0)
    assert isinstance(ret_1, CustomDict)


def test_hash() -> None:
    assert (
        (ret := hash(CustomDict(a=0, b=1)))
        == hash(CustomDict({"a": 0}, b=1))
        == hash(CustomDict({"a": 0, "b": 1}))
        == hash(CustomDict([("a", 0), ("b", 1)]))
        == hash(CustomDict([("a", 0)], b=1))
    )
    assert isinstance(ret, int)


def test_getitem() -> None:
    ret = CustomDict(a=(a := 0), b=(b := 1))
    assert ret["a"] is a
    assert ret["b"] is b


def test_init() -> None:
    assert (
        (ret := CustomDict(a=0, b=1))
        == CustomDict({"a": 0}, b=1)
        == CustomDict({"a": 0, "b": 1})
        == CustomDict([("a", 0), ("b", 1)])
        == CustomDict([("a", 0)], b=1)
    )
    assert isinstance(ret, CustomDict)


def test_iter() -> None:
    assert list(iter(CustomDict(a=0, b=1))) == ["a", "b"]


def test_len() -> None:
    ret = len(CustomDict(a=0, b=1))
    assert ret == 2
    assert isinstance(ret, int)


def test_or() -> None:
    ret_0 = CustomDict(a=0) | {"b": 1}
    assert ret_0 == CustomDict(a=0, b=1)
    assert isinstance(ret_0, CustomDict)

    ret_1 = {"a": 0} | CustomDict(b=1)
    assert ret_1 == {"a": 0, "b": 1}
    assert isinstance(ret_1, dict)


def test_repr() -> None:
    ret = repr(CustomDict(a=0, b=1))
    assert ret == "CustomDict({'a': 0, 'b': 1})"
    assert isinstance(ret, str)


def test_reversed() -> None:
    assert list(reversed(CustomDict(a=0, b=1))) == ["b", "a"]
