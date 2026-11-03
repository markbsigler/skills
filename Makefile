UV ?= uv
PY_PATHS := aha-feature/scripts tests

.PHONY: install fmt lint format-check typecheck test check

install: ## Create the environment and install locked dependencies
	$(UV) sync --locked

fmt: ## Auto-fix and format the Python tooling
	$(UV) run ruff check --fix $(PY_PATHS)
	$(UV) run ruff format $(PY_PATHS)

lint: ## Lint the Python tooling
	$(UV) run ruff check $(PY_PATHS)

format-check: ## Check Python formatting
	$(UV) run ruff format --check $(PY_PATHS)

typecheck: ## Type-check the Python tooling (strict)
	$(UV) run mypy

test: ## Run the Python test suite with coverage
	$(UV) run pytest

check: lint format-check typecheck test ## Run all Python checks
