"""Global hotkey listener that toggles pipeline features."""
from __future__ import annotations

from typing import Any

import keyboard

from trainer.config import HotkeyConfig


class HotkeyHandler:
    name = "hotkeys"

    def __init__(self, cfg: HotkeyConfig) -> None:
        self.cfg = cfg
        self._pending: list[dict[str, Any]] = []
        self._install()

    def _install(self) -> None:
        keyboard.add_hotkey(self.cfg.aim_toggle, lambda: self._pending.append({"kind": "toggle", "feature": "aim"}))
        keyboard.add_hotkey(self.cfg.esp_toggle, lambda: self._pending.append({"kind": "toggle", "feature": "esp"}))
        keyboard.add_hotkey(self.cfg.recoil_toggle, lambda: self._pending.append({"kind": "toggle", "feature": "recoil"}))
        keyboard.add_hotkey(self.cfg.panic, lambda: self._pending.append({"kind": "panic"}))

    def poll(self) -> list[dict[str, Any]]:
        out = self._pending
        self._pending = []
        return out