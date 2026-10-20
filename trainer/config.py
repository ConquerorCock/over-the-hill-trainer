"""Config loader. YAML on disk -> pydantic models."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class GameConfig(BaseModel):
    process_name: str = "OverTheHill.exe"
    signatures_path: str = "trainer/signatures/base.yaml"
    tick_ms: int = 16


class AimConfig(BaseModel):
    enabled: bool = True
    fov_degrees: float = 8.0
    smoothing: float = 0.35
    target_bone: Literal["head", "chest", "nearest"] = "head"


class EspConfig(BaseModel):
    enabled: bool = True
    box: bool = True
    health_bar: bool = True
    max_distance_m: int = 250
    color: str = "#00ff88"


class RecoilConfig(BaseModel):
    enabled: bool = True
    pattern: Literal["ak", "m4", "smg", "auto"] = "auto"
    strength: float = 0.75


class OverlayConfig(BaseModel):
    enabled: bool = True
    fullscreen: bool = True
    click_through: bool = True
    fps_cap: int = 0


class HotkeyConfig(BaseModel):
    aim_toggle: str = "f1"
    esp_toggle: str = "f2"
    recoil_toggle: str = "f3"
    panic: str = "f12"


class LoggingConfig(BaseModel):
    level: str = "INFO"


class TrainerConfig(BaseModel):
    game: GameConfig = Field(default_factory=GameConfig)
    aim: AimConfig = Field(default_factory=AimConfig)
    esp: EspConfig = Field(default_factory=EspConfig)
    recoil: RecoilConfig = Field(default_factory=RecoilConfig)
    overlay: OverlayConfig = Field(default_factory=OverlayConfig)
    hotkeys: HotkeyConfig = Field(default_factory=HotkeyConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def load_config(path: str | Path) -> TrainerConfig:
    p = Path(path)
    if not p.exists():
        return TrainerConfig()
    with p.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return TrainerConfig.model_validate(raw)