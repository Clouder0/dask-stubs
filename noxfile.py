"""Automation entry points for the types-dask project."""

from __future__ import annotations

import os
from pathlib import Path

import nox

nox.needs_version = ">=2024.10.6"
nox.options.sessions = ("lint", "typecheck", "tests")
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_missing_interpreters = False
nox.options.default_venv_backend = "uv"

REPO_ROOT = Path(__file__).parent.resolve()
STUB_ROOT = REPO_ROOT / "src" / "types_dask" / "stubs"


@nox.session
def lint(session: nox.Session) -> None:
    """Run Ruff on the source tree and test samples."""
    session.install("ruff")
    session.run("ruff", "check", "src", "tests", "noxfile.py")


@nox.session
def typecheck(session: nox.Session) -> None:
    """Type check the stub tree using Mypy."""
    session.install("mypy")
    session.run(
        "mypy",
        "src/types_dask/stubs",
        "tests/typecheck/samples",
        env={
            "MYPYPATH": str(STUB_ROOT),
            "PYTHONPATH": str(REPO_ROOT / "src"),
        },
    )


@nox.session
def tests(session: nox.Session) -> None:
    """Run usage-based tests that exercise the stubs."""
    session.install("pytest", "pytest-mypy-plugins", "mypy")
    session.run(
        "pytest",
        "tests",
        env={
            "MYPYPATH": str(STUB_ROOT),
            "PYTHONPATH": os.pathsep.join(
                (os.fsdecode(STUB_ROOT), os.fsdecode(REPO_ROOT / "src"))
            ),
        },
    )
