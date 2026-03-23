# standard library
from typing import assert_type

# dependencies
from readonlydict import ReadonlyDict

# static-type tests
assert_type(ReadonlyDict(a=0), ReadonlyDict[str, int])
assert_type(ReadonlyDict({"a": 0}), ReadonlyDict[str, int])
assert_type(ReadonlyDict({"a": 0}, b="1"), ReadonlyDict[str, int | str])
assert_type(ReadonlyDict({"a": 0}.items()), ReadonlyDict[str, int])
assert_type(ReadonlyDict({"a": 0}.items(), b="1"), ReadonlyDict[str, int | str])
assert_type(ReadonlyDict.fromkeys(["a", "b"]), ReadonlyDict[str, None])
assert_type(ReadonlyDict.fromkeys(["a", "b"], 0), ReadonlyDict[str, int])
assert_type(ReadonlyDict({"a": "0"}) | {"b": 1}, ReadonlyDict[str, int | str])
assert_type({"a": "0"} | ReadonlyDict(b=1), dict[str, int | str])


# runtime tests
def test_copy() -> None:
    ret = ReadonlyDict(a=0, b=1).copy()
    assert ret.copy() is ret


def test_fromkeys() -> None:
    ret_0 = ReadonlyDict.fromkeys(["a", "b"])
    assert ret_0 == dict.fromkeys(["a", "b"])
    assert isinstance(ret_0, ReadonlyDict)

    ret_1 = ReadonlyDict.fromkeys(["a", "b"], 0)
    assert ret_1 == dict.fromkeys(["a", "b"], 0)
    assert isinstance(ret_1, ReadonlyDict)


def test_hash() -> None:
    assert (
        (ret := hash(ReadonlyDict(a=0, b=1)))
        == hash(ReadonlyDict({"a": 0}, b=1))
        == hash(ReadonlyDict({"a": 0, "b": 1}))
        == hash(ReadonlyDict([("a", 0), ("b", 1)]))
        == hash(ReadonlyDict([("a", 0)], b=1))
    )
    assert isinstance(ret, int)


def test_getitem() -> None:
    ret = ReadonlyDict(a=(a := 0), b=(b := 1))
    assert ret["a"] is a
    assert ret["b"] is b


def test_init() -> None:
    assert (
        (ret := ReadonlyDict(a=0, b=1))
        == ReadonlyDict({"a": 0}, b=1)
        == ReadonlyDict({"a": 0, "b": 1})
        == ReadonlyDict([("a", 0), ("b", 1)])
        == ReadonlyDict([("a", 0)], b=1)
    )
    assert isinstance(ret, ReadonlyDict)


def test_iter() -> None:
    assert list(iter(ReadonlyDict(a=0, b=1))) == ["a", "b"]


def test_len() -> None:
    ret = len(ReadonlyDict(a=0, b=1))
    assert ret == 2
    assert isinstance(ret, int)


def test_or() -> None:
    ret_0 = ReadonlyDict(a=0) | {"b": 1}
    assert ret_0 == ReadonlyDict(a=0, b=1)
    assert isinstance(ret_0, ReadonlyDict)

    ret_1 = {"a": 0} | ReadonlyDict(b=1)
    assert ret_1 == {"a": 0, "b": 1}
    assert isinstance(ret_1, dict)


def test_repr() -> None:
    ret = repr(ReadonlyDict(a=0, b=1))
    assert ret == "ReadonlyDict({'a': 0, 'b': 1})"
    assert isinstance(ret, str)


def test_reversed() -> None:
    assert list(reversed(ReadonlyDict(a=0, b=1))) == ["b", "a"]
