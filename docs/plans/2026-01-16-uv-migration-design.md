# Migration to uv + Modern Python Packaging

## Overview

Modernize the project's build and development tooling:
- Migrate from Pipenv to uv
- Replace setup.py with pyproject.toml
- Update CI to Python 3.12, 3.13, 3.14
- Implement trusted publishing to PyPI
- Simplify dev tooling with ruff

## File Changes

| Action | File |
|--------|------|
| Create | `pyproject.toml` |
| Generate | `uv.lock` (via `uv lock`) |
| Update | `justfile` |
| Rewrite | `.github/workflows/main.yml` |
| Delete | `setup.py`, `Pipfile`, `Pipfile.lock`, `Makefile` |

## pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "key_set"
version = "2.0.0"
description = "KeySet with 4 classes to represent concepts of All, None, Some, and AllExceptSome"
readme = "README.md"
license = "Apache-2.0"
requires-python = ">=3.12"
authors = [{ name = "Eduardo Turiño", email = "eturino@eturino.com" }]
keywords = ["set", "key_set"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
]

[project.urls]
Homepage = "https://github.com/eturino/key_set.py"
Repository = "https://github.com/eturino/key_set.py"

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-cov",
    "mypy",
    "black",
    "ruff",
    "twine",
    "build",
    "bump-my-version",
]

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "SIM",    # flake8-simplify
]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true

[tool.black]
target-version = ["py312"]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v"

[tool.bumpversion]
current_version = "2.0.0"
commit = true
tag = true
tag_name = "v{new_version}"
message = "chore(release): {new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'

[tool.hatch.build.targets.wheel]
packages = ["key_set"]
```

## justfile

```just
# key_set justfile

default: test mypy lint

py_files := "key_set tests"

# Sync dev environment (uses uv.lock)
sync:
    uv sync --all-extras

# Update lock file and sync
update:
    uv lock --upgrade
    uv sync --all-extras

# Run tests
test:
    uv run pytest tests -v

# Run tests with coverage
test-cov:
    uv run pytest tests -v --cov=key_set --cov-report=term-missing

# Type checking
mypy:
    uv run mypy key_set

# Lint (ruff replaces flake8 + isort)
lint:
    uv run ruff check {{py_files}}

# Format check
format-check:
    uv run black {{py_files}} --check

# Apply all fixes
fix:
    uv run ruff check {{py_files}} --fix
    uv run black {{py_files}}

# Prepare for PR (clean slate, fix issues, full check)
pr: clean fix check

# Full check
check: test mypy lint format-check

# Build
build:
    uv build

# Bump version (usage: just bump patch|minor|major)
bump part:
    uv run bump-my-version bump {{part}}
    git push && git push --tags

# Clean
clean:
    rm -rf .venv .mypy_cache .pytest_cache .ruff_cache __pycache__ build dist *.egg-info
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Show outdated
outdated:
    uv pip list --outdated
```

## CI Workflow (.github/workflows/main.yml)

```yaml
name: CI

on:
  push:
    branches: [master, feature/*]
    tags: ["v*"]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --frozen --all-extras

      - name: Run tests with coverage
        run: uv run pytest tests -v --cov=key_set --cov-report=xml

      - name: Type check
        run: uv run mypy key_set

      - name: Lint
        run: uv run ruff check key_set tests

      - name: Format check
        run: uv run black key_set tests --check

      - name: Upload coverage to Codecov
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: false

  publish:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

## One-time PyPI Setup

For trusted publishing to work:
1. Go to https://pypi.org/manage/project/key_set/settings/publishing/
2. Add new trusted publisher:
   - Owner: `eturino`
   - Repository: `key_set.py`
   - Workflow name: `main.yml`
   - Environment: `pypi`

## Release Process

```bash
# 1. Update CHANGELOG.md manually
# 2. Bump version (creates commit + tag)
just bump patch  # or minor, major

# CI automatically publishes to PyPI when tag is pushed
```

## Migration Steps

1. Create `pyproject.toml`
2. Update `justfile`
3. Rewrite `.github/workflows/main.yml`
4. Run `uv lock` to generate `uv.lock`
5. Delete `setup.py`, `Pipfile`, `Pipfile.lock`, `Makefile`
6. Run `just pr` to verify everything works
7. Configure PyPI trusted publishing
8. Commit and push
