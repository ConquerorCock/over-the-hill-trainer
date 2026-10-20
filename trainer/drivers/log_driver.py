"""Logs a compact summary of each pipeline event."""
from __future__ import annotations

import logging
from typing import Any

log = logging.getLogger("events")


class LogDriver:
    def __init__(self, level: str = "INFO") -> None:
        log.setLevel(level)

    def emit(self, event: dict[str, Any]) -> None:
        kind = event.get("kind")
        if kind == "toggle":
            log.info("toggle %s -> %s", event.get("feature"), event.get("value"))
        elif kind == "panic":
            log.warning("panic hotkey pressed")
        elif "draws" in event:
            log.debug("esp draws=%d", len(event["draws"]))