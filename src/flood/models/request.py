"""FloodRequest and TargetSpec — the engine's input contract."""
from __future__ import annotations

import uuid
from typing import Literal

from pydantic import BaseModel, Field


class TargetSpec(BaseModel):
    raw: str
    kind: Literal["sms", "call", "sip"] = "sms"
    sender: str | None = None


class FloodRequest(BaseModel):
    kind: Literal["sms", "call", "sip"]
    target: TargetSpec
    count: int = Field(gt=0, le=1_000_000)
    concurrency: int = Field(gt=0, le=2048)
    payload: str = "load-test probe"
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))