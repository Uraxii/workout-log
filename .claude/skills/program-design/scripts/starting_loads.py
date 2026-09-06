"""A template's blocks plus a spoken baseline -> where each lift starts.

Split out of `design.py` (house limit; `docs/architecture.md` "one script per
skill... split by domain, never by execution step"). `design.py` owns the turn:
which template gets picked and what gets written. This owns one question,
"what weight does this block start at", and answers it in the two shapes the
turn needs, the progression record that persists and the clause the athlete
reads.

It is the bridge between three modules that do not know about each other:
`baselines.py` reads a lift out of her words, `loads.py` does the arithmetic,
and `program_page.py` owns where per-exercise state lives.
"""

from __future__ import annotations

from typing import Any, Iterator

import loads
import program_page


def blocks_with_start(program: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Every block in the rotation that declares a `start` rule."""
    for node in program["rotation"]:
        for block in node["blocks"]:
            if "start" in block:
                yield block


def block_exercise(block: dict[str, Any]) -> str:
    """The lift a `start`-bearing block trains. Most blocks name it directly
    on `exercise`; nSuns' T1 blocks run one lift through several rep/pct
    steps in `sequence` instead, so the name lives on the first step
    (workout-log-bv0)."""
    if "exercise" in block:
        return block["exercise"]
    return block["sequence"][0]["exercise"]


def resolve(program: dict[str, Any], on_file: dict[str, tuple[float, int]],
            unit: str, preferences: dict[str, str],
            progression: dict[str, dict[str, Any]]) -> list[str]:
    """Merge a starting load into `progression` for every block whose lift has
    a baseline on file, and return one clause per lift resolved. A block whose
    baseline is missing, or whose `start` rule carries no baseline arithmetic,
    is skipped in silence: it starts wherever the template says."""
    clauses = []
    for block in blocks_with_start(program):
        name = block_exercise(block)
        baseline = on_file.get(name)
        if baseline is None:
            continue
        resolved = _one_block(block, name, *baseline, unit, preferences)
        if resolved is None:
            continue
        name, record, clause = resolved
        program_page.merge_progression(progression, name, record)
        clauses.append(clause)
    return clauses


def _one_block(block: dict[str, Any], name: str, weight: float, reps: int,
               unit: str, preferences: dict[str, str]
               ) -> tuple[str, dict[str, Any], str] | None:
    """One block's first working weight: the progression record carrying it,
    and the clause explaining it. Arithmetic in kilograms, answer in her own
    unit, floored to what her gym loads (`docs/unit-and-magnitude-model.md`
    s1, workout-log-ayf.2)."""
    effective_1rm_kg = loads.estimated_max(loads.to_kg(weight, unit), reps)
    if effective_1rm_kg is None:
        return None
    start_load = loads.resolve_start_load(effective_1rm_kg, block["start"], unit,
                                          preferences)
    if start_load is None:
        return None
    effective_1rm = loads.to_display(effective_1rm_kg, unit)
    record = {
        "training_max": loads.round_down_to_increment(effective_1rm, unit, preferences),
        "next_target": loads.format_load(start_load, unit),
    }
    clause = (f"{block.get('label', name)} {name} starts at "
              f"{loads.format_load(start_load, unit)} (from {weight:g}x{reps}, e1RM "
              f"{effective_1rm:.0f} {unit} after form allowance).")
    return name, record, clause
