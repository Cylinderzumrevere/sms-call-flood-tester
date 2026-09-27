"""Async token bucket. One instance per session, shared by all workers."""
from __future__ import annotations

import asyncio
import time


class TokenBucket:
    """Refills `rate` tokens/sec up to `burst`. `acquire()` blocks."""

    def __init__(self, rate: float, burst: int) -> None:
        self.rate = rate
        self.capacity = float(burst)
        self._tokens = float(burst)
        self._updated = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, n: float = 1.0) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                self._tokens = min(self.capacity, self._tokens + (now - self._updated) * self.rate)
                self._updated = now
                if self._tokens >= n:
                    self._tokens -= n
                    return
                deficit = (n - self._tokens) / self.rate
                await asyncio.sleep(deficit)