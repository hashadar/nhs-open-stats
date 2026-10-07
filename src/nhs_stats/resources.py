"""Locate contracts and SQL in an installed wheel or a source checkout."""

from __future__ import annotations

from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PACKAGE_DIR.parent.parent


def _resolve(packaged: str, checkout: str) -> Path:
    for candidate in (_PACKAGE_DIR / packaged, _REPO_ROOT / checkout):
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"Could not locate resource directory '{checkout}'")


def contracts_dir() -> Path:
    return _resolve("_contracts", "contracts")


def sql_dir() -> Path:
    return _resolve("_sql", "sql")
