"""Locate contracts in an installed wheel or a source checkout."""

from __future__ import annotations

from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PACKAGE_DIR.parent.parent


def contracts_dir() -> Path:
    packaged = _PACKAGE_DIR / "_contracts"
    checkout = _REPO_ROOT / "contracts"
    for candidate in (packaged, checkout):
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("Could not locate contracts directory")
