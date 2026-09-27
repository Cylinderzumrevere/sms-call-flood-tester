"""Round-robin proxy pool loaded from a text file."""
from __future__ import annotations

import itertools
import logging
from pathlib import Path

log = logging.getLogger(__name__)


class ProxyPool:
    def __init__(self, proxies: list[str]) -> None:
        self._proxies = proxies
        self._cycle = itertools.cycle(proxies) if proxies else None

    @classmethod
    def from_file(cls, path: Path) -> "ProxyPool":
        if not path.is_file():
            log.warning("proxy file %s missing — running direct", path)
            return cls([])
        lines = [
            ln.strip()
            for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")
        ]
        log.info("loaded %d proxies", len(lines))
        return cls(lines)

    def next(self) -> str | None:
        return next(self._cycle) if self._cycle else None

    def __len__(self) -> int:
        return len(self._proxies)