"""Standalone CLI: dump loaded signatures and test attach."""
from __future__ import annotations

import argparse
import json
import sys

from trainer.config import load_config
from trainer.handlers.memory_handler import MemoryHandler


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="oth-diag")
    ap.add_argument("-c", "--config", default="config/default.yaml")
    ap.add_argument("--dump-signatures", action="store_true")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    mem = MemoryHandler(cfg.game.process_name, cfg.game.signatures_path)

    if args.dump_signatures:
        print(json.dumps({"process": cfg.game.process_name, "offsets": mem._offsets}, indent=2))
        return 0

    try:
        mem.attach()
        print(f"OK attached to {cfg.game.process_name} @ 0x{mem._base:x}")
        return 0
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())