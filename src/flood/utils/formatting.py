"""Small formatting helpers for CLI output and log lines."""
from __future__ import annotations


def human_rate(per_sec: float) -> str:
    if per_sec >= 1000:
        return f"{per_sec / 1000:.1f}k/s"
    return f"{per_sec:.1f}/s"


def truncate(s: str, width: int = 48) -> str:
    return s if len(s) <= width else s[: width - 1] + "…"