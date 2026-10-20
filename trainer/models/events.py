"""Typed event helpers for the pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Event:
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, **self.payload}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Event":
        kind = d.get("kind", "unknown")
        payload = {k: v for k, v in d.items() if k != "kind"}
        return cls(kind=kind, payload=payload)