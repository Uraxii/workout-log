"""The seam for `program-design`: `design_turn(line, state) -> Turn` (build-
plan s6, s7). Same shape as `log_set`, `intake_turn`, `triage_turn`:

    python3 design.py                 # {"line":..., "state":...} on stdin, Turn on stdout
    from design import design_turn    # in-process, from the replay runner

Three lines a turn can be, checked in this order:

1. A GAP category (`library.refusal_for`) -> the s7.2 scripted refusal, no
   writes. Checked first: a request naming rings or carries should never fall
   through to a nearby template pick.
2. "new limits entry: <area>" -> swap-in-place (`_swap_turn`), the s6 trigger
   for any newly opened `config/limits` entry (lim L-21).
3. Anything else -> a plan request (`_plan_turn`): pick a template
   (`library.pick_template`) against the athlete's stored profile as well as
   this line, retrieve it verbatim from `library/`, and resolve a starting
   load for every block whose baseline is on file, floored to what
   `config/preferences` says her gym can load.

Every turn that changes the program writes the whole template body to
`program/current` (`program_page.py`), so the rotation a later chat reads is
the rotation this turn picked, swaps included. `state["program"]` is the same
object, threaded for the rest of this chat.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from typing import Any, TypedDict

import baselines
import library
import program_page
import starting_loads
import substitutions

DEFAULT_UNIT = "lb"
# The stored profile fields `references/templates.md` matches words against.
PROFILE_MATCH_KEYS = ("goal", "equipment", "training_age")
_DAYS_RE = re.compile(r"\b(\d+)\s*days?\b", re.IGNORECASE)
_LIMITS_RE = re.compile(r"\bnew limits entry\b", re.IGNORECASE)
_AREA_RE = re.compile(r"\b(knee|shoulder|back|hip|ankle|elbow|wrist)\b", re.IGNORECASE)


class Write(TypedDict):
    verb: str
    target: str
    payload: dict[str, Any]


class Turn(TypedDict):
    writes: list[Write]
    say: str
    state: dict[str, Any]


def _parse_days(line: str) -> int:
    match = _DAYS_RE.search(line)
    return int(match.group(1)) if match else 0


def _profile_days(athlete: dict[str, str]) -> int:
    """`config/athlete.days_per_week`, the value `intake` wrote there. Nothing
    else records how often the athlete trains, so with no line saying "3 days"
    this is what `min_days` filters on (workout-log-k37)."""
    raw = str(athlete.get("days_per_week", "")).strip()
    return int(raw) if raw.isdigit() else 0


def _profile_text(line: str, athlete: dict[str, str]) -> str:
    """The words `library.pick_template` matches goal, equipment and training
    age against: this line plus the profile `intake` already stored, so an
    athlete who answered those questions is not made to repeat them."""
    return " ".join([line] + [str(athlete.get(key, "")) for key in PROFILE_MATCH_KEYS])


def _started_at(state: dict[str, Any], template_id: str) -> str:
    """When the ACTIVE program began, which is what scopes the rotation
    cursor to it. Asking again for the program you are already on is not a
    new block: it keeps its start, so an accidental second "make me a plan"
    cannot send the athlete back to day one."""
    if state.get("program_id") == template_id and state.get("program_started_at"):
        return state["program_started_at"]
    return state.get("now", "")


def _program_write(program: dict[str, Any], template_id: str, started_at: str) -> Write:
    return {"verb": "config-write", "target": "program/current",
            "payload": program_page.page_body(program, template_id, started_at)}


def _plan_turn(line: str, state: dict[str, Any]) -> Turn:
    state = copy.deepcopy(state)
    athlete = state.get("athlete", {})
    preferences = state.get("preferences", {})
    unit = state.get("units") or DEFAULT_UNIT
    days = _parse_days(line) or _profile_days(athlete)
    template_id, reason = library.pick_template(_profile_text(line, athlete), days)
    program = library.load_template(template_id)
    started_at = _started_at(state, template_id)
    on_file = baselines.parse(f"{line} {athlete.get('strength_baseline', '')}")

    writes: list[Write] = [_program_write(program, template_id, started_at)]
    progression = state.setdefault("progression", {})
    load_lines = starting_loads.resolve(program, on_file, unit, preferences,
                                        progression)
    if load_lines:
        # One write for every resolved load: per-exercise state is one key on
        # `program/current`, never a row. A starting load is not a log.
        writes.append(program_page.progression_write(progression))

    state["program"] = program
    state["program_id"] = template_id
    state["program_started_at"] = started_at
    say = f"Picked {program['name']}: {reason}"
    if load_lines:
        say += " " + " ".join(load_lines)
    return {"writes": writes, "say": say, "state": state}


def _swap_turn(line: str, state: dict[str, Any]) -> Turn:
    state = copy.deepcopy(state)
    program = state.get("program")
    area_match = _AREA_RE.search(line)
    if program is None or area_match is None:
        return {"writes": [], "say": "No active program to adjust.", "state": state}

    area = area_match.group(1).lower()
    subs = substitutions.for_area(area)
    swapped = []
    for node in program["rotation"]:
        for block in node["blocks"]:
            exercise_id = block.get("exercise")
            if exercise_id in subs:
                block["exercise"] = subs[exercise_id]
                swapped.append((node["label"], block.get("label", ""), exercise_id, subs[exercise_id]))

    if not swapped:
        return {"writes": [], "say": f"No substitute on file for {area}; leaving the program as is.", "state": state}

    parts = [f"{node_label} {block_label}: {old} -> {new}"
             for node_label, block_label, old, new in swapped]
    say = f"New {area} entry. Swapped in place: {'; '.join(parts)}."
    write = _program_write(program, state.get("program_id", ""),
                           state.get("program_started_at", ""))
    return {"writes": [write], "say": say, "state": state}


def design_turn(line: str, state: dict[str, Any]) -> Turn:
    refusal = library.refusal_for(line)
    if refusal is not None:
        return {"writes": [], "say": refusal, "state": copy.deepcopy(state)}
    if _LIMITS_RE.search(line):
        return _swap_turn(line, state)
    return _plan_turn(line, state)


def main() -> int:
    request = json.load(sys.stdin)
    json.dump(design_turn(request["line"], request.get("state", {})), sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
