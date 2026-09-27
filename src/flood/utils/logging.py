"""Logging setup — file + rich console, no `print` anywhere else."""
from __future__ import annotations

import logging
from pathlib import Path

from rich.logging import RichHandler


def configure_logging(level: str, log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers.clear()

    console = RichHandler(rich_tracebacks=True, show_path=False)
    console.setLevel(level.upper())
    root.addHandler(console)

    file_handler = logging.FileHandler(log_dir / "flood.log", encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s")
    )
    root.addHandler(file_handler)

    logging.getLogger("httpx").setLevel("WARNING")