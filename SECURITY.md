# Security Policy

over-the-hill-trainer reads and writes memory of a single-player and private-server
game process. It does **not** phone home, does **not** include a remote loader,
and does **not** ship obfuscated binaries.

## Supported versions

Only the latest tagged release on `main` receives offset fixes.

## Reporting a vulnerability

If you find something that could be weaponized (e.g. arbitrary write primitive
exposed over IPC, or an unsigned auto-update path), email the maintainer listed
in `pyproject.toml` **before** opening a public issue. Give us 72 hours.

## Out of scope

- Getting banned on official servers. Read the README disclaimer.
- Antivirus false positives from `pymem`/`pywin32`. These are known and expected.