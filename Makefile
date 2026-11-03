UV ?= uv
PY_PATHS := aha-feature/scripts tests
# Reference validator for the Agent Skills spec, pinned to a commit.
SKILLS_REF := git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379\#subdirectory=skills-ref

.PHONY: install fmt lint format-check typecheck test check validate-skills

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

validate-skills: ## Validate every skill against the Agent Skills spec (needs network)
	@for d in */SKILL.md; do \
		$(UV)x --from "$(SKILLS_REF)" skills-ref validate "$$(dirname "$$d")" || exit 1; \
	done
