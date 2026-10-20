"""Renders the ESP overlay via a transparent Win32 layered window."""
from __future__ import annotations

import ctypes
import logging
from typing import Any

from trainer.config import OverlayConfig

log = logging.getLogger("overlay")
_user32 = ctypes.windll.user32
_gdi32 = ctypes.windll.gdi32

_WS_EX_LAYERED = 0x00080000
_WS_EX_TRANSPARENT = 0x00000020
_WS_POPUP = 0x80000000


class OverlayDriver:
    def __init__(self, cfg: OverlayConfig) -> None:
        self.cfg = cfg
        self._hwnd: int | None = None

    def _ensure_window(self) -> None:
        if self._hwnd is not None or not self.cfg.enabled:
            return
        self._hwnd = _user32.CreateWindowExW(
            _WS_EX_LAYERED | _WS_EX_TRANSPARENT,
            "STATIC", "oth-overlay", _WS_POPUP,
            0, 0, 1920, 1080,
            0, 0, 0, 0,
        )
        _user32.ShowWindow(self._hwnd, 5)
        log.info("overlay window created (hwnd=0x%x)", self._hwnd)

    def emit(self, event: dict[str, Any]) -> None:
        if not self.cfg.enabled:
            return
        draws = event.get("draws")
        if not draws:
            return
        self._ensure_window()
        # Real rendering goes through GDI on the layered window; stub for now.
        for d in draws:
            if d["type"] == "box":
                _gdi32.Rectangle(0, int(d["x"]), int(d["y"]), int(d["x"] + d["w"]), int(d["y"] + d["h"]))