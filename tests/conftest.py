"""Shared fixtures for the Java dependency analyzer tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "java-version-upgrade"
    / "scripts"
    / "analyze_java_dependencies.py"
)


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
