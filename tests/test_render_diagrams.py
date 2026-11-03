"""Tests for codebase-diagrams/scripts/render_diagrams.sh, using a stub Mermaid CLI."""

from __future__ import annotations

import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent / "codebase-diagrams" / "scripts" / "render_diagrams.sh"
)

pytestmark = pytest.mark.skipif(
    sys.platform == "win32" or shutil.which("bash") is None, reason="needs bash"
)

# Stand-in for mmdc: logs its arguments, fails on diagrams containing BROKEN, and otherwise
# writes the requested output file.
STUB = """#!/usr/bin/env bash
echo "$@" >> "$STUB_LOG"
input="" output=""
while [ $# -gt 0 ]; do
  case "$1" in
    -i) input="$2"; shift 2 ;;
    -o) output="$2"; shift 2 ;;
    *) shift ;;
  esac
done
if grep -q BROKEN "$input"; then
  for n in $(seq 1 20); do echo "parse error detail line $n" >&2; done
  exit 1
fi
: > "$output"
"""

# Tools the script itself calls, so a PATH without mmdc and npx can still run it.
SCRIPT_TOOLS = ("bash", "cat", "mktemp", "rm", "basename", "head", "sed", "dirname")


def make_executable(path: Path, body: str) -> None:
    path.write_text(body)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


class Env:
    def __init__(self, root: Path) -> None:
        self.bin = root / "bin"
        self.bin.mkdir()
        self.log = root / "stub.log"
        self.diagrams = root / "diagrams"
        self.diagrams.mkdir()
        for tool in (*SCRIPT_TOOLS, "grep", "seq"):
            found = shutil.which(tool)
            assert found is not None, tool
            (self.bin / tool).symlink_to(found)

    def add_stub(self, name: str) -> None:
        if name == "npx":
            # npx forwards to the same stub, dropping the --yes flag and package spec.
            body = '#!/usr/bin/env bash\necho "npx $@" >> "$STUB_LOG"\nshift 2\n'
            body += f'exec "{self.bin}/mmdc-stub" "$@"\n'
            make_executable(self.bin / "mmdc-stub", STUB)
            make_executable(self.bin / "npx", body)
        else:
            make_executable(self.bin / name, STUB)

    def diagram(self, name: str, content: str = "flowchart TD\n  A --> B\n") -> Path:
        path = self.diagrams / f"{name}.mmd"
        path.write_text(content)
        return path

    def run(
        self, *args: str, extra_env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        env = {"PATH": str(self.bin), "STUB_LOG": str(self.log), "HOME": str(self.bin)}
        env.update(extra_env or {})
        return subprocess.run(
            [str(self.bin / "bash"), str(SCRIPT), *args],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

    def logged_calls(self) -> list[str]:
        return self.log.read_text().splitlines() if self.log.exists() else []


@pytest.fixture
def env(tmp_path: Path) -> Env:
    e = Env(tmp_path)
    e.add_stub("mmdc")
    return e


def test_help_exits_zero_and_documents_exit_codes(env: Env) -> None:
    result = env.run("--help")
    assert result.returncode == 0
    assert "--check" in result.stdout
    assert "Exit codes" in result.stdout


def test_unknown_option_is_a_usage_error(env: Env) -> None:
    result = env.run("--bogus")
    assert result.returncode == 2
    assert "unknown option" in result.stderr


def test_second_directory_is_a_usage_error(env: Env) -> None:
    result = env.run(str(env.diagrams), "other")
    assert result.returncode == 2
    assert "only one diagram directory" in result.stderr


def test_missing_directory_exits_two(env: Env) -> None:
    result = env.run(str(env.diagrams / "nope"))
    assert result.returncode == 2
    assert "directory not found" in result.stderr


def test_directory_without_diagrams_exits_two(env: Env) -> None:
    result = env.run(str(env.diagrams))
    assert result.returncode == 2
    assert "no .mmd files" in result.stderr


def test_missing_mermaid_cli_and_npx_exits_two(tmp_path: Path) -> None:
    bare = Env(tmp_path)  # no stubs: neither mmdc nor npx is on PATH
    bare.diagram("a")
    result = bare.run(str(bare.diagrams))
    assert result.returncode == 2
    assert "mmdc or Node.js" in result.stderr


def test_renders_every_diagram_to_png(env: Env) -> None:
    env.diagram("a")
    env.diagram("b")
    result = env.run(str(env.diagrams))
    assert result.returncode == 0
    assert (env.diagrams / "a.png").exists()
    assert (env.diagrams / "b.png").exists()
    assert "2 succeeded, 0 failed" in result.stdout


def test_failure_exits_one_but_still_renders_the_rest(env: Env) -> None:
    env.diagram("good")
    env.diagram("bad", "BROKEN")
    result = env.run(str(env.diagrams))
    assert result.returncode == 1
    assert (env.diagrams / "good.png").exists()
    assert not (env.diagrams / "bad.png").exists()
    assert "FAILED  bad.mmd" in result.stderr
    assert "1 succeeded, 1 failed" in result.stdout


def test_error_output_is_trimmed(env: Env) -> None:
    env.diagram("bad", "BROKEN")
    result = env.run(str(env.diagrams))
    assert "parse error detail line 1" in result.stderr
    assert "parse error detail line 20" not in result.stderr


def test_check_mode_writes_nothing_to_the_diagram_directory(env: Env) -> None:
    env.diagram("a")
    result = env.run("--check", str(env.diagrams))
    assert result.returncode == 0
    assert sorted(p.name for p in env.diagrams.iterdir()) == ["a.mmd"]
    assert ".svg" in env.logged_calls()[0]


def test_check_mode_reports_failures(env: Env) -> None:
    env.diagram("bad", "BROKEN")
    result = env.run("--check", str(env.diagrams))
    assert result.returncode == 1
    assert "FAILED  bad.mmd" in result.stderr


def test_puppeteer_config_is_passed_through(env: Env) -> None:
    env.diagram("a")
    env.run(str(env.diagrams), extra_env={"RENDER_PUPPETEER_CONFIG": "/tmp/p.json"})
    assert "-p /tmp/p.json" in env.logged_calls()[0]


def test_no_puppeteer_flag_by_default(env: Env) -> None:
    env.diagram("a")
    env.run(str(env.diagrams))
    assert "-p " not in env.logged_calls()[0]


def test_render_settings_come_from_environment(env: Env) -> None:
    env.diagram("a")
    env.run(
        str(env.diagrams),
        extra_env={"RENDER_WIDTH": "100", "RENDER_HEIGHT": "50", "RENDER_SCALE": "3"},
    )
    call = env.logged_calls()[0]
    assert "--width 100" in call
    assert "--height 50" in call
    assert "--scale 3" in call


def test_falls_back_to_pinned_npx_without_global_install(tmp_path: Path) -> None:
    e = Env(tmp_path)
    e.add_stub("npx")
    e.diagram("a")
    result = e.run(str(e.diagrams))
    assert result.returncode == 0
    assert (e.diagrams / "a.png").exists()
    npx_call = e.logged_calls()[0]
    assert npx_call.startswith("npx --yes @mermaid-js/mermaid-cli@")
    assert "latest" not in npx_call
