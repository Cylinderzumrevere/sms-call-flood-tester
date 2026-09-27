"""FloodEngine — orchestrates workers, rate limiting, and result collection.

Inputs: `AppConfig`, `Session`, `FloodRequest`.
Outputs: `RunSummary` with per-status counts and latency percentiles.
Concurrency: N asyncio workers gated by a token bucket and a semaphore.
Errors: transport exceptions are caught per-attempt and counted, never
propagated — a single dead proxy must not kill the run.
"""
from __future__ import annotations

import asyncio
import logging
import time
from collections import Counter

from flood.bootstrap.session import Session
from flood.config.registry import get_transport
from flood.config.schema import AppConfig
from flood.core.result import AttemptResult, RunSummary

log = logging.getLogger(__name__)


class FloodEngine:
    def __init__(self, config: AppConfig, session: Session) -> None:
        self.config = config
        self.session = session

    async def run(self, req) -> RunSummary:
        transport_cls = get_transport(req.kind)
        transport = transport_cls(self.config, self.session)
        sem = asyncio.Semaphore(req.concurrency)
        results: list[AttemptResult] = []
        started = time.perf_counter()

        async def one(i: int) -> None:
            async with sem:
                await self.session.limiter.acquire()
                t0 = time.perf_counter()
                try:
                    res = await transport.send(req, i)
                except Exception as exc:  # noqa: BLE001 — counted, not raised
                    res = AttemptResult(i, "error", 0.0, repr(exc))
                res.latency_ms = (time.perf_counter() - t0) * 1000.0
                results.append(res)

        try:
            await asyncio.gather(*(one(i) for i in range(req.count)))
        finally:
            await transport.close()

        elapsed = time.perf_counter() - started
        return self._summarize(results, elapsed)

    def _summarize(self, results: list[AttemptResult], elapsed: float) -> RunSummary:
        by_status = Counter(r.status for r in results)
        latencies = sorted(r.latency_ms for r in results if r.status == "ok")
        p50 = latencies[len(latencies) // 2] if latencies else 0.0
        p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0.0
        return RunSummary(
            session_id=self.session.id,
            total=len(results),
            by_status=dict(by_status),
            elapsed_s=elapsed,
            p50_ms=p50,
            p99_ms=p99,
        )