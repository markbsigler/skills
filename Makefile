UV ?= uv

.PHONY: install fmt lint format-check typecheck test check

install: ## Create the environment and install locked dependencies
	$(UV) sync --locked

fmt: ## Auto-fix and format the Python tooling
	$(UV) run ruff check --fix java-version-upgrade/scripts tests
	$(UV) run ruff format java-version-upgrade/scripts tests

lint: ## Lint the Python tooling
	$(UV) run ruff check java-version-upgrade/scripts tests

format-check: ## Check Python formatting
	$(UV) run ruff format --check java-version-upgrade/scripts tests

typecheck: ## Type-check the Python tooling (strict)
	$(UV) run mypy

test: ## Run the Python test suite with coverage
	$(UV) run pytest

check: lint format-check typecheck test ## Run all Python checks
