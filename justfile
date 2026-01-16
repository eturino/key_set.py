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
pr: clean sync fix check

# Full check
check: test mypy lint format-check

# Build
build:
    uv build

# Bump version (usage: just bump patch|minor|major)
bump part:
    uv run bump-my-version bump {{part}}
    git push && git push --tags

# Tag current commit (usage: just tag v2.0.0)
tag version:
    git tag -a {{version}} -m "Release {{version}}"
    git push origin {{version}}

# Create GitHub release with auto-generated notes (usage: just release v2.0.0)
release version:
    gh release create {{version}} --generate-notes --title "{{version}}"

# Create GitHub release with custom notes (usage: just release-notes v2.0.0 "Release notes here")
release-notes version notes:
    gh release create {{version}} --title "{{version}}" --notes "{{notes}}"

# Create GitHub release with notes from file (usage: just release-file v2.0.0 RELEASE_NOTES.md)
release-file version file:
    gh release create {{version}} --title "{{version}}" --notes-file "{{file}}"

# Clean
clean:
    rm -rf .venv .mypy_cache .pytest_cache .ruff_cache __pycache__ build dist *.egg-info
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Show outdated
outdated:
    uv pip list --outdated
