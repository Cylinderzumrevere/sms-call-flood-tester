"""BaseTransport — the contract every SMS/voice transport implements."""
from __future__ import annotations

from abc import ABC, abstractmethod

from flood.bootstrap.session import Session
from flood.config.schema import AppConfig
from flood.core.result import AttemptResult


class BaseTransport(ABC):
    """One transport per protocol (HTTP-SMS, HTTP-Call, SIP)."""

    kind: str = "base"

    def __init__(self, config: AppConfig, session: Session) -> None:
        self.config = config
        self.session = session

    @abstractmethod
    async def send(self, req, index: int) -> AttemptResult:
        """Send one attempt. Must not raise on transport-level errors."""

    async def close(self) -> None:
        """Release pooled connections. Override if the transport holds any."""