# Repository Guidelines

## Project Structure & Module Organization

The stub package lives under `src/dasktyping`. Place public `.pyi` stubs inside `src/dasktyping/stubs`, mirroring the runtime package structure (for example, `stubs/delayed/__init__.pyi`). Annotated usage samples and fixtures for validation live in `tests/typecheck/samples`, while entry points for automation and settings reside in `noxfile.py`, `pyproject.toml`, and `pyrightconfig.json`. Keep generated artifacts in `build/` and leave transient caches untracked.

## Build, Test, and Development Commands

Install tooling with `uv sync --group dev`; run everything through the managed environment. Use `UV_CACHE_DIR=.uv-cache uv run nox -s lint` for style checks, `uv run nox -s typecheck` for direct mypy validation of stubs and samples, and `uv run nox` to execute the full suite. When iterating locally, activate `.venv` via `source .venv/bin/activate` so `uv run` reuses the cached interpreter and packages.

## Coding Style & Naming Conventions

Target Python 3.12+ semantics with 4-space indentation. Stub files must use `.pyi` extensions and mirror their import paths. Prefer explicit re-exports and keep `__all__` aligned with public names. Run `ruff check` before committing and address diagnostics rather than suppressing, unless the Dask API requires a deliberate exception.

## Testing Guidelines

We rely on `pytest` plus `pytest-mypy-plugins` to assert that stubbed APIs behave as expected. Add runnable examples to `tests/typecheck/samples` (for example, `delayed_usage.py`) and reference them from `tests/typecheck/test_samples.py`. Name new tests after the feature under validation and ensure they fail without the accompanying stub change. Use the sample suite to lock regression coverage for Dask collections, delayed values, and distributed futures. `uv run nox -s tests` runs the same checks executed in continuous integration.

## Commit & Pull Request Guidelines

Follow Conventional Commit prefixes (`feat`, `fix`, `docs`, `test`, `chore`) and keep subject lines under 72 characters. Each commit should bundle a coherent change to the stubs or tooling. Pull requests must describe the affected Dask APIs, note any remaining typing gaps, and link upstream issues when available. Include before-and-after mypy output or IDE screenshots if they demonstrate improved typing coverage.

## IDE & Agent Tips

For VS Code with Pylance, set `"python.analysis.stubPath": ["src/dasktyping/stubs"]` in workspace settings or `pyrightconfig.json`. When running automated agents, export `UV_CACHE_DIR=.uv-cache` to avoid permission errors and drive all automation through `uv run` to respect the locked dependency set. Prefer submitting typed callables over lambdas when checking distributed futures to keep type inference precise.
