"""Retry/backoff policy wrapper used by transports."""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def with_retries(
    fn: Callable[[], Awaitable[T]],
    retries: int,
    base_delay: float = 0.25,
) -> T:
    """Run `fn`, retrying on exception with exponential backoff + jitter."""
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return await fn()
        except Exception as exc:  # noqa: BLE001
            last = exc
            if attempt == retries:
                break
            await asyncio.sleep(base_delay * (2**attempt))
    assert last is not None
    raise last