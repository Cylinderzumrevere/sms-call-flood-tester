"""Engine smoke tests — no network. Uses a stub transport."""
from __future__ import annotations

import pytest

from flood.bootstrap.session import Session
from flood.config.schema import AppConfig
from flood.core.engine import FloodEngine
from flood.core.result import AttemptResult
from flood.models.request import FloodRequest, TargetSpec


class _StubTransport:
    kind = "sms"

    def __init__(self, config, session) -> None:
        self.session = session

    async def send(self, req, index: int) -> AttemptResult:
        return AttemptResult(index, "ok")

    async def close(self) -> None:
        return None


@pytest.mark.asyncio
async def test_engine_counts_all_attempts(monkeypatch):
    monkeypatch.setattr("flood.core.engine.get_transport", lambda kind: _StubTransport)
    cfg = AppConfig(rate_per_sec=10_000, burst=10_000)
    session = Session.create(cfg)
    engine = FloodEngine(cfg, session)
    req = FloodRequest(
        kind="sms",
        target=TargetSpec(raw="https://example.test/sms"),
        count=50,
        concurrency=8,
    )
    summary = await engine.run(req)
    assert summary.total == 50
    assert summary.by_status.get("ok") == 50