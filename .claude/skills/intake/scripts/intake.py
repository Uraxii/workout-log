"""The seam for `intake`: `intake_turn(line, state) -> Turn` (build-plan s5,
s9), same shape as `log_set` and `screen_turn`:

    python3 intake.py                 # {"line":..., "state":...} on stdin, Turn on stdout
    from intake import intake_turn    # in-process, from the replay runner

One flat question list, one item per turn (`principle-experience-first`):
`references/questions.md` is the ordered source. Safety runs first as seven
PAR-Q+ items plus one conditional follow-up, delegated in-process to
`screen` (`.claude/skills/screen/scripts/screen.py`) so the questions and the
clearance-write rule (S8) live in one place. `intake_cursor` is the flat
index into `ALL_IDS`, written to `config/athlete` after every turn (lim
L-48). A line is scanned against every not-yet-answered field first (lim
L-47): a match writes it and marks it answered, so its own turn is skipped
with a one-clause acknowledgement instead of asked again.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "screen" / "scripts"))
import screen  # noqa: E402  (skill-to-skill seam import, mirrors replay.py's own sys.path use)

DB_ORDER = ("Sessions", "Exercises", "Locations", "Sets")
PARENT = "root-page"
TRIGGER_RE = re.compile(r"\bset\s*me\s*up\b", re.IGNORECASE)
DONE_SAY = 'All set. Say "what do I have today" to start.'

class Write(TypedDict):
    verb: str
    target: str
    payload: dict[str, Any]

class Turn(TypedDict):
    writes: list[Write]
    say: str
    state: dict[str, Any]

def _extract_units(line: str) -> str | None:
    m = re.search(r"\b(lbs?|pounds?|kgs?|kilos?|kilograms?)\b", line, re.I)
    if not m:
        return None
    return "kg" if m.group(1).lower().startswith(("kg", "kilo")) else "lb"

def _extract_days(line: str) -> str | None:
    m = re.search(r"\b(\d+)\s*days?\b", line, re.I)
    return m.group(1) if m else None

def _extract_age(line: str) -> str | None:
    m = re.search(r"\b(\d{1,3})\s*(?:years?\s*old|yo)\b", line, re.I) or re.search(r"\bi'?m\s+(\d{1,3})\b", line, re.I)
    return m.group(1) if m else None

def _extract_nutrition(line: str) -> str | None:
    low = line.lower()
    for word in ("none", "general", "specific"):
        if word in low:
            return word
    return None

# Field steps: safety (PAR-Q+) is handled separately, see ALL_IDS below.
FIELD_STEPS = [
    {"id": "units", "page": "config/preferences", "key": "units",
     "prompt": "Pounds or kilos?", "extract": _extract_units, "global": True},
    {"id": "jurisdiction", "page": "config/athlete", "key": "jurisdiction",
     "prompt": "What country or state are you in? Scope-of-practice rules vary.", "extract": None, "global": False},
    {"id": "goal", "page": "config/athlete", "key": "goal",
     "prompt": "What's the goal? Strength, muscle, fat loss, endurance, sport, general health, or rehab-adjacent?",
     "extract": None, "global": False},
    {"id": "training_age", "page": "config/athlete", "key": "training_age",
     "prompt": "Have you trained before? How long, how consistently?", "extract": None, "global": False},
    {"id": "days_per_week", "page": "config/athlete", "key": "days_per_week",
     "prompt": "How many days a week can you train?", "extract": _extract_days, "global": True},
    {"id": "equipment", "page": "config/athlete", "key": "equipment",
     "prompt": "What equipment do you have? Barbell, dumbbells, machines, bands, bodyweight only?",
     "extract": None, "global": False},
    {"id": "baseline", "page": "config/athlete", "key": "strength_baseline",
     "prompt": "Know your 1RM on your main lifts? If not, what's the most weight x reps you've done recently?",
     "extract": None, "global": False},
    {"id": "measure_kinds", "page": "config/athlete", "key": "measure_kinds",
     "prompt": "Do any of these apply: timed holds, loaded carries, running, level-graded work like Otago?",
     "extract": None, "global": False},
    {"id": "age", "page": "config/athlete", "key": "age",
     "prompt": "How old are you?", "extract": _extract_age, "global": True},
    {"id": "nutrition_strictness", "page": "config/preferences", "key": "nutrition_strictness",
     "prompt": "How strict do you want nutrition guidance? None, general, or specific numbers?",
     "extract": _extract_nutrition, "global": False},
    {"id": "referral_name", "page": "config/athlete", "key": "referral_name",
     "prompt": "If something needs a referral, who's the name on file? A GP is the default.",
     "extract": None, "global": False},
    {"id": "location", "page": None, "key": None,
     "prompt": "What gym or space are you training in? Name it, so I can track its equipment.",
     "extract": None, "global": False, "location": True},
]
_FIELD_BY_ID = {f["id"]: f for f in FIELD_STEPS}

SAFETY_IDS = tuple(f"parq_{i}" for i in range(1, 8)) + ("parq_followup",)
ALL_IDS = SAFETY_IDS + tuple(f["id"] for f in FIELD_STEPS)

def _prompt_for(step_id: str) -> str:
    if step_id == "parq_followup":
        return screen.FOLLOWUP_PROMPT
    if step_id.startswith("parq_"):
        return screen.QUESTIONS[int(step_id.split("_")[1]) - 1]
    return _FIELD_BY_ID[step_id]["prompt"]

def _advance(ist: dict[str, Any], idx: int) -> tuple[int, list[str]]:
    """Skip every already-answered step (volunteered, or the synthetic-skip
    `parq_followup`), collecting one acknowledgement clause per field step."""
    acks = []
    while idx < len(ALL_IDS) and ALL_IDS[idx] in ist["answers"]:
        step_id = ALL_IDS[idx]
        if step_id in _FIELD_BY_ID:
            acks.append(f"Already got that: {ist['answers'][step_id]}.")
        idx += 1
    ist["cursor"] = idx
    return idx, acks

def _db_create_writes() -> list[Write]:
    return [{"verb": "database-create", "target": db, "payload": {"parent": PARENT}} for db in DB_ORDER]

def intake_turn(line: str, state: dict[str, Any]) -> Turn:
    state = copy.deepcopy(state)
    ist = state.get("intake", {"cursor": 0, "answers": {}, "any_yes": False})
    now = state.get("now", "")

    if TRIGGER_RE.search(line):
        # First "set me up" creates the databases and starts asking. A later
        # one (interruption, or a curious re-run) adopts them (idempotent at
        # the writer) and resumes at `intake_cursor` instead of restarting
        # (lim L-48).
        writes = _db_create_writes()
        idx, acks = _advance(ist, ist["cursor"])
        state["intake"] = ist
        if idx >= len(ALL_IDS):
            return {"writes": writes, "say": " ".join(acks + [DONE_SAY]), "state": state}
        return {"writes": writes, "say": " ".join(acks + [_prompt_for(ALL_IDS[idx])]), "state": state}

    idx = ist["cursor"]
    if idx >= len(ALL_IDS):
        state["intake"] = ist
        return {"writes": [], "say": DONE_SAY, "state": state}

    step_id = ALL_IDS[idx]
    writes: list[Write] = []

    if step_id.startswith("parq_"):
        if step_id == "parq_followup":
            writes.append(screen.clearance_write(True, line, now))
        else:
            if screen.is_yes(line):
                ist["any_yes"] = True
            if step_id == "parq_7":
                if not ist["any_yes"]:
                    writes.append(screen.clearance_write(False, "", now))
                    ist["answers"]["parq_followup"] = "n/a"
        ist["answers"][step_id] = line.strip()
    else:
        field = _FIELD_BY_ID[step_id]
        if field.get("location"):
            writes.append({"verb": "row-create", "target": "Locations", "payload": {"Name": line.strip()}})
            ist["answers"][step_id] = line.strip()
        else:
            extracted = field["extract"](line) if field["extract"] else None
            value = extracted if extracted is not None else line.strip()
            writes.append({"verb": "config-write", "target": field["page"], "payload": {field["key"]: value}})
            ist["answers"][step_id] = value
        # Out-of-order: scan the same line for any other unanswered global field.
        for other in FIELD_STEPS:
            if other["id"] == step_id or other["id"] in ist["answers"] or not other["global"]:
                continue
            found = other["extract"](line)
            if found is not None:
                writes.append({"verb": "config-write", "target": other["page"], "payload": {other["key"]: found}})
                ist["answers"][other["id"]] = found

    next_idx, acks = _advance(ist, idx + 1)
    writes.append({"verb": "config-write", "target": "config/athlete", "payload": {"intake_cursor": str(next_idx)}})
    state["intake"] = ist
    say = " ".join(acks + [_prompt_for(ALL_IDS[next_idx]) if next_idx < len(ALL_IDS) else DONE_SAY])
    return {"writes": writes, "say": say, "state": state}

def main() -> int:
    request = json.load(sys.stdin)
    json.dump(intake_turn(request["line"], request.get("state", {})), sys.stdout)
    return 0

if __name__ == "__main__":
    sys.exit(main())
