"""Shared fixtures for the skill script tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The aha-feature scripts import each other as top-level modules, as they do when run directly.
AHA_FEATURE_SCRIPTS = ROOT / "aha-feature" / "scripts"
if str(AHA_FEATURE_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(AHA_FEATURE_SCRIPTS))
