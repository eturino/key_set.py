# key_set justfile

# Default recipe
default: test mypy lint

# Python files to check
py_files := "key_set tests"

# Create virtual environment and install dependencies
venv:
    rm -rf .venv
    uv venv --python 3.12
    uv pip install -e ".[dev]" || uv pip install pytest mypy black isort flake8 -e .

# Run tests
test:
    pytest tests -v

# Run tests with coverage
test-cov:
    pytest tests -v --cov=key_set --cov-report=term-missing

# Run mypy type checker
mypy:
    mypy key_set

# Run black formatter (check only)
black:
    black {{py_files}} --check

# Run black formatter (apply)
black-apply:
    black {{py_files}}

# Run isort (check only)
isort:
    isort --profile black --check-only {{py_files}}

# Run isort (apply)
isort-apply:
    isort --profile black {{py_files}}

# Run all linting checks
lint: isort black
    flake8 key_set tests

# Apply all formatting fixes
format: isort-apply black-apply

# Full check (test + type check + lint)
check: test mypy lint

# Build wheel
build: check
    python -m build

# Clean build artifacts
clean:
    rm -rf .venv .tox .mypy_cache .pytest_cache __pycache__ build dist *.egg-info
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Publish to PyPI
publish: build
    twine upload dist/*

# Show outdated packages
outdated:
    uv pip list --outdated

# Run the module
run:
    python -m key_set
