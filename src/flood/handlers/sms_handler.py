"""SMS flood handler — builds the request body for an SMS gateway."""
from __future__ import annotations

from flood.models.request import FloodRequest, TargetSpec


def build_sms_body(req: FloodRequest, index: int) -> dict:
    return {
        "to": req.target.raw,
        "from": req.target.sender or "FLOOD",
        "body": f"{req.payload} #{index}",
        "idempotency_key": f"{req.session_id}-{index}",
    }


def normalize_target(raw: str) -> TargetSpec:
    kind = "sms"
    sender = None
    if "|" in raw:
        raw, sender = raw.split("|", 1)
    return TargetSpec(raw=raw.strip(), kind=kind, sender=sender)