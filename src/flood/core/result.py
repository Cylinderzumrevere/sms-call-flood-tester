"""Result and summary dataclasses returned by the engine."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AttemptResult:
    index: int
    status: str          # "ok" | "blocked" | "timeout" | "error"
    latency_ms: float = 0.0
    detail: str = ""


@dataclass(slots=True)
class RunSummary:
    session_id: str
    total: int
    by_status: dict[str, int] = field(default_factory=dict)
    elapsed_s: float = 0.0
    p50_ms: float = 0.0
    p99_ms: float = 0.0

    def render(self) -> str:
        rate = self.total / self.elapsed_s if self.elapsed_s else 0.0
        lines = [
            f"session   {self.session_id}",
            f"total     {self.total}",
            f"elapsed   {self.elapsed_s:.2f}s ({rate:.1f}/s)",
            f"p50/p99   {self.p50_ms:.1f}ms / {self.p99_ms:.1f}ms",
        ]
        for status, n in sorted(self.by_status.items()):
            lines.append(f"  {status:<8} {n}")
        return "\n".join(lines)