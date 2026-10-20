"""Entity views read from game memory."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from trainer.handlers.memory_handler import MemoryHandler

log = logging.getLogger("entities")


@dataclass
class Entity:
    id: int
    screen_x: float
    screen_y: float
    distance_m: float
    health: int
    alive: bool
    team: int = 0

    @property
    def is_enemy(self) -> bool:
        return self.team != 0


class EntityList:
    """Lazily refreshes from the game's entity manager on first access."""

    def __init__(self, mem: MemoryHandler) -> None:
        self.mem = mem
        self._items: list[Entity] = []
        self._refresh()

    def _refresh(self) -> None:
        try:
            self.mem.attach()
            # Real implementation walks the entity manager chain.
            # Placeholder returns an empty list until offsets are wired.
            self._items = []
        except Exception as exc:
            log.debug("entity refresh failed: %s", exc)
            self._items = []

    def visible(self) -> list[Entity]:
        return [e for e in self._items if e.alive and e.is_enemy]