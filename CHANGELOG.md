# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [2.0.0](https://github.com/eturino/key_set.py/compare/v1.1.1...v2.0.0) (2026-01-16)

### BREAKING CHANGES

* **Python version**: Now requires Python 3.12+ (previously 3.6+)
* **KeySetAll.__len__**: Now raises `TypeError` instead of returning 0, since `KeySetAll` represents an infinite set

### Features

* `KeySetAll.enable_compat_len(True)` - opt-in compatibility mode where `len(KeySetAll())` returns `sys.maxsize` instead of raising `TypeError`
* Use `match` statements with exhaustive type checking via `assert_never`
* Use `frozenset` internally for better performance and hashability
* Add `__hash__` to all KeySet classes (now usable as dict keys and in sets)
* Add `__slots__` for reduced memory footprint
* Use `Iterable[str]` for more flexible input types
* Migrate from Makefile to `just` for task running

### Performance

* Internal storage uses `frozenset` instead of `set` - faster operations
* `__slots__` reduces per-instance memory overhead
* Direct frozenset operations avoid unnecessary copies in set operations

### Build & Tooling

* Migrate from Pipenv to uv with pyproject.toml
* Migrate from Makefile to justfile
* CI tests on Python 3.12, 3.13, 3.14
* Replace flake8 + plugins with ruff
* Add Codecov coverage reporting
* Add trusted publishing to PyPI via OIDC
* Add mise.toml for local tool versioning

### [1.1.1](https://github.com/eturino/key_set.py/compare/v1.1.0...v1.1.1) (2022-02-25)

## 1.1.0 (2021-08-02)


### Features

* __contains__, __str__, and __repr__ ([1bebb4d](https://github.com/eturino/key_set.py/commit/1bebb4df8d6bd7f519c46abfb73cef60fb0ce4a4))
* adding KeySetType enum ([108e3df](https://github.com/eturino/key_set.py/commit/108e3df7c911f3d1f0c5a1d50d0c2ab4fdd04cd5))
* build and readme ([dbd5e0a](https://github.com/eturino/key_set.py/commit/dbd5e0a5c579013b3178b50a58be6208de74547e))
* difference() ([8a08634](https://github.com/eturino/key_set.py/commit/8a0863457307853096cc8adf9b3086cead1505e0))
* equality and clone ([3362cf7](https://github.com/eturino/key_set.py/commit/3362cf7657adc222a760a69de8db395f5ee56560))
* equality non-hashable ([e685dd9](https://github.com/eturino/key_set.py/commit/e685dd945e06da65d421443eb39acfbc41452b35))
* includes(elem) ([48d2d66](https://github.com/eturino/key_set.py/commit/48d2d664d29969008278c79bc04020c0cb616eb4))
* intersect(other) ([f07b3fd](https://github.com/eturino/key_set.py/commit/f07b3fdb84d4e8e7e00bbe8f1e3e8c95ac63e4ce))
* inverse() ([159004d](https://github.com/eturino/key_set.py/commit/159004da10baf7648ac72fb5606a902720b7ab3a))
* represents_xxx methods ([85aa4f3](https://github.com/eturino/key_set.py/commit/85aa4f3a64cbef662e55b9e380fed182cdbd7c43))
* union(other) ([27e992e](https://github.com/eturino/key_set.py/commit/27e992e025aff69ebcfdf2a352cf8ab327105e1b))


### Bug Fixes

* fixing tests and circular dependencies ([2324136](https://github.com/eturino/key_set.py/commit/23241365e38129262e741ecf151d3579bb85af7d))
* type hint ([50a992d](https://github.com/eturino/key_set.py/commit/50a992d31611f36aef896c5194f0c3e37012f8ca))

## 1.0.0 (2021-08-02)


### Features

* adding KeySetType enum ([108e3df](https://github.com/eturino/key_set.py/commit/108e3df7c911f3d1f0c5a1d50d0c2ab4fdd04cd5))
* build and readme ([dbd5e0a](https://github.com/eturino/key_set.py/commit/dbd5e0a5c579013b3178b50a58be6208de74547e))
* difference() ([8a08634](https://github.com/eturino/key_set.py/commit/8a0863457307853096cc8adf9b3086cead1505e0))
* equality and clone ([3362cf7](https://github.com/eturino/key_set.py/commit/3362cf7657adc222a760a69de8db395f5ee56560))
* equality non-hashable ([e685dd9](https://github.com/eturino/key_set.py/commit/e685dd945e06da65d421443eb39acfbc41452b35))
* includes(elem) ([48d2d66](https://github.com/eturino/key_set.py/commit/48d2d664d29969008278c79bc04020c0cb616eb4))
* intersect(other) ([f07b3fd](https://github.com/eturino/key_set.py/commit/f07b3fdb84d4e8e7e00bbe8f1e3e8c95ac63e4ce))
* inverse() ([159004d](https://github.com/eturino/key_set.py/commit/159004da10baf7648ac72fb5606a902720b7ab3a))
* represents_xxx methods ([85aa4f3](https://github.com/eturino/key_set.py/commit/85aa4f3a64cbef662e55b9e380fed182cdbd7c43))
* union(other) ([27e992e](https://github.com/eturino/key_set.py/commit/27e992e025aff69ebcfdf2a352cf8ab327105e1b))


### Bug Fixes

* fixing tests and circular dependencies ([2324136](https://github.com/eturino/key_set.py/commit/23241365e38129262e741ecf151d3579bb85af7d))
* type hint ([50a992d](https://github.com/eturino/key_set.py/commit/50a992d31611f36aef896c5194f0c3e37012f8ca))
