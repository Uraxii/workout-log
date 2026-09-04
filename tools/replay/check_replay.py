"""Differential proof for `rules.replay()` (phase 1, replay-engine-scope.md):
for every fixture whose `expected.tsv` carries a `config-write
agent/progression-state` row, fold the same sessions through `replay()` and
assert it reproduces the value the turn-by-turn write path already wrote.

Fixture list is derived by glob, never hardcoded, so a new fixture that
writes progression state is picked up automatically. A window is the run of
consecutive session lines for one exercise between its `setup` line and the
first accept/decline/halt after it (`replay` cannot cross one: those move
`cfg` outside `evaluate`, load_adjust.py `_decline_or_accept`); an exercise
whose window is empty is skipped, not failed.

    python3 tools/replay/check_replay.py
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / ".claude/skills/load-adjust/scripts"))
sys.path.insert(0, str(_ROOT / "tools/mock-notion"))

import load_adjust  # noqa: E402  (same-dir-style insert above)
import parse  # noqa: E402
import rules  # noqa: E402
from transcript import parse_transcript  # noqa: E402

WRITES = frozenset({"bump", "miss_hold", "next_stage", "deload_ask", "deload_repeat"})
YES_NO = load_adjust._YES | load_adjust._NO
FIELD_ACCUMULATOR = {"bump": "current", "next_stage": "stage"}


def _progression_rows(expected_tsv: pathlib.Path) -> list[dict[str, Any]]:
    rows = []
    for line in expected_tsv.read_text().splitlines()[1:]:
        cols = line.split("\t", 3)
        if len(cols) == 4 and cols[0] == "config-write" and \
           cols[1] == "agent/progression-state" and cols[2] == "progression":
            rows.append(json.loads(cols[3]))
    return rows


def _fixtures(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(d for d in root.glob("fixtures/*/")
                  if _progression_rows(d / "expected.tsv"))


def _checkpoints(rows: list[dict[str, Any]], name: str) -> list[Any]:
    """Every distinct value `name`'s sub-dict took on, in write order. One
    entry per write-producing turn for that exercise, in the whole fixture,
    since the cumulative JSON blob repeats an unchanged value verbatim."""
    seen: list[Any] = []
    for row in rows:
        if name in row and (not seen or row[name] != seen[-1]):
            seen.append(row[name])
    return seen


def _setups(turns: list) -> list[tuple[str, int, dict[str, Any]]]:
    """First *readable* `setup` turn per exercise: its name, the index right
    after it, and its parsed cfg. A `setup` line the grammar can't read
    (08-progression-refusal's `increment=abc`) never seeds a rule in
    production either (load_adjust.py's `Unreadable` catch reverts state),
    so it is skipped here the same way, leaving the next `setup` for that
    name as the real one."""
    found, seen = [], set()
    for i, turn in enumerate(turns):
        line = turn.line.strip(" \r\n")
        if turn.skill != "load-adjust" or not line.startswith("setup\t"):
            continue
        fields = line.split("\t")
        if fields[1] in seen:
            continue
        try:
            cfg = parse.setup_config(fields[2:])
        except parse.Unreadable:
            continue
        seen.add(fields[1])
        found.append((fields[1], i + 1, cfg))
    return found


def _window(turns: list, start: int, name: str) -> list[tuple]:
    """The clean run of `name`'s session lines after its setup: stops at a
    halt (a turn outside load-adjust), a yes/no, or a re-setup of `name`.
    Other exercises' turns and unreadable lines pass through untouched."""
    sessions = []
    for turn in turns[start:]:
        line = turn.line.strip(" \r\n")
        if turn.skill != "load-adjust" or line.lower() in YES_NO:
            break
        if line.startswith("setup\t"):
            if line.split("\t")[1] == name:
                break
            continue
        if "\t" not in line or line.split("\t", 1)[0] != name:
            continue
        parts = line.split("\t", 1)[1].split("\t")
        try:
            set_rows, kind = parse.sets(parts[0])
            sessions.append((set_rows, kind, parse.rpe(parts[1:])))
        except parse.Unreadable:
            continue
    return sessions


def _write_tally(outcomes: list[str]) -> tuple[int, str | None]:
    writes = [tag for tag in outcomes if tag in WRITES]
    return len(writes), (writes[-1] if writes else None)


def _expected_field(cfg: dict[str, Any], tag: str,
                     result: dict[str, Any]) -> tuple[str, Any] | None:
    if tag not in FIELD_ACCUMULATOR:
        return None
    field = "stage_index" if tag == "next_stage" else rules.TARGET_FIELD[cfg["axis"]]
    raw = result[FIELD_ACCUMULATOR[tag]]
    return field, load_adjust._stored_value(cfg, {"outcome": tag, "value": raw})


def _verify(cfg: dict[str, Any], name: str, sessions: list[tuple],
            rows: list[dict[str, Any]]) -> tuple[bool, str] | None:
    result = rules.replay(cfg, sessions)
    if len(result["outcomes"]) != len(sessions):
        # A short fold could otherwise alias an earlier, still-valid
        # checkpoint (e.g. skipping the last session of three bumps lands
        # on the second bump's own recorded value) and pass by accident.
        return False, f"{len(result['outcomes'])} outcomes for {len(sessions)} sessions"
    count, tag = _write_tally(result["outcomes"])
    if count == 0:
        return None
    checkpoints = _checkpoints(rows, name)
    if count > len(checkpoints):
        return False, f"replay saw {count} writes, fixture recorded {len(checkpoints)}"
    expected = checkpoints[count - 1]
    ok = expected.get("fail_count") == result["fail_count"]
    extra = _expected_field(cfg, tag, result)
    if extra:
        field, value = extra
        ok = ok and expected.get(field) == value
    return ok, "" if ok else f"replay={result} expected={expected}"


def main() -> int:
    checked, failed = 0, False
    for fixture_dir in _fixtures(_ROOT):
        text = (fixture_dir / "transcript.txt").read_text()
        turns = parse_transcript(text).turns
        rows = _progression_rows(fixture_dir / "expected.tsv")
        for name, start, cfg in _setups(turns):
            unit = f"{fixture_dir.name}/{name}"
            sessions = _window(turns, start, name)
            if not sessions:
                print(f"{unit}: skip (empty window)")
                continue
            verdict = _verify(cfg, name, sessions, rows)
            if verdict is None:
                print(f"{unit}: skip (window wrote nothing)")
                continue
            ok, reason = verdict
            checked += 1
            failed = failed or not ok
            print(f"{unit}: {'ok' if ok else 'FAIL'}" + (f"\n  {reason}" if reason else ""))
    print(f"windows checked: {checked}")
    if checked == 0:
        print("windows checked: FAIL (expected > 0)")
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
