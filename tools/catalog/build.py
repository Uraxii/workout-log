#!/usr/bin/env python3
"""Merge the free-exercise-db seed and exercises/extra.json into one catalog.

Rerunnable and idempotent: `python3 tools/catalog/build.py` always writes the
same exercises/catalog.json for the same inputs. Every seed row gets a
`measure` kind (schema/notion-schema.json measure_kinds) derived by a small
rule; extra.json rows already declare their own. See exercises/README.md.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

EXERCISES_DIR = Path(__file__).resolve().parent.parent.parent / "exercises"
SCHEMA_PATH = Path(__file__).resolve().parent.parent.parent / "schema" / "notion-schema.json"

# Equipment that implies an external load is tracked (weight_reps default).
# Everything else (bodyweight, or an unweighted implement like an ab wheel or
# rings) defaults to reps_only.
LOADED_EQUIPMENT = {
    "barbell", "dumbbell", "cable", "machine", "kettlebells",
    "e-z curl bar", "bands", "medicine ball",
}

# Hand-picked exceptions the category/equipment rule gets wrong.
MEASURE_OVERRIDES = {
    "Rope_Jumping": "hold_time",  # timed, not distance-tracked
}


def measure_for(row: dict) -> str:
    """Derive a measure kind for a free-exercise-db row.

    Order: category first (stretching/cardio/strongman have a clear default
    shape), then a static hold, then equipment decides load vs. bodyweight.
    """
    if row["id"] in MEASURE_OVERRIDES:
        return MEASURE_OVERRIDES[row["id"]]
    category = row.get("category")
    if category == "stretching":
        return "hold_time"
    if category == "cardio":
        return "distance_time"
    if category == "strongman":
        return "distance_load"
    if row.get("force") == "static":
        return "hold_time"
    if row.get("equipment") in LOADED_EQUIPMENT:
        return "weight_reps"
    return "reps_only"


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_catalog() -> list[dict]:
    seed = load_json(EXERCISES_DIR / "free-exercise-db.json")
    extra = load_json(EXERCISES_DIR / "extra.json")

    for row in seed:
        row["measure"] = measure_for(row)
        row["source"] = "free-exercise-db"
    for row in extra:
        row["source"] = "extra"

    catalog = seed + extra
    catalog.sort(key=lambda r: r["id"])
    return catalog


def validate(catalog: list[dict], aliases: dict) -> None:
    valid_measures = set(load_json(SCHEMA_PATH)["measure_kinds"].keys())

    ids = [row["id"] for row in catalog]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        raise SystemExit(f"duplicate ids: {sorted(duplicates)}")

    bad_measures = {row["id"] for row in catalog if row.get("measure") not in valid_measures}
    if bad_measures:
        raise SystemExit(f"invalid measure kind on: {sorted(bad_measures)}")

    id_set = set(ids)
    dangling = {alias: target for alias, target in aliases.items() if target not in id_set}
    if dangling:
        raise SystemExit(f"aliases with no target: {dangling}")

    colliding = sorted(set(aliases.keys()) & id_set)
    if colliding:
        raise SystemExit(f"aliases that collide with a canonical id: {colliding}")


def main() -> None:
    aliases = load_json(EXERCISES_DIR / "aliases.json")
    catalog = build_catalog()
    validate(catalog, aliases)

    out_path = EXERCISES_DIR / "catalog.json"
    # ponytail: os.replace is atomic on POSIX only within one filesystem, so
    # the temp file must live in the same dir as out_path (never /tmp).
    fd, tmp_path = tempfile.mkstemp(dir=EXERCISES_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(json.dumps(catalog, indent=2) + "\n")
        os.replace(tmp_path, out_path)
    except BaseException:
        os.unlink(tmp_path)
        raise

    extra_count = sum(1 for row in catalog if row["source"] == "extra")
    by_measure: dict[str, int] = {}
    for row in catalog:
        by_measure[row["measure"]] = by_measure.get(row["measure"], 0) + 1
    print(f"catalog rows: {len(catalog)} ({len(catalog) - extra_count} seed + {extra_count} extra)")
    print(f"aliases: {len(aliases)}")
    print(f"measure kinds: {by_measure}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    sys.exit(main())
