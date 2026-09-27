"""Load and validate `config.toml`, falling back to defaults."""
from __future__ import annotations

import os
import tomllib
from pathlib import Path

from flood.config.schema import AppConfig


def load_config(path: Path) -> AppConfig:
    """Read TOML config. Missing file → defaults. Env overrides win."""
    data: dict = {}
    if path.is_file():
        with path.open("rb") as fh:
            data = tomllib.load(fh)

    if v := os.getenv("FLOOD_LOG_LEVEL"):
        data["log_level"] = v
    if v := os.getenv("FLOOD_RATE"):
        data["rate_per_sec"] = float(v)
    if v := os.getenv("FLOOD_PROXY_FILE"):
        data["proxy_file"] = Path(v)

    return AppConfig.model_validate(data)