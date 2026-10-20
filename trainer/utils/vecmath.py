"""Vector math used by aim and esp processors."""
from __future__ import annotations

import math


def length(v: tuple[float, float, float]) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def world_to_screen(
    world: tuple[float, float, float],
    view_matrix: list[float],
    width: int = 1920,
    height: int = 1080,
) -> tuple[float, float] | None:
    x, y, z = world
    clip_x = x * view_matrix[0] + y * view_matrix[4] + z * view_matrix[8] + view_matrix[12]
    clip_y = x * view_matrix[1] + y * view_matrix[5] + z * view_matrix[9] + view_matrix[13]
    clip_w = x * view_matrix[3] + y * view_matrix[7] + z * view_matrix[11] + view_matrix[15]
    if clip_w < 0.001:
        return None
    ndc_x, ndc_y = clip_x / clip_w, clip_y / clip_w
    return (width / 2) * (ndc_x + 1), (height / 2) * (1 - ndc_y)