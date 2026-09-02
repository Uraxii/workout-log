"""The intake question table and the cursor that walks it.

Split out of `intake.py` (house limit, docs/architecture.md "One script per
skill" splits by DOMAIN): what gets asked, in what order, and whether a
given chat line answers it is one body of knowledge. Turning an answer into
Notion writes is another, and stays in `intake.py`.

`parse` returning `None` is the whole re-ask rule (ticket workout-log-481).
A step whose answer does not parse is re-entered instead of advanced past,
expressed once here for every row of the table, so no step carries a retry
branch of its own. Before this, only the PAR-Q+ follow-up could produce an
unparseable answer that mattered, and it advanced anyway: clearance landed
on `pending` and nothing ever asked again.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "screen" / "scripts"))
import screen  # noqa: E402  (skill-to-skill seam import, mirrors intake.py's own)

Reader = Callable[[str], Any | None]


def _free_text(line: str) -> str | None:
    return line.strip() or None


def _bare_number(line: str) -> str | None:
    """A line that is only a number, which is what a direct reply to "how
    many days" or "how old are you" usually is."""
    m = re.fullmatch(r"\s*(\d{1,3})\s*", line)
    return m.group(1) if m else None


def _units(line: str) -> str | None:
    m = re.search(r"\b(lbs?|pounds?|kgs?|kilos?|kilograms?)\b", line, re.I)
    if not m:
        return None
    return "kg" if m.group(1).lower().startswith(("kg", "kilo")) else "lb"


def _days_in_sentence(line: str) -> str | None:
    m = re.search(r"\b(\d+)\s*days?\b", line, re.I)
    return m.group(1) if m else None


def _age_in_sentence(line: str) -> str | None:
    m = (re.search(r"\b(\d{1,3})\s*(?:years?\s*old|yo)\b", line, re.I)
         or re.search(r"\bi'?m\s+(\d{1,3})\b", line, re.I))
    return m.group(1) if m else None


def _nutrition(line: str) -> str | None:
    low = line.lower()
    for word in ("none", "general", "specific"):
        if word in low:
            return word
    return None


def _days_answer(line: str) -> str | None:
    return _days_in_sentence(line) or _bare_number(line)


def _age_answer(line: str) -> str | None:
    return _age_in_sentence(line) or _bare_number(line)


# One row per question. Two readers, because they do two different jobs:
# `answer` reads a direct reply to THIS question ("4"), `scan` hunts the
# same field inside a line answering a different one ("lb, and I train 4
# days", lim L-47) and so needs the unit word to be sure. `reask` is what
# the athlete reads when her answer did not parse; a row without one
# repeats its prompt.
FIELD_STEPS: list[dict[str, Any]] = [
    {"id": "units", "page": "config/preferences", "key": "units",
     "prompt": "Pounds or kilos?", "answer": _units, "scan": _units,
     "reask": "Pounds or kilos? One or the other, please."},
    {"id": "jurisdiction", "page": "config/athlete", "key": "jurisdiction",
     "prompt": "What country or state are you in? Scope-of-practice rules vary.",
     "answer": _free_text},
    {"id": "goal", "page": "config/athlete", "key": "goal",
     "prompt": "What's the goal? Strength, muscle, fat loss, endurance, sport, general health, or rehab-adjacent?",
     "answer": _free_text},
    {"id": "training_age", "page": "config/athlete", "key": "training_age",
     "prompt": "Have you trained before? How long, how consistently?", "answer": _free_text},
    {"id": "days_per_week", "page": "config/athlete", "key": "days_per_week",
     "prompt": "How many days a week can you train?",
     "answer": _days_answer, "scan": _days_in_sentence,
     "reask": "I need a number of days. How many days a week can you train?"},
    {"id": "equipment", "page": "config/athlete", "key": "equipment",
     "prompt": "What equipment do you have? Barbell, dumbbells, machines, bands, bodyweight only?",
     "answer": _free_text},
    {"id": "baseline", "page": "config/athlete", "key": "strength_baseline",
     "prompt": "Know your 1RM on your main lifts? If not, what's the most weight x reps you've done recently?",
     "answer": _free_text},
    {"id": "measure_kinds", "page": "config/athlete", "key": "measure_kinds",
     "prompt": "Do any of these apply: timed holds, loaded carries, running, level-graded work like Otago?",
     "answer": _free_text},
    {"id": "age", "page": "config/athlete", "key": "age",
     "prompt": "How old are you?", "answer": _age_answer, "scan": _age_in_sentence,
     "reask": "I need a number. How old are you?"},
    {"id": "nutrition_strictness", "page": "config/preferences", "key": "nutrition_strictness",
     "prompt": "How strict do you want nutrition guidance? None, general, or specific numbers?",
     "answer": _nutrition,
     "reask": "None, general, or specific numbers? Pick one of those three."},
    {"id": "referral_name", "page": "config/athlete", "key": "referral_name",
     "prompt": "If something needs a referral, who's the name on file? A GP is the default.",
     "answer": _free_text},
    {"id": "location", "page": None, "key": None,
     "prompt": "What gym or space are you training in? Name it, so I can track its equipment.",
     "answer": _free_text, "location": True},
]

FIELD_BY_ID = {step["id"]: step for step in FIELD_STEPS}

SAFETY_IDS = tuple(f"parq_{i}" for i in range(1, 8)) + ("parq_followup",)
ALL_IDS = SAFETY_IDS + tuple(step["id"] for step in FIELD_STEPS)


def prompt_for(step_id: str) -> str:
    """The question the athlete reads when this step comes up."""
    if step_id == "parq_followup":
        return screen.FOLLOWUP_PROMPT
    if step_id.startswith("parq_"):
        return screen.QUESTIONS[int(step_id.split("_")[1]) - 1]
    return FIELD_BY_ID[step_id]["prompt"]


def parse(step_id: str, line: str) -> Any | None:
    """This step's answer, or `None` when the line does not answer it.

    `None` is never a value and never a default: it routes to `reask_for`
    and the cursor stays put (ticket workout-log-481). PAR-Q+ and its
    follow-up read an explicit yes or no, so "maybe" is not silently a NO;
    `units` and `nutrition_strictness` accept only what they can map, so
    `config/preferences` is never handed a sentence its own schema enum
    would then reject.
    """
    if step_id in SAFETY_IDS:
        return screen.yes_no(line)
    return FIELD_BY_ID[step_id]["answer"](line)


def reask_for(step_id: str) -> str:
    """What the athlete reads when her answer did not parse. The seven
    PAR-Q+ questions stay verbatim inside it (build-plan s6.1 rule S8)."""
    if step_id == "parq_followup":
        return screen.CLEARANCE_REASK
    if step_id.startswith("parq_"):
        return f"I need a yes or a no. {prompt_for(step_id)}"
    return FIELD_BY_ID[step_id].get("reask", prompt_for(step_id))


def advance(answers: dict[str, Any], idx: int) -> tuple[int, list[str]]:
    """The next step still unanswered, and one acknowledgement clause per
    field step skipped because the athlete already volunteered it (lim
    L-47)."""
    acks = []
    while idx < len(ALL_IDS) and ALL_IDS[idx] in answers:
        step_id = ALL_IDS[idx]
        if step_id in FIELD_BY_ID:
            acks.append(f"Already got that: {answers[step_id]}.")
        idx += 1
    return idx, acks


def volunteered(line: str, answered: dict[str, Any],
                asked_id: str) -> list[tuple[dict[str, Any], str]]:
    """Every other scannable field this one line also answers (lim L-47),
    as `(step, value)` pairs in table order."""
    found = []
    for step in FIELD_STEPS:
        if step["id"] == asked_id or step["id"] in answered or "scan" not in step:
            continue
        value = step["scan"](line)
        if value is not None:
            found.append((step, value))
    return found
