"""HTTP SMS transport. POSTs to a gateway endpoint per attempt."""
from __future__ import annotations

import httpx

from flood.core.result import AttemptResult
from flood.core.scheduler import with_retries
from flood.core.transport import BaseTransport
from flood.handlers.sms_handler import build_sms_body


class SmsTransport(BaseTransport):
    kind = "sms"

    def __init__(self, config, session) -> None:
        super().__init__(config, session)
        self._client = httpx.AsyncClient(
            timeout=config.timeout_s,
            verify=config.verify_tls,
            headers={"User-Agent": config.user_agent},
            http2=True,
        )

    async def send(self, req, index: int) -> AttemptResult:
        proxy = self.session.proxies.next()
        body = build_sms_body(req, index)
        url = req.target.raw if req.target.raw.startswith("http") else f"https://{req.target.raw}/sms"

        async def attempt() -> httpx.Response:
            return await self._client.post(url, json=body, proxy=proxy)

        try:
            resp = await with_retries(attempt, self.config.retries)
        except httpx.TimeoutException:
            return AttemptResult(index, "timeout")
        except httpx.HTTPError as exc:
            return AttemptResult(index, "error", detail=str(exc))

        status = "ok" if resp.status_code < 400 else "blocked"
        return AttemptResult(index, status, detail=f"HTTP {resp.status_code}")

    async def close(self) -> None:
        await self._client.aclose()