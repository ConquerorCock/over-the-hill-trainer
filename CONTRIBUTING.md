# Contributing to over-the-hill-trainer

Thanks for wanting to help the old-timers keep up.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m trainer.bootstrap
```

## Pull requests

- Keep PRs focused. One feature / one fix.
- Run `pytest tests/` before pushing.
- If you add a new memory signature, put it under `trainer/signatures/` and document the game build it targets in the docstring.
- Never commit offsets for a build you haven't verified — stale offsets crash the game and get issues filed against us.

## Code style

- Python 3.11+, type hints on public functions.
- `snake_case` for modules, `PascalCase` for models.
- Prefer dataclasses/pydantic for anything that crosses the process boundary.

## Reporting offset changes

Game patches break signatures. Open an issue with:
1. Game version string
2. Which feature broke (aim assist / ESP / recoil)
3. Output of `python -m trainer.diagnostics --dump-signatures`