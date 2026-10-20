"""Aim assist: nudges the mouse toward the nearest enemy bone within FOV."""
from __future__ import annotations

import math
from typing import Any

from trainer.config import AimConfig
from trainer.handlers.memory_handler import MemoryHandler
from trainer.models.entities import Entity, EntityList


class AimProcessor:
    def __init__(self, mem: MemoryHandler, cfg: AimConfig) -> None:
        self.mem = mem
        self.cfg = cfg

    def _best_target(self, ents: EntityList, screen_center: tuple[float, float]) -> Entity | None:
        cx, cy = screen_center
        best: Entity | None = None
        best_d = float("inf")
        for e in ents.visible():
            if not e.alive:
                continue
            d = math.hypot(e.screen_x - cx, e.screen_y - cy)
            if d < best_d and d < self.cfg.fov_degrees * 40:
                best, best_d = e, d
        return best

    def process(self, event: dict[str, Any], state) -> dict[str, Any]:
        if not (self.cfg.enabled and state.aim_enabled):
            return event
        if event.get("kind") != "input.delta":
            return event

        ents = EntityList(self.mem)  # refreshed internally
        target = self._best_target(ents, (1920 / 2, 1080 / 2))
        if target is None:
            return event

        dx = (target.screen_x - 960) * self.cfg.smoothing
        dy = (target.screen_y - 540) * self.cfg.smoothing
        event["aim_delta"] = {"dx": dx, "dy": dy, "target_id": target.id}
        return event