# skills

Agentic AI skills.

More context and examples: [agentskills.io](https://agentskills.io/).

Summary: a curated set of reusable skill docs, references, and scripts for building, documenting, and upgrading AI agent workflows.

## Skills

| Skill | What it does |
| --- | --- |
| [aha-feature](aha-feature/SKILL.md) | Elicits, elaborates, and verifies Aha! features as spec-driven records through the Aha! MCP server, with EARS requirements and on-demand Spec Kit, OpenSpec, or Kiro export |
| [codebase-diagrams](codebase-diagrams/SKILL.md) | Generates Mermaid architecture diagrams for a codebase |

## Install

Install a skill with [GitHub CLI](https://cli.github.com/) 2.90 or later:

```bash
gh skill install markbsigler/skills aha-feature --agent github-copilot --scope user   # or --agent cursor
```

[INSTALL.md](INSTALL.md) gives step-by-step instructions for GitHub Copilot (VS Code and Copilot CLI) and Cursor, including other install methods and connecting aha-feature to the Aha! MCP server.

## Evals

Each skill's `evals/` folder holds labeled prompts for testing whether its `description` triggers on the right requests, following the [agentskills.io description-optimization guide](https://agentskills.io/skill-creation/optimizing-descriptions). Each entry is `{"query": ..., "should_trigger": true|false}`. `train_queries.json` is for iterating on the description and `validation_queries.json` is held back to check that changes generalize. The files are for skill authors and are not loaded by the agent.

## Development

Python helper scripts carry [PEP 723](https://peps.python.org/pep-0723/) metadata, so a script can run in an isolated environment without installing anything globally:

```bash
uv run aha-feature/scripts/aha_feature.py lint draft.md --gate elaborated
```

Repository-level linting, type checking, and tests use [uv](https://docs.astral.sh/uv/):

```bash
uv sync --locked
make check            # ruff, mypy (strict), pytest
make validate-skills  # validate every skill with the agentskills.io reference validator (needs network)
```

CI runs both, plus shellcheck on the bundled shell scripts. Each skill must keep `name` equal to its directory name and pass `skills-ref validate`.

