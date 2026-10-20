"""Wraps pymem to expose resolved pointers for the game process."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pymem
import yaml

log = logging.getLogger("memory")


class MemoryHandler:
    def __init__(self, process_name: str, signatures_path: str) -> None:
        self.process_name = process_name
        self.signatures_path = Path(signatures_path)
        self._pm: pymem.Pymem | None = None
        self._base: int = 0
        self._offsets: dict[str, int] = {}

    def attach(self) -> None:
        if self._pm is not None:
            return
        self._pm = pymem.Pymem(self.process_name)
        self._base = self._pm.base_address
        log.info("attached to %s @ 0x%x", self.process_name, self._base)
        self._load_offsets()

    def _load_offsets(self) -> None:
        if not self.signatures_path.exists():
            log.warning("no signatures file at %s", self.signatures_path)
            return
        with self.signatures_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        self._offsets = {k: int(v, 0) for k, v in data.get("offsets", {}).items()}

    def read_ptr(self, name: str, chain: list[int]) -> int:
        self.attach()
        assert self._pm is not None
        addr = self._base + self._offsets.get(name, 0)
        for off in chain:
            addr = self._pm.read_longlong(addr) + off
        return addr

    def poll(self) -> list[dict[str, Any]]:
        # Memory is pulled on-demand by processors, not polled here.
        return []