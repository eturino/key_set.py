# Required executables
ifeq (, $(shell which python3))
 $(error "No python3 on PATH.")
endif
ifeq (, $(shell which pipenv))
 $(error "No pipenv on PATH.")
endif

# Suppress warning if pipenv is started inside .venv
export PIPENV_VERBOSITY=1
# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT=1
# Ignore existing venvs (required for travis)
export PIPENV_IGNORE_VIRTUALENVS=1
# Setup python path
PYTHONPATH=.
# Make sure we are running with an explicit encoding
LC_ALL=C.UTF-8
LANG=C.UTF-8

venv:
	# Initialize virtualenv, i.e., install required packages etc.
	pip3 install pipenv --upgrade
	pipenv --three install --dev --skip-lock

shell:
	# Initialize virtualenv and open a new shell using it
	pipenv shell

clean:
	# Clean project base
	rm -rfv \
		.venv \
		.tox \
		.egg \
		*.egg-info \
		build \
		dist \
		**/.pytest_cache \
		.pytest_cache \
		**/__pycache__

test:
	# Run all tests in default virtualenv
	pipenv run py.test tests

testall:
	# Run all tests against all virtualenvs defined in tox.ini
	pipenv run tox tests

coverage:
	# Run test coverage checks
	pipenv run py.test -c .coveragerc --verbose tests

lint:
	# Run code formatting checks against source code base
	pipenv run flake8 my_module tests

build: test coverage lint
	# Run setup.py-based build process to package application
	pipenv run python setup.py bdist_wheel

publish: build
	# Release
	pipenv run twine upload dist/*

run:
	# Execute my_module directly
	pipenv run python -m my_module

all: clean venv build

.PHONY: all