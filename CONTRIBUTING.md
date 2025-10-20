# Contributing

Thanks for your interest in making the typing story for Dask better! This guide
outlines the conventions used in this repository.

## Getting started

1. **Create a virtual environment** with Python 3.12+ (e.g. `uv venv`).
2. **Install dependencies** using `uv sync --group dev`.
3. **Run the automation** with `uv run nox` to confirm the baseline is green before
   making changes.

## Workflow

1. Work on a focused branch per logical change.
2. Write or extend a usage-based sample under `tests/typecheck/samples/` that
   proves the new stubs behave as expected.
3. Keep commits tidy—separate structural cleanup from functional annotation
   changes.
4. Run `uv run nox` locally and make sure everything passes before opening a pull
   request.

## Styling guidelines

- Type stubs live in `src/types_dask/stubs/`. Mirror the module layout from the
  runtime package (`dask`, `distributed`, etc.).
- Prefer precise typing over `Any`, but do not guess—`Any` with a `TODO` is
  better than an incorrect signature.
- Use re-export stubs (i.e. `from .module import Class as Class`) to match the
  runtime public API.
- Add succinct comments when a type uses a non-obvious technique or mirrors a
  quirky runtime behavior.

## Tests and automation

`nox` coordinates the following tasks and can be driven through `uv run`:

- **`lint`**: runs Ruff on the repository sources.
- **`typecheck`**: type checks the stub tree with Mypy.
- **`tests`**: executes the usage samples with `pytest` (each sample is a `.py`
  file validated via mypy).

You can run individual sessions via `uv run nox -s lint`, etc. The default
`uv run nox` executes them all.

## Opening pull requests

- Fill in the PR template (when available) with context about the API surface
  you touched.
- Link to upstream Dask documentation or source that verifies the signatures.
- If your change intentionally diverges from the runtime behavior, call that out
  explicitly in the PR body so reviewers understand the trade-off.

We appreciate your contributions and review energy!***
