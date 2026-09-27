"""Typer entry point for the flood-tester desktop CLI.

Wires user input to the core engine. Holds no business logic itself —
every command builds a `FloodRequest` and hands it to `FloodEngine`.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import typer
from rich.console import Console

from flood.bootstrap.session import Session
from flood.config.loader import load_config
from flood.core.engine import FloodEngine
from flood.models.request import FloodRequest, TargetSpec
from flood.utils.logging import configure_logging

app = typer.Typer(
    name="flood",
    help="SMS & voice gateway flood tester (authorized targets only).",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.command("sms")
def sms(
    target: str = typer.Option(..., "--target", "-t", help="E.164 number or gateway URL"),
    count: int = typer.Option(500, "--count", "-c", help="Messages to send"),
    concurrency: int = typer.Option(32, "--concurrency", "-j", help="Parallel workers"),
    config: Path = typer.Option(Path("config.toml"), "--config", "-f"),
) -> None:
    """Flood an SMS gateway with a fixed payload."""
    cfg = load_config(config)
    configure_logging(cfg.log_level, cfg.log_dir)
    req = FloodRequest(
        kind="sms",
        target=TargetSpec(raw=target, kind="sms"),
        count=count,
        concurrency=concurrency,
        payload=cfg.default_sms_payload,
    )
    _run(req, cfg)


@app.command("call")
def call(
    target: str = typer.Option(..., "--target", "-t", help="E.164 number or SIP URI"),
    count: int = typer.Option(200, "--count", "-c", help="Calls to place"),
    concurrency: int = typer.Option(16, "--concurrency", "-j"),
    config: Path = typer.Option(Path("config.toml"), "--config", "-f"),
) -> None:
    """Flood a voice gateway with call setup attempts."""
    cfg = load_config(config)
    configure_logging(cfg.log_level, cfg.log_dir)
    req = FloodRequest(
        kind="call",
        target=TargetSpec(raw=target, kind="call"),
        count=count,
        concurrency=concurrency,
        payload=cfg.default_call_payload,
    )
    _run(req, cfg)


def _run(req: FloodRequest, cfg) -> None:
    session = Session.create(cfg)
    engine = FloodEngine(cfg, session)
    try:
        summary = asyncio.run(engine.run(req))
    except KeyboardInterrupt:
        console.print("[yellow]interrupted[/yellow]")
        sys.exit(130)
    console.print(summary.render())


def main() -> None:
    app()


if __name__ == "__main__":
    main()