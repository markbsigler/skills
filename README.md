# skills

Agentic AI skills.

More context and examples: [agentskills.io](https://agentskills.io/).

Summary: a curated set of reusable skill docs, references, and scripts for building, documenting, and upgrading AI agent workflows.

## Skills

| Skill | What it does |
| --- | --- |
| [aha-feature](aha-feature/SKILL.md) | Elicits, elaborates, and verifies Aha! features as spec-driven records through the Aha! MCP server, with EARS requirements and on-demand Spec Kit, OpenSpec, or Kiro export |
| [feature-creator](feature-creator/SKILL.md) | Drafts a feature specification document in Aha!-aligned Markdown |
| [codebase-diagrams](codebase-diagrams/SKILL.md) | Generates Mermaid architecture diagrams for a codebase |
| [java-version-upgrade](java-version-upgrade/SKILL.md) | Upgrades Java projects across versions, with dependency analysis |

## Install

Install a skill with [GitHub CLI](https://cli.github.com/) 2.90 or later:

```bash
gh skill install markbsigler/skills aha-feature --agent github-copilot --scope user   # or --agent cursor
```

[INSTALL.md](INSTALL.md) gives step-by-step instructions for GitHub Copilot (VS Code and Copilot CLI) and Cursor, including other install methods and connecting aha-feature to the Aha! MCP server.

## Development

Python helper scripts carry [PEP 723](https://peps.python.org/pep-0723/) metadata, so a script can run in an isolated environment without installing anything globally:

```bash
uv run java-version-upgrade/scripts/analyze_java_dependencies.py --target-version 21 --project-dir .
uv run aha-feature/scripts/aha_feature.py lint draft.md --gate elaborated
```

Repository-level linting, type checking, and tests use [uv](https://docs.astral.sh/uv/):

```bash
uv sync --locked
make check
```

