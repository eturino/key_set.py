# Required executables
ifeq (, $(shell which python))
 $(error "No python on PATH.")
endif
ifeq (, $(shell uv help))
 $(error "uv not available in Python installation.")
endif

export LC_ALL = C
export LANG = C.UTF-8
PY_FILES := my_module tests

# Bundle tasks

all: clean venv build
	@echo Executed default build pipeline

# Clean up and set up

clean:
	@echo Clean project base
	find . -type d \
	-name ".venv" -o \
	-name ".tox" -o \
	-name ".ropeproject" -o \
	-name ".mypy_cache" -o \
	-name ".ruff_cache" -o \
	-name ".pytest_cache" -o \
	-name "__pycache__" -o \
	-iname "*.egg-info" -o \
	-name "build" -o \
	-name "dist" \
	|xargs rm -rfv

clear-cache:
	@echo Clear dependency cache
	uv cache clean

venv: clean
	@echo Initialize virtualenv, i.e., install required packages etc.
	uv sync

# Building software

build: test mypy lint format
	@echo Run build process to package application
	uv build

test:
	@echo Run all tests suites
	uv run py.test tests

mypy:
	@echo Run static code checks against source code base
	uv run mypy $(PY_FILES)

lint:
	@echo Run linting checks using ruff
	uv run ruff check $(PY_FILES)

lint-fix:
	@echo Fix linting issues using ruff
	uv run ruff check --fix $(PY_FILES)

format:
	@echo Run code formatting using ruff
	uv run ruff format $(PY_FILES)

format-check:
	@echo Check code formatting using ruff
	uv run ruff format --check $(PY_FILES)

outdated:
	@echo Show outdated dependencies
	uv pip list --outdated --exclude-editable

update:
	@echo Update outdated dependencies
	uv sync --upgrade

# Executing

run-venv:
	@echo Execute package directly in virtual environment
	uv run python -m my_module

install-run:
	@echo Install and run package via CLI using the activated Python env
	python -m pip install --upgrade .
	@echo --- Note: The next command might fail before you reload your shell
	my_module_cli
