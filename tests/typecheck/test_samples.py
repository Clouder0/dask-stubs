from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence

import pytest
from mypy import api as mypy_api

from types_dask import get_stub_root


SAMPLE_ROOT = Path(__file__).with_suffix("").parent / "samples"


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

    stub_root = str(get_stub_root())
    existing = os.environ.get("MYPYPATH")
    combined_mypy_path = os.pathsep.join(filter(None, (stub_root, existing)))
    monkeypatch.setenv("MYPYPATH", combined_mypy_path)

    stdout, stderr, status = mypy_api.run(args)
    assert status == 0, stdout + stderr
