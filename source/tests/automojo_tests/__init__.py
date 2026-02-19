"""
    Test package bootstrap helpers.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType


def _ensure_packages_on_path() -> None:
    """
        Adds the source/packages directory to sys.path for unittest imports.
    """
    source_dir = Path(__file__).resolve().parents[2]
    packages_dir = source_dir / "packages"
    packages_str = str(packages_dir)
    if packages_dir.is_dir() and packages_str not in sys.path:
        sys.path.insert(0, packages_str)


def _ensure_error_stubs() -> None:
    """
        Provides lightweight ``automojo.errors`` stubs when the dependency is unavailable.
    """
    try:
        importlib.import_module("automojo.errors.exceptions")
    except ModuleNotFoundError:
        automojo_pkg = importlib.import_module("automojo")
        errors_pkg = ModuleType("automojo.errors")
        exceptions_mod = ModuleType("automojo.errors.exceptions")

        class ConfigurationError(Exception):
            """Fallback ConfigurationError for tests."""

        class SemanticError(Exception):
            """Fallback SemanticError for tests."""

        exceptions_mod.ConfigurationError = ConfigurationError
        exceptions_mod.SemanticError = SemanticError
        errors_pkg.exceptions = exceptions_mod

        sys.modules["automojo.errors"] = errors_pkg
        sys.modules["automojo.errors.exceptions"] = exceptions_mod
        setattr(automojo_pkg, "errors", errors_pkg)


_ensure_packages_on_path()
_ensure_error_stubs()
