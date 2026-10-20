"""Builds draw commands for the overlay: boxes, health bars, distance."""
from __future__ import annotations

from typing import Any

from trainer.config import EspConfig
from trainer.handlers.memory_handler import MemoryHandler
from trainer.models.entities import EntityList


class EspProcessor:
    def __init__(self, mem: MemoryHandler, cfg: EspConfig) -> None:
        self.mem = mem
        self.cfg = cfg

    def process(self, event: dict[str, Any], state) -> dict[str, Any]:
        if not (self.cfg.enabled and state.esp_enabled):
            return event
        if event.get("kind") != "input.delta":
            return event

        draws: list[dict[str, Any]] = []
        for e in EntityList(self.mem).visible():
            if e.distance_m > self.cfg.max_distance_m:
                continue
            if self.cfg.box:
                draws.append({"type": "box", "x": e.screen_x - 20, "y": e.screen_y - 40,
                              "w": 40, "h": 80, "color": self.cfg.color})
            if self.cfg.health_bar:
                draws.append({"type": "bar", "x": e.screen_x - 22, "y": e.screen_y - 44,
                              "w": 44, "h": 3, "pct": e.health / 100.0,
                              "color": self.cfg.color})
        if draws:
            event["draws"] = draws
        return event