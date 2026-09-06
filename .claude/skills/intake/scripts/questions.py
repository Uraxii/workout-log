"""The intake question table and the cursor that walks it.

Split out of `intake.py` (house limit, docs/architecture.md "One script per
skill" splits by DOMAIN): what gets asked and in what order is one body of
knowledge. Turning an answer into writes is another, and stays in
`intake.py`; reading a value out of a chat line is a third, and lives in
`readers.py`.

`parse` returning `None` is the whole re-ask rule (ticket workout-log-481).
A step whose answer does not parse is re-entered instead of advanced past,
expressed once here for every row of the table, so no step carries a retry
branch of its own. Before this, only the PAR-Q+ follow-up could produce an
unparseable answer that mattered, and it advanced anyway: clearance landed
on `pending` and nothing ever asked again.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "screen" / "scripts"))
import screen  # noqa: E402  (skill-to-skill seam import, mirrors intake.py's own)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import readers  # noqa: E402  (same-dir readers; the dir name is not importable)
import storage  # noqa: E402  (same-dir storage; the dir name is not importable)


# One row per question. Two reader slots, because they do two different jobs:
# `answer` reads a direct reply to THIS question ("4"), `scan` hunts the
# same field inside a line answering a different one ("lb, and I train 4
# days", lim L-47) and so needs the unit word to be sure. `reask` is what
# the athlete reads when her answer did not parse; a row without one
# repeats its prompt. `section` (only value used today: `"storage"`) puts a
# row ahead of PAR-Q+ in `ALL_IDS`; every other row runs after. `state_key`
# names the state key the answer also lands on, for the values a later turn
# of the same chat needs in hand and not only on the page they were written
# to (ticket workout-log-36h).
#
# `ROOT_STEP_ID` is the one row that carries no `prompt`, `reask` or
# `answer` of its own: a Notion page link and a path to a vault folder are
# the same question asked by two stores, so the store profile owns its
# words and its reader (`ddl.ROOT_PROMPT`, `vault.root_parse`, and the rest
# of the names every profile answers). That is why `prompt_for`,
# `reask_for` and `parse` each take a profile.

ROOT_STEP_ID = "storage_root"


def _storage_refusal(value: str) -> str | None:
    """`None` when the athlete named a store this build can write to;
    otherwise the line she reads instead of the next question
    (docs/storage-section-design.md "Refusing a store")."""
    return None if storage.is_proven(value) else storage.refusal(value)


FIELD_STEPS: list[dict[str, Any]] = [
    {"id": "storage_platform", "page": "config/athlete", "key": "storage_platform",
     "section": "storage", "state_key": "storage_platform",
     "prompt": f"Where do you want your training log kept? {storage.proven_stores()} are what I can write to today. Name anything else and I'll tell you straight away rather than half build it.",
     "answer": readers.platform,
     "reask": f"I need the name of a place to put it. {storage.proven_stores()} are the ones I can write to today.",
     "refuse": _storage_refusal},
    {"id": ROOT_STEP_ID, "page": "config/athlete", "key": ROOT_STEP_ID,
     "section": "storage", "state_key": ROOT_STEP_ID},
    {"id": "timezone", "page": "config/athlete", "key": "timezone",
     "section": "storage", "state_key": "tz",
     "prompt": "What timezone are you in? I need it as an IANA name, like America/Los_Angeles or Europe/London, so a late session lands on the right day.",
     "answer": readers.timezone,
     "reask": "I don't know that zone. It's Area/City, capitals and all, like America/New_York or Australia/Sydney."},
    {"id": "units", "page": "config/preferences", "key": "units",
     "state_key": "units",
     "prompt": "Pounds or kilos?", "answer": readers.units, "scan": readers.units,
     "reask": "Pounds or kilos? One or the other, please."},
    {"id": "jurisdiction", "page": "config/athlete", "key": "jurisdiction",
     "prompt": "What country or state are you in? Scope-of-practice rules vary.",
     "answer": readers.free_text},
    {"id": "goal", "page": "config/athlete", "key": "goal",
     "prompt": "What's the goal? Strength, muscle, fat loss, endurance, sport, general health, or rehab-adjacent?",
     "answer": readers.free_text},
    {"id": "training_age", "page": "config/athlete", "key": "training_age",
     "prompt": "Have you trained before? How long, how consistently?", "answer": readers.free_text},
    {"id": "days_per_week", "page": "config/athlete", "key": "days_per_week",
     "prompt": "How many days a week can you train?",
     "answer": readers.days_answer, "scan": readers.days_in_sentence,
     "reask": "I need a number of days. How many days a week can you train?"},
    {"id": "equipment", "page": "config/athlete", "key": "equipment",
     "prompt": "What equipment do you have? Barbell, dumbbells, machines, bands, bodyweight only?",
     "answer": readers.free_text},
    {"id": "baseline", "page": "config/athlete", "key": "strength_baseline",
     "prompt": "Know your 1RM on your main lifts? If not, what's the most weight x reps you've done recently?",
     "answer": readers.free_text},
    {"id": "measure_kinds", "page": "config/athlete", "key": "measure_kinds",
     "prompt": "Do any of these apply: timed holds, loaded carries, running, level-graded work like Otago?",
     "answer": readers.free_text},
    {"id": "age", "page": "config/athlete", "key": "age",
     "prompt": "How old are you?", "answer": readers.age_answer, "scan": readers.age_in_sentence,
     "reask": "I need a number. How old are you?"},
    {"id": "nutrition_strictness", "page": "config/preferences", "key": "nutrition_strictness",
     "prompt": "How strict do you want nutrition guidance? None, general, or specific numbers?",
     "answer": readers.nutrition,
     "reask": "None, general, or specific numbers? Pick one of those three."},
    {"id": "referral_name", "page": "config/athlete", "key": "referral_name",
     "prompt": "If something needs a referral, who's the name on file? A GP is the default.",
     "answer": readers.free_text},
    {"id": "location", "page": "config/preferences", "key": "location",
     "prompt": "What gym or space are you training in? Name it, so I can track its equipment.",
     "answer": readers.free_text},
]

FIELD_BY_ID = {step["id"]: step for step in FIELD_STEPS}

SAFETY_IDS = tuple(f"parq_{i}" for i in range(1, 8)) + ("parq_followup",)

# Three questions about the tool, then every question after is about her.
# The storage platform is first because the athlete has to name a store
# before anything else about it makes sense
# (docs/storage-section-design.md question 1), and because the store she
# names owns the words of the question after it; the storage root is
# second because the database creates fire from the "set me up" turn
# onward and each one needs it (ticket workout-log-mqs); the timezone is
# third because it is frozen onto session 1 (rule L3) and a session can
# open long before the profile is finished (ticket workout-log-ayf.16).
# Each row says for itself which side of PAR-Q+ it sits on, so adding or
# renaming a row cannot silently reorder the flow.
ALL_IDS = (tuple(s["id"] for s in FIELD_STEPS if s.get("section") == "storage")
           + SAFETY_IDS
           + tuple(s["id"] for s in FIELD_STEPS if s.get("section") != "storage"))


def prompt_for(step_id: str, profile: ModuleType | None) -> str:
    """The question the athlete reads when this step comes up.

    `profile` is the store profile from `storage.profile`, and only
    `ROOT_STEP_ID` reads it. That step is unreachable until the athlete has
    named a store this build can write to, because an unproven answer holds
    the cursor on `storage_platform`, so `None` never reaches a profile
    name.
    """
    if step_id == ROOT_STEP_ID:
        return profile.ROOT_PROMPT
    if step_id == "parq_followup":
        return screen.FOLLOWUP_PROMPT
    if step_id.startswith("parq_"):
        return screen.QUESTIONS[int(step_id.split("_")[1]) - 1]
    return FIELD_BY_ID[step_id]["prompt"]


def parse(step_id: str, line: str, profile: ModuleType | None) -> Any | None:
    """This step's answer, or `None` when the line does not answer it.

    `None` is never a value and never a default: it routes to `reask_for`
    and the cursor stays put (ticket workout-log-481). PAR-Q+ and its
    follow-up read an explicit yes or no, so "maybe" is not silently a NO;
    `units` and `nutrition_strictness` accept only what they can map, so
    `config/preferences` is never handed a sentence its own schema enum
    would then reject. The store root reads whatever its own store accepts,
    a page link or a vault path, and rejects the other one the same way.
    """
    if step_id == ROOT_STEP_ID:
        return profile.root_parse(line)
    if step_id in SAFETY_IDS:
        return screen.yes_no(line)
    return FIELD_BY_ID[step_id]["answer"](line)


def reask_for(step_id: str, profile: ModuleType | None) -> str:
    """What the athlete reads when her answer did not parse. The seven
    PAR-Q+ questions stay verbatim inside it (build-plan s6.1 rule S8)."""
    if step_id == ROOT_STEP_ID:
        return profile.ROOT_REASK
    if step_id == "parq_followup":
        return screen.CLEARANCE_REASK
    if step_id.startswith("parq_"):
        return f"I need a yes or a no. {prompt_for(step_id, profile)}"
    return FIELD_BY_ID[step_id].get("reask", prompt_for(step_id, profile))


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
