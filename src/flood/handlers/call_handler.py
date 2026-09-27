"""Voice flood handler — builds SIP/HTTP call-setup requests."""
from __future__ import annotations

from flood.models.request import FloodRequest, TargetSpec


def build_call_setup(req: FloodRequest, index: int) -> dict:
    return {
        "destination": req.target.raw,
        "caller_id": req.target.sender or "+10000000000",
        "media": req.payload,
        "tag": f"{req.session_id}-{index}",
    }


def normalize_target(raw: str) -> TargetSpec:
    kind = "call"
    sender = None
    if "@" in raw and raw.startswith("sip:"):
        kind = "sip"
    if "|" in raw:
        raw, sender = raw.split("|", 1)
    return TargetSpec(raw=raw.strip(), kind=kind, sender=sender)