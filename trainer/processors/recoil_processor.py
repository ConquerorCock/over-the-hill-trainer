"""Counteracts weapon recoil by injecting downward mouse deltas."""
from __future__ import annotations

from typing import Any

from trainer.config import RecoilConfig
from trainer.handlers.memory_handler import MemoryHandler

_PATTERNS = {
    "ak": [(-0.4, 0.9), (-0.3, 0.8), (-0.2, 0.7), (-0.1, 0.6)],
    "m4": [(-0.2, 0.5), (-0.15, 0.45), (-0.1, 0.4), (-0.05, 0.35)],
    "smg": [(-0.1, 0.3), (-0.08, 0.28), (-0.06, 0.25), (-0.04, 0.22)],
}


class RecoilProcessor:
    def __init__(self, mem: MemoryHandler, cfg: RecoilConfig) -> None:
        self.mem = mem
        self.cfg = cfg
        self._shot_idx = 0

    def _pattern(self) -> list[tuple[float, float]]:
        if self.cfg.pattern in _PATTERNS:
            return _PATTERNS[self.cfg.pattern]
        return _PATTERNS["m4"]

    def process(self, event: dict[str, Any], state) -> dict[str, Any]:
        if not (self.cfg.enabled and state.recoil_enabled):
            return event
        if event.get("kind") != "input.delta":
            return event

        pat = self._pattern()
        idx = self._shot_idx % len(pat)
        dx, dy = pat[idx]
        self._shot_idx += 1
        event["recoil_delta"] = {"dx": dx * self.cfg.strength, "dy": dy * self.cfg.strength}
        return event