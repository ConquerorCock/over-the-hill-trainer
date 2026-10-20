"""Entry point. Wires handlers -> processors -> drivers, then runs the pipeline."""
from __future__ import annotations

import argparse
import logging
import sys

from trainer.config import load_config
from trainer.pipeline import Pipeline
from trainer.handlers.input_handler import InputHandler
from trainer.handlers.memory_handler import MemoryHandler
from trainer.handlers.hotkey_handler import HotkeyHandler
from trainer.processors.aim_processor import AimProcessor
from trainer.processors.esp_processor import EspProcessor
from trainer.processors.recoil_processor import RecoilProcessor
from trainer.drivers.overlay_driver import OverlayDriver
from trainer.drivers.input_driver import InputDriver
from trainer.drivers.log_driver import LogDriver


def build_pipeline(cfg) -> Pipeline:
    mem = MemoryHandler(cfg.game.process_name, cfg.game.signatures_path)
    inp = InputHandler()
    hot = HotkeyHandler(cfg.hotkeys)

    aim = AimProcessor(mem, cfg.aim)
    esp = EspProcessor(mem, cfg.esp)
    recoil = RecoilProcessor(mem, cfg.recoil)

    overlay = OverlayDriver(cfg.overlay)
    input_drv = InputDriver()
    log = LogDriver(cfg.logging.level)

    pipe = Pipeline(name="oth-main")
    pipe.register_source(hot)
    pipe.register_source(inp)
    pipe.register_processor(aim)
    pipe.register_processor(esp)
    pipe.register_processor(recoil)
    pipe.register_sink(overlay)
    pipe.register_sink(input_drv)
    pipe.register_sink(log)
    return pipe


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="oth-trainer")
    parser.add_argument("-c", "--config", default="config/default.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    cfg = load_config(args.config)
    pipe = build_pipeline(cfg)

    if args.dry_run:
        logging.getLogger("bootstrap").info("dry-run: pipeline built, not starting")
        return 0

    try:
        pipe.run()
    except KeyboardInterrupt:
        logging.getLogger("bootstrap").info("shutting down")
    return 0


if __name__ == "__main__":
    sys.exit(main())