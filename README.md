# `key_set`

[![CI](https://github.com/eturino/key_set.py/actions/workflows/main.yml/badge.svg)](https://github.com/eturino/key_set.py/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/eturino/key_set.py/branch/master/graph/badge.svg)](https://codecov.io/gh/eturino/key_set.py)
[![PyPI version](https://badge.fury.io/py/key-set.svg)](https://pypi.org/project/key-set/)

**Requires Python 3.12+**

## Installation

```bash
pip install key-set
```

## Overview

Lightweight, zero-dependency library implementing 4 KeySet types representing set theory concepts:
- **All (𝕌)**: Universal set - contains everything
- **None (∅)**: Empty set
- **Some**: Finite subset of elements
- **AllExceptSome**: Complement of a finite set

Operations like `intersect`, `union`, `difference` are algebraically correct. You can also check inclusion with `includes(element)` or use `element in keyset`.

Python port of [KeySet in TypeScript](https://github.com/eturino/ts-key-set)
and [KeySet in Ruby](https://github.com/eturino/ruby_key_set)


## Limitations

- for now, only KeySet of strings
- no ComposedKeySet yet (see [KeySet in TypeScript](https://github.com/eturino/ts-key-set#composedkeyset))

## `KeySetType` enum

Enum that represents the 4 types of KeySets:

- `ALL` represents the entirety of possible keys (`𝕌`)
- `NONE` represents an empty set (`∅`)
- `SOME` represents a concrete set (`A ⊂ 𝕌`)
- `ALL_EXCEPT_SOME` represents the complementary of a set, all the elements except the given
  ones (`A' = {x ∈ 𝕌 | x ∉ A}`) _(see [Complement in Wikipedia](https://en.wikipedia.org/wiki/Complement_set_theory))*

## Creation

Build your KeySets using the build functions

```python
from key_set import build_all, build_none, build_some_or_none, build_all_except_some_or_all

build_all()  # => returns a new instance of KeySetAll
build_none()  # => returns a new instance of KeySetNone

build_some_or_none([])  # returns a new instance of KeySetNone

# returns a new instance of KeySetSome with keys {'a', 'b', 'c'} (in a unique set)
build_some_or_none({'a', 'c', 'b'})
build_some_or_none(['a', 'c', 'b', 'c'])

build_all_except_some_or_all([])  # returns a new instance of KeySetAll

# returns a new instance of KeySetAllExceptSome with keys {'a', 'b', 'c'} (in a unique set)
build_all_except_some_or_all({'a', 'c', 'b'})
build_all_except_some_or_all(['a', 'c', 'b', 'c'])
```

## `KeySet` classes

Methods exposed:

### `key_set_type()`

returns the `KeySetType` enum

### `elements()`

returns the set with the elements. It will be blank for `All` and `None`.

### `represents_xxx()` methods

- `represents_all`: returns True if the KeySet is ALL
- `represents_none`: returns True if the KeySet is NONE
- `represents_some`: returns True if the KeySet is SOME
- `represents_all_except_some`: returns True if the KeySet is ALL_EXCEPT_SOME

### `invert()`

Returns a new KeySet that represents the inverse Set of this one.

- `ALL` <-> `NONE`
- `SOME` <-> `ALL_EXCEPT_SOME`

### `intersect(other)`

Returns a new KeySet with the intersection (A ∩ B) of both Sets: a set that contains the elements included in both sets.

### `union(other)`

Returns a new KeySet with the union (A ∪ B) of both Sets: a set that contains the elements in any of the sets.

### `difference(other)`

Returns a new KeySet with the difference (A - B) of the Sets: a set that contains the elements of A that are not in B.

### `includes(element)`

Returns True if the set that this KeySet represents contains the given element.

### `clone()`

Returns a new KeySet with the same elements.

## Hashability

All KeySet classes are hashable and can be used as dictionary keys or in sets:

```python
from key_set import KeySetSome, KeySetAll

cache = {
    KeySetAll(): "all data",
    KeySetSome({'a', 'b'}): "partial data",
}

unique_keysets = {KeySetSome({'a'}), KeySetSome({'a'})}  # contains 1 element
```

## `len()` support

`KeySetNone`, `KeySetSome`, and `KeySetAllExceptSome` support `len()`:

```python
len(KeySetNone())  # 0
len(KeySetSome({'a', 'b'}))  # 2
len(KeySetAllExceptSome({'a', 'b'}))  # 2 (number of excluded elements)
```

`KeySetAll` represents an infinite set, so by default `len()` raises `TypeError`:

```python
len(KeySetAll())  # raises TypeError
```

### Compatibility mode for `KeySetAll`

If you need `len()` to work on all KeySet types (e.g., for code that expects all objects to support `len()`), you can enable compatibility mode:

```python
from key_set import KeySetAll

KeySetAll.enable_compat_len(True)
len(KeySetAll())  # returns sys.maxsize

KeySetAll.enable_compat_len(False)  # restore default behavior
len(KeySetAll())  # raises TypeError again
```
