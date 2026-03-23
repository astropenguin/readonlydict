# ReadonlyDict

[![Release](https://img.shields.io/pypi/v/readonlydict?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/readonlydict/)
[![Python](https://img.shields.io/pypi/pyversions/readonlydict?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/readonlydict/)
[![Downloads](https://img.shields.io/pypi/dm/readonlydict?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/readonlydict)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.19187089-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.19187089)
[![Tests](https://img.shields.io/github/actions/workflow/status/astropenguin/readonlydict/tests.yaml?label=Tests&style=flat-square)](https://github.com/astropenguin/readonlydict/actions)

Drop-in read-only dictionary with 100% typing and runtime compatibility

## Overview: Why ReadonlyDict?

This package is built strictly on the following formula: ``ReadonlyDict = (Built-in dictionary) - (In-place features) + (Read-only features)``.

- **100% compatibility and zero custom API:** Our goal is to achieve flawless compatibility with Python's built-in dictionary in both static type checking ([mypy], [Pyright]) and runtime behavior. We simply removed in-place methods (e.g., ``pop()``, ``update()``). We do not introduce any custom methods.
- **True immutable semantics:** The only additions are those strictly required for a read-only data structure: it is fully hashable (only if all values are hashable), and shallow copies (``self.copy()``, ``copy.copy(self)``) return itself to save memory.
- **When to use this package:** If you want extended read-only features or custom methods, existing packages like [frozendict], [immutabledict], or [immutables] are better choices. However, if your priority is pure compatibility and perfect static type inference, ReadonlyDict is the optimal choice.

## Installation

```bash
pip install readonlydict
```

## Basic Usage

It works exactly like a built-in dictionary, but raises an error if you try to modify it.

```python
from readonlydict import ReadonlyDict


# Initialization works just like the built-in dictionary:
>>> ro = ReadonlyDict(a=0, b=1)
>>> ro
ReadonlyDict({'a': 0, 'b': 1})


# It is fully hashable (can be used as a dictionary key or in a set):
>>> hash(ro)
-5925576189957013898
>>> {ro, ro}
{ReadonlyDict({'a': 0, 'b': 1})}


# Mutation is strictly prohibited (static type checkers will also warn you):
>>> ro["c"] = 2
TypeError: 'ReadonlyDict' object does not support item assignment
>>> ro.update(c=2)
AttributeError: 'ReadonlyDict' object has no attribute 'update'
```

## Advanced Usage: Subclassing with Type Hints

If you want to create your own custom read-only dictionary by subclassing ``ReadonlyDict``, you can maintain static type inference (for both [mypy] and [Pyright]) by utilizing ``TYPE_CHECKING`` and ``@overload``.
Here is the best-practice template for subclassing:

```python
# standard library
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Any, TypeVar, overload

# dependencies
from readonlydict import ReadonlyDict

# type variables
K = TypeVar("K")
K2 = TypeVar("K2")
V = TypeVar("V")
V2 = TypeVar("V2")


class CustomDict(ReadonlyDict[K, V]):
    # Modify the return types to guarantee type inference:
    if TYPE_CHECKING:

        @overload
        def __new__(cls, **kwargs: V) -> "CustomDict[str, V]": ...
        @overload
        def __new__(cls, mapping: Mapping[K, V], /, **kwargs: V2) -> "CustomDict[K | str, V | V2]": ...
        @overload
        def __new__(cls, iterable: Iterable[tuple[K, V]], /, **kwargs: V2) -> "CustomDict[K | str, V | V2]": ...
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

    # Then add your custom properties or methods:
    @property
    def first(self) -> tuple[K, V]:
        return next(iter(self.items()))
```

[frozendict]: https://github.com/Marco-Sulla/python-frozendict
[immutabledict]: https://immutabledict.corenting.fr
[immutables]: https://github.com/MagicStack/immutables
[mypy]: https://www.mypy-lang.org
[Pyright]: https://microsoft.github.io/pyright
