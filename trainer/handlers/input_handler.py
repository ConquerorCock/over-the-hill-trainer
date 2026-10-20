"""Captures mouse/keyboard deltas via the Win32 API and emits them as events."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Any

_user32 = ctypes.windll.user32


class _POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


class InputHandler:
    name = "input"

    def __init__(self) -> None:
        self._last = _POINT()
        _user32.GetCursorPos(ctypes.byref(self._last))

    def poll(self) -> list[dict[str, Any]]:
        cur = _POINT()
        _user32.GetCursorPos(ctypes.byref(cur))
        dx = cur.x - self._last.x
        dy = cur.y - self._last.y
        self._last = cur
        if dx == 0 and dy == 0:
            return []
        return [{"kind": "input.delta", "dx": dx, "dy": dy}]