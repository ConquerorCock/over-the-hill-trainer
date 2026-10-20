"""Simple async pipeline: sources -> processors -> sinks."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

log = logging.getLogger("pipeline")


class Source(Protocol):
    def poll(self) -> list[dict[str, Any]]: ...


class Processor(Protocol):
    def process(self, event: dict[str, Any], state: "PipelineState") -> dict[str, Any]: ...


class Sink(Protocol):
    def emit(self, event: dict[str, Any]) -> None: ...


@dataclass
class PipelineState:
    aim_enabled: bool = True
    esp_enabled: bool = True
    recoil_enabled: bool = True
    extras: dict[str, Any] = field(default_factory=dict)


class Pipeline:
    def __init__(self, name: str) -> None:
        self.name = name
        self.sources: list[Source] = []
        self.processors: list[Processor] = []
        self.sinks: list[Sink] = []
        self.state = PipelineState()

    def register_source(self, s: Source) -> None:
        self.sources.append(s)

    def register_processor(self, p: Processor) -> None:
        self.processors.append(p)

    def register_sink(self, s: Sink) -> None:
        self.sinks.append(s)

    def run(self) -> None:
        log.info("pipeline %s starting (%d sources, %d processors, %d sinks)",
                 self.name, len(self.sources), len(self.processors), len(self.sinks))
        while True:
            t0 = time.perf_counter()
            for src in self.sources:
                for ev in src.poll():
                    for proc in self.processors:
                        try:
                            ev = proc.process(ev, self.state)
                        except Exception as exc:  # keep the pipeline alive
                            log.exception("processor %s failed: %s", type(proc).__name__, exc)
                    for sink in self.sinks:
                        sink.emit(ev)
            elapsed = (time.perf_counter() - t0) * 1000
            sleep_ms = max(0.0, 16.0 - elapsed)
            time.sleep(sleep_ms / 1000.0)