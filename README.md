# ReadonlyDict

[![Release](https://img.shields.io/pypi/v/readonlydict?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/readonlydict/)
[![Python](https://img.shields.io/pypi/pyversions/readonlydict?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/readonlydict/)
[![Downloads](https://img.shields.io/pypi/dm/readonlydict?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/readonlydict)
[![Tests](https://img.shields.io/github/actions/workflow/status/astropenguin/readonlydict/tests.yaml?label=Tests&style=flat-square)](https://github.com/astropenguin/readonlydict/actions)

Drop-in read-only dictionary with typing and runtime compatibility

## Installation

```bash
pip install readonlydict
```

## Usage

```python
>>> from readonlydict import ReadonlyDict

>>> dict(a=0, b=1)
{"a": 0, "b": 1}

>>> ReadonlyDict(a=0, b=1)
ReadonlyDict({"a": 0, "b": 1})
```

