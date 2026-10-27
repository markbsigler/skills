"""Shared fixtures for the skill script tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent

SCRIPT = ROOT / "java-version-upgrade" / "scripts" / "analyze_java_dependencies.py"

# The aha-feature scripts import each other as top-level modules, as they do when run directly.
AHA_FEATURE_SCRIPTS = ROOT / "aha-feature" / "scripts"
if str(AHA_FEATURE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AHA_FEATURE_SCRIPTS))


def load_analyzer() -> ModuleType:
    """Load the hyphenated tree's standalone analyzer as a module."""
    spec = importlib.util.spec_from_file_location("analyze_java_dependencies", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def analyzer_module() -> Any:
    return load_analyzer()
