"""Transport registry. Maps `kind` strings to transport classes."""
from __future__ import annotations

from flood.core.transport import BaseTransport
from flood.services.sms_transport import SmsTransport
from flood.services.call_transport import CallTransport
from flood.services.sip_transport import SipTransport

_REGISTRY: dict[str, type[BaseTransport]] = {
    "sms": SmsTransport,
    "call": CallTransport,
    "sip": SipTransport,
}


def get_transport(kind: str) -> type[BaseTransport]:
    try:
        return _REGISTRY[kind]
    except KeyError as exc:
        raise ValueError(f"unknown transport kind: {kind!r}") from exc


def available() -> list[str]:
    return sorted(_REGISTRY)