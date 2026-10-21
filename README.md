# skills

Agentic AI skills.

More context and examples: [agentskills.io](https://agentskills.io/).

Summary: a curated set of reusable skill docs, references, and scripts for building, documenting, and upgrading AI agent workflows.

## Development

Python helper scripts carry [PEP 723](https://peps.python.org/pep-0723/) metadata, so a script can run in an isolated environment without installing anything globally:

```bash
uv run java-version-upgrade/scripts/analyze_java_dependencies.py --target-version 21 --project-dir .
```

Repository-level linting, type checking, and tests use [uv](https://docs.astral.sh/uv/):

```bash
uv sync --locked
make check
```

