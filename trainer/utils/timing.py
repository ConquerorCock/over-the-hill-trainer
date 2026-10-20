"""Frame-time helpers."""
from __future__ import annotations

import time
from contextlib import contextmanager


@contextmanager
def frame_clock():
    t0 = time.perf_counter()
    yield
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    time.sleep(max(0.0, (16.0 - elapsed_ms) / 1000.0))