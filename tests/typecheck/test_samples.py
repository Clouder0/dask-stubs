from __future__ import annotations

import os
from importlib import metadata
from importlib import resources
from pathlib import Path
from typing import Sequence

import pytest
from mypy import api as mypy_api

SAMPLE_ROOT = Path(__file__).with_suffix("").parent / "samples"
REPO_ROOT = Path(__file__).resolve().parents[2]


def _find_stub_root() -> Path:
    """Locate the installed dask-stubs package path."""
    fallback = REPO_ROOT / "src" / "dask-stubs"
    try:
        dist = metadata.distribution("dask-stubs")
    except metadata.PackageNotFoundError:
        return fallback

    for candidate in ("dask-stubs", "dask-stubs/__init__.pyi"):
        try:
            traversable = Path(str(dist.locate_file(candidate)))
        except FileNotFoundError:
            raise

        try:
            with resources.as_file(traversable) as resolved:
                path = Path(resolved)
        except FileNotFoundError:
            raise

        if candidate.endswith(".pyi"):
            path = path.parent

        if path.exists():
            return path

    return fallback


def _iter_sample_files() -> Sequence[Path]:
    return sorted(SAMPLE_ROOT.glob("*.py"))


@pytest.mark.parametrize("sample_path", _iter_sample_files(), ids=lambda p: p.stem)
def test_sample_typechecks(sample_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    args = [
        "--strict",
        "--hide-error-context",
        "--no-color-output",
        "--namespace-packages",
        "--python-version",
        "3.12",
        str(sample_path),
    ]

    stub_root = str(_find_stub_root())
    existing = os.environ.get("MYPYPATH")
    combined_mypy_path = os.pathsep.join(filter(None, (stub_root, existing)))
    monkeypatch.setenv("MYPYPATH", combined_mypy_path)

    stdout, stderr, status = mypy_api.run(args)
    assert status == 0, stdout + stderr
