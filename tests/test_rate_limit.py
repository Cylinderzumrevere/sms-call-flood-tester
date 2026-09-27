"""Token bucket timing tests."""
from __future__ import annotations

import asyncio
import time

import pytest

from flood.utils.rate_limit import TokenBucket


@pytest.mark.asyncio
async def test_bucket_throttles_to_rate():
    bucket = TokenBucket(rate=100.0, burst=1)
    start = time.monotonic()
    for _ in range(5):
        await bucket.acquire()
    elapsed = time.monotonic() - start
    # 5 tokens at 100/s with burst=1 ≈ 40ms of waiting.
    assert elapsed >= 0.035
    assert elapsed < 0.5


@pytest.mark.asyncio
async def test_burst_allows_immediate_drain():
    bucket = TokenBucket(rate=1.0, burst=10)
    start = time.monotonic()
    for _ in range(10):
        await bucket.acquire()
    assert time.monotonic() - start < 0.05
</｜｜DSML｜｜ parameter>
<｜｜DSML｜｜ parameter name="file_metadata">{