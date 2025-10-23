from __future__ import annotations

import pytest
from importlib import util
from pathlib import Path


class _FakeClient:
    def __init__(self, *, asynchronous: bool | None = None, **kwargs):
        self.asynchronous = bool(asynchronous)
        self._closed = False

    def persist(self, value, **kwargs):
        return value

    async def compute(self, value):
        if hasattr(value, "compute"):
            return value.compute(scheduler="sync")
        return value

    def close(self):
        if self.asynchronous:

            async def _closer() -> None:
                self._closed = True

            return _closer()
        self._closed = True
        return None

    def __await__(self):
        async def _await_self() -> _FakeClient:
            self.asynchronous = True
            return self

        return _await_self().__await__()

    async def __aenter__(self) -> _FakeClient:
        self.asynchronous = True
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        closer = self.close()
        if closer is not None:
            await closer


_SAMPLE_MODULE_NAME = "distributed_client_async_creation_runtime"
_SAMPLE_PATH = (
    Path(__file__).resolve().parents[1]
    / "typecheck"
    / "samples"
    / "distributed_client_async_creation.py"
)

_spec = util.spec_from_file_location(_SAMPLE_MODULE_NAME, _SAMPLE_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Unable to load sample module from {_SAMPLE_PATH}")

_module = util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

ClusterUnavailable = getattr(_module, "ClusterUnavailable")
await_client_creation = getattr(_module, "await_client_creation")
use_async_context_manager = getattr(_module, "use_async_context_manager")
persist_without_await = getattr(_module, "persist_without_await")
create_sync_client = getattr(_module, "create_sync_client")


@pytest.mark.asyncio
async def test_async_client_examples() -> None:
    await await_client_creation()
    await use_async_context_manager()
    await persist_without_await()


def test_sync_client_example() -> None:
    create_sync_client()
