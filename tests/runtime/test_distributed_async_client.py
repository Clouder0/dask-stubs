from __future__ import annotations

from importlib import util
from pathlib import Path

import pytest

_SAMPLE_MODULE_NAME = "distributed_client_async_creation_runtime"
_SAMPLE_PATH = (
    Path(__file__).resolve().parents[1]
    / "typecheck"
    / "samples"
    / "distributed_client_async_creation.py"
)


def _load_sample_module() -> object:
    spec = util.spec_from_file_location(_SAMPLE_MODULE_NAME, _SAMPLE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load sample module from {_SAMPLE_PATH}")

    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


try:
    _sample = _load_sample_module()
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
    raise RuntimeError(f"Runtime Dask/Distributed required: {exc}") from exc

ClusterUnavailable = getattr(_sample, "ClusterUnavailable")
await_client_creation = getattr(_sample, "await_client_creation")
use_async_context_manager = getattr(_sample, "use_async_context_manager")
persist_without_await = getattr(_sample, "persist_without_await")
create_sync_client = getattr(_sample, "create_sync_client")


@pytest.mark.asyncio
async def test_async_client_examples() -> None:
    await await_client_creation()
    await use_async_context_manager()
    await persist_without_await()


def test_sync_client_example() -> None:
    create_sync_client()
