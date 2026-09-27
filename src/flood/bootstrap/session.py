"""Session object: per-run identity, proxy pool, rate limiter, counters."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from flood.config.schema import AppConfig
from flood.services.proxy_pool import ProxyPool
from flood.utils.rate_limit import TokenBucket


@dataclass(slots=True)
class Session:
    """Mutable per-run state. One session per `flood` invocation."""

    id: str
    started_at: datetime
    config: AppConfig
    proxies: ProxyPool
    limiter: TokenBucket
    counters: dict[str, int] = field(default_factory=dict)

    @classmethod
    def create(cls, config: AppConfig) -> "Session":
        return cls(
            id=str(uuid.uuid4()),
            started_at=datetime.now(tz=timezone.utc),
            config=config,
            proxies=ProxyPool.from_file(config.proxy_file),
            limiter=TokenBucket(rate=config.rate_per_sec, burst=config.burst),
            counters={"sent": 0, "failed": 0, "blocked": 0},
        )

    def bump(self, key: str, n: int = 1) -> None:
        self.counters[key] = self.counters.get(key, 0) + n