"""Pydantic schema for `config.toml`. Validated at load time."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    model_config = {"extra": "forbid"}

    log_level: str = "INFO"
    log_dir: Path = Path("logs")
    proxy_file: Path = Path("proxies.txt")
    rate_per_sec: float = Field(default=50.0, gt=0)
    burst: int = Field(default=100, gt=0)
    timeout_s: float = Field(default=8.0, gt=0)
    retries: int = Field(default=2, ge=0, le=10)
    verify_tls: bool = True
    default_sms_payload: str = "load-test probe"
    default_call_payload: str = "silence/1"
    user_agent: str = "flood-tester/0.6.2"