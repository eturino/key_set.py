# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python boilerplate/template project designed as a best-practices starting point for Python modules. It uses `uv` for dependency management and virtual environments (not Poetry or pip-tools). The project name is currently `my_module` and is meant to be renamed via `rename_template.sh` when used as a template.

## Development Commands

All operations are managed through the Makefile, which acts as a facade for `uv` commands:

### Initial Setup
```bash
make                # Clean, create venv, sync dependencies, and run full build
```

### Testing
```bash
make test           # Run pytest test suite
uv run py.test tests                    # Run all tests
uv run py.test tests/test_code.py       # Run a single test file
```

### Code Quality
```bash
make build          # Run full build: test, mypy, isort, black, lint, then package
make mypy           # Type checking with mypy
make isort          # Check import sorting (read-only)
make isort-apply    # Fix import sorting
make black          # Format code with black
make lint           # Run flake8 linting
```

### Execution
```bash
make run-venv       # Run the module directly: uv run python -m my_module
make install-run    # Install package and run via CLI as my_module_cli
```

### Environment Management
```bash
make clean          # Remove all generated files (.venv, caches, build artifacts)
make venv           # Clean and recreate virtual environment with uv sync
make clear-cache    # Clear uv dependency cache
make outdated       # Show outdated dependencies
make update         # Update outdated dependencies
```

### Template Setup
```bash
./rename_template.sh    # Rename the template project (interactive script)
```

## Architecture

### Package Structure
- `my_module/` - Main module code
  - `__init__.py` - Package initialization
  - `__main__.py` - Entry point with `main()` function
- `tests/` - Test suite using pytest
- CLI entry point defined in pyproject.toml as `my_module_cli`

### Build System
- Uses `uv` as the build backend (specified in pyproject.toml)
- `module-root = ""` in uv build config means the package is at repository root
- Package structure follows packaging.python.org standards

### Code Quality Configuration
- **Black**: Line length 88, `skip-string-normalization = true`
- **Flake8**: Max line length 88 (matches black), ignores Q003, W503, E203
- **Mypy**: Strict mode with `disallow_untyped_defs = true`, `check_untyped_defs = true`
- **isort**: Configured to work with black and flake8
- Python versions supported: 3.10, 3.11, 3.12, 3.13 (requires-python: ">=3.10,<3.14")

### Testing
- Uses pytest with `-p no:warnings` to suppress warnings
- Tests should follow the class-based structure in `tests/test_code.py`

### VSCode Integration
- Python formatter: black-formatter (format on save enabled)
- Pytest discovery enabled
- Tab size: 4 spaces
- Word wrap: 88 columns
- Trailing whitespace automatically trimmed
