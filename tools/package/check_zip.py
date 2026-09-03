#!/usr/bin/env python3
"""Import every skill module out of the built ZIP and log one set through it.

Every other phase 7 check (docs/build-plan.md s9) reads the repo tree, so a
ZIP that ships no data files still passed them while flavour B (docs/install.md)
could not import `rows.py` at all (workout-log-d2y). This unpacks
dist/workout-skills.zip into a scratch dir outside the repo, which is
what a claude.ai upload gets, imports every <skill>/scripts/*.py from it, then
calls the `session-runner` seam and checks the row it writes.

    python3 tools/package/check_zip.py
"""
from __future__ import annotations

import importlib
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_ZIP = REPO_ROOT / "dist" / "workout-skills.zip"

# One turn against the seam that broke: fixture 01-three-sets' first line and
# the state replay.py builds for it (fixtures/01-three-sets/transcript.txt).
SEAM_LINE = "185x5"
SEAM_STATE = {
    "tz": "UTC",
    "units": "lb",
    "known": {"Squat (Barbell)": "weight_reps"},
    "session_id": None,
    "session_seq": 0,
    "cursor": {},
    "now": "2026-09-01T09:00:00+00:00",
    "message_id": "msg-1",
}
EXPECTED_SET_FIELDS = {"Load": 185, "Reps": 5, "Unit": "lb"}


def import_every_module(unpacked: Path) -> list[str]:
    """Import each <skill>/scripts/*.py from the unpacked ZIP, ZIP paths only."""
    scripts_dirs = sorted(unpacked.glob("*/scripts"))
    if not scripts_dirs:
        sys.exit(f"{DIST_ZIP}: no <skill>/scripts dir in the ZIP")
    sys.path[:0] = [str(unpacked)] + [str(d) for d in scripts_dirs]
    imported = []
    for scripts_dir in scripts_dirs:
        for module_file in sorted(scripts_dir.glob("*.py")):
            importlib.import_module(module_file.stem)
            imported.append(f"{scripts_dir.parent.name}/{module_file.name}")
    return imported


def log_one_set() -> str:
    """Run `log_set` from the unpacked ZIP, return its confirm line."""
    turn = importlib.import_module("log_set").log_set(SEAM_LINE, dict(SEAM_STATE))
    set_rows = [w["payload"] for w in turn["writes"] if w["target"] == "Sets"]
    if len(set_rows) != 1:
        sys.exit(f"log_set wrote {len(set_rows)} Sets rows for {SEAM_LINE!r}, want 1")
    wrong = {
        field: (want, set_rows[0].get(field))
        for field, want in EXPECTED_SET_FIELDS.items()
        if set_rows[0].get(field) != want
    }
    if wrong:
        sys.exit(f"log_set wrote the wrong Sets row, want/got: {wrong}")
    return turn["confirm_line"]


def main() -> int:
    if not DIST_ZIP.exists():
        sys.exit(f"{DIST_ZIP}: not built, run `make skills` first")
    with tempfile.TemporaryDirectory(prefix="workout-log-zip-") as scratch:
        unpacked = Path(scratch)
        with zipfile.ZipFile(DIST_ZIP) as zf:
            zf.extractall(unpacked)
        imported = import_every_module(unpacked)
        confirm_line = log_one_set()
    print(f"imported {len(imported)} module(s) from {DIST_ZIP.name}")
    print(f"log_set from the ZIP said: {confirm_line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
