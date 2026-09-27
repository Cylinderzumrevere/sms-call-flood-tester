"""Batch handler — expands a target file into many FloodRequests."""
from __future__ import annotations

from pathlib import Path

from flood.models.request import FloodRequest


def load_targets(path: Path) -> list[str]:
    if not path.is_file():
        return []
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def fan_out(base: FloodRequest, targets: list[str]) -> list[FloodRequest]:
    return [
        base.model_copy(update={"target": base.target.model_copy(update={"raw": t})})
        for t in targets
    ]