# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python boilerplate/template project using `uv` for dependency management. The project name `my_module` is meant to be renamed via `./rename_template.sh` when used as a template.

## Development Commands

All operations are managed through the Makefile (facade for `uv` commands):

```bash
make                # Full setup: clean, create venv, sync deps, run build
make test           # Run pytest test suite
make build          # Run test, mypy, lint, format, then package
make mypy           # Type checking
make lint           # Ruff linting
make lint-fix       # Auto-fix lint issues
make format         # Format code with ruff
make run-venv       # Run module: uv run python -m my_module
```

### Running Single Tests
```bash
uv run py.test tests/test_code.py           # Single file
uv run py.test tests/test_code.py::TestCode # Single class
uv run py.test tests/test_code.py -k "test_code"  # By name pattern
```

### Environment Management
```bash
make clean          # Remove .venv, caches, build artifacts
make venv           # Recreate virtual environment
make update         # Update dependencies
```

## Architecture

- `my_module/` - Main package with `__main__.py` entry point
- `tests/` - pytest test suite (class-based structure)
- CLI entry point: `my_module_cli` (defined in pyproject.toml)

## Code Quality

- **Ruff**: Linting + formatting (line-length 88, quote-style preserve)
  - Includes security scanning via flake8-bandit (S) rules
- **Mypy**: Strict mode (`disallow_untyped_defs = true`)
- **Python**: 3.10, 3.11, 3.12, 3.13

All config is centralized in `pyproject.toml`.
