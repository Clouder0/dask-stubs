"""Package helpers for the types-dask project."""

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Iterable

__all__ = ["iter_stub_files", "get_stub_root"]


def get_stub_root() -> Path:
    """Return the filesystem location of the bundled stub tree."""
    return Path(resources.files(__package__)) / "stubs"


def iter_stub_files(suffix: str = ".pyi") -> Iterable[Path]:
    """Yield stub files contained in the project."""
    root = get_stub_root()
    for path in root.rglob(f"*{suffix}"):
        if path.is_file():
            yield path
