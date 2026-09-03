#!/usr/bin/env python3
"""Validate `exercises/defaults.json` and every name that points into it.

The defaults file is authored, not generated: it is read once by the agent
when it builds a program and once per typed name by the fallback ladder, and
nothing writes it. So the proof it needs is a validator, not a builder
(the generator it replaces was a templating layer over a file used once).

An exercise is identified by its `name`. There is no slug and no id: the
name is what a `Sets` row stores, what a `library/` template prescribes, and
what an alias resolves to. This check is what stops those three drifting.

    python3 tools/catalog/check.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULTS_PATH = ROOT / "exercises" / "defaults.json"
ALIASES_PATH = ROOT / "exercises" / "aliases.json"
SCHEMA_PATH = ROOT / "schema" / "notion-schema.json"
LIBRARY_DIR = ROOT / "library"
SUBSTITUTIONS_PATH = (
    ROOT / ".claude" / "skills" / "program-design" / "references" / "substitutions.md"
)
ROW_KEYS = {"name", "measure", "source"}
SOURCES = {"free-exercise-db", "extra"}


def prescribed_names() -> set[str]:
    """Every `exercise` a shipped `library/` template names."""
    found: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "exercise" and isinstance(value, str):
                    found.add(value)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    for path in sorted(LIBRARY_DIR.glob("*.json")):
        walk(json.loads(path.read_text()))
    return found


def substitution_names(names: set[str]) -> set[str]:
    """Every default name `references/substitutions.md` swaps to or from."""
    text = SUBSTITUTIONS_PATH.read_text()
    return {name for name in names if f"| {name} " in text or f" {name} |" in text}


def problems() -> list[str]:
    defaults = json.loads(DEFAULTS_PATH.read_text())
    aliases = json.loads(ALIASES_PATH.read_text())
    measures = set(json.loads(SCHEMA_PATH.read_text())["measure_kinds"])
    bad: list[str] = []

    names = [row.get("name") for row in defaults]
    duplicates = sorted({n for n in names if names.count(n) > 1})
    if duplicates:
        bad.append(f"duplicate names: {duplicates}")
    lowered = [str(n).lower() for n in names]
    collisions = sorted({n for n in lowered if lowered.count(n) > 1})
    if collisions:
        bad.append(f"names that differ only by case: {collisions}")

    for row in defaults:
        if set(row) != ROW_KEYS:
            bad.append(f"{row.get('name')!r}: keys {sorted(row)}, want {sorted(ROW_KEYS)}")
        if row.get("measure") not in measures:
            bad.append(f"{row.get('name')!r}: measure {row.get('measure')!r} is not a measure kind")
        if row.get("source") not in SOURCES:
            bad.append(f"{row.get('name')!r}: source {row.get('source')!r} not in {sorted(SOURCES)}")

    name_set = set(names)
    dangling = {alias: target for alias, target in aliases.items() if target not in name_set}
    if dangling:
        bad.append(f"aliases with no default: {dangling}")
    shadowed = sorted({a for a in aliases if a.lower() in {n.lower() for n in name_set}})
    if shadowed:
        bad.append(f"aliases that collide with a default name: {shadowed}")

    unprescribed = sorted(prescribed_names() - name_set)
    if unprescribed:
        bad.append(f"library templates prescribe names no default carries: {unprescribed}")
    return bad


def main() -> int:
    bad = problems()
    for line in bad:
        print(f"defaults: {line}")
    if bad:
        return 1
    defaults = json.loads(DEFAULTS_PATH.read_text())
    aliases = json.loads(ALIASES_PATH.read_text())
    extra = sum(1 for row in defaults if row["source"] == "extra")
    print(f"defaults: {len(defaults)} names ok "
          f"({len(defaults) - extra} free-exercise-db + {extra} authored), "
          f"{len(aliases)} aliases, {len(prescribed_names())} prescribed by library/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
