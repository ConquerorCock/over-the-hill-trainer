"""Injects mouse movement into the game via SendInput."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Any

_user32 = ctypes.windll.user32

_MOUSEEVENTF_MOVE = 0x0001


class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))]


class _INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("mi", _MOUSEINPUT)]


class InputDriver:
    def _move(self, dx: float, dy: float) -> None:
        inp = _INPUT(type=0, mi=_MOUSEINPUT(int(dx), int(dy), 0, _MOUSEEVENTF_MOVE, 0, None))
        _user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(_INPUT))

    def emit(self, event: dict[str, Any]) -> None:
        total_dx = 0.0
        total_dy = 0.0
        if "aim_delta" in event:
            total_dx += event["aim_delta"]["dx"]
            total_dy += event["aim_delta"]["dy"]
        if "recoil_delta" in event:
            total_dx += event["recoil_delta"]["dx"]
            total_dy += event["recoil_delta"]["dy"]
        if total_dx or total_dy:
            self._move(total_dx, total_dy)