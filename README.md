# dasktyping

`dasktyping` provides third-party typing information for the Dask project. The
goal is to fill the gaps left by the runtime package so that type checkers such
as Mypy and Pyright can reason about typical Dask usage with confidence.

## Project layout

The repository separates runtime helpers from the stub definitions:

- `src/dasktyping/stubs/` holds `.pyi` files that mirror the public Dask API.
- `tests/typecheck/samples/` provides runtime-free Python snippets that mypy
  validates to guard the stubs.
- `noxfile.py` defines automation for linting, type checking, and stub sanity
  checks.

## Quick start

1. Install development dependencies with `uv` (Python 3.12+):

   ```bash
   uv sync --group dev
   ```

2. Run the default automation via `uv`:

   ```bash
   uv run nox
   ```

   This runs Ruff, Mypy against the stubs, and the sample type-check tests.

## Contribution guidelines

1. Prefer working against small slices of the API. It is easier to review and
   iterate on focused modules.
2. Each new stub should be paired with a usage example under
   `tests/typecheck/samples/` (tested via mypy).
3. Keep the stubs faithful to the runtime signatures. Where the runtime is
   dynamic, fall back to `Any` but leave a `TODO` for future improvement.
4. Run the full `uv run nox` suite before sending a pull request.

See `CONTRIBUTING.md` for more detail on project conventions and coding
standards.
