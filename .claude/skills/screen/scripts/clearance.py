"""What a PAR-Q+ pass earns: the `config/limits` clearance value, and rule
S5's exit from `progression: manual`. Split out of `screen.py` (house limit,
docs/architecture.md "One script per skill" splits by domain): deciding what
a set of answers is worth is one body of knowledge, running the seven-turn
conversation is another.

`intake` imports `is_yes` and `clearance_write` through `screen` for its own
in-process PAR-Q+ block, so the rule lives here and only here (rule S8).
"""

from __future__ import annotations

import json
from typing import Any, TypedDict

# Rule S5's window, counted in LOGGED days, not calendar days.
SYMPTOM_FREE_DAYS = 14

# `Sessions.Status` on a day `pain-triage` stopped (rule L12). A day the
# athlete was halted on is not a symptom-free day, whatever else it logged.
HALTED = "halted"

_YES_WORDS = ("yes", "yeah", "yep", "y")
_NO_WORDS = ("no", "nope", "nah", "n")

# The three answers an explicit yes/no turn can carry, and the clearance each
# one earns. `None` is "the athlete said neither", which is never consent: it
# writes `pending` and the caller asks again, because a screening question
# that guesses is the failure this seam exists to prevent (ticket R4).
_CLEARANCE_BY_ANSWER = {True: "cleared", False: "referred", None: "pending"}


class Write(TypedDict):
    verb: str
    target: str
    payload: dict[str, Any]


def yes_no(line: str) -> bool | None:
    """The athlete's explicit answer, from the first word: `True` yes,
    `False` no, `None` neither. Phase 1 grammar, and deliberately not a
    negation parser: `screen` asks a yes/no question and reads a yes/no
    answer."""
    first_word = line.strip().lower().split(" ", 1)[0].strip(".,!")
    if first_word in _YES_WORDS:
        return True
    if first_word in _NO_WORDS:
        return False
    return None


def is_yes(line: str) -> bool:
    """A bare-word yes at the start of the line."""
    return yes_no(line) is True


def clearance_write(any_yes: bool, follow_up_line: str, now: str) -> Write:
    """The one config-write `screen` ever emits for clearance (rule S8):
    `screen` is the only skill that sets `config/limits.clearance` and
    `.parq_date`, whether called from its own turn loop or in-process by
    `intake`'s safety block.

    All seven NO needs no answer to read. Any YES reads the follow-up turn's
    explicit yes/no and nothing else, so a denial ("no, my clinician has not
    cleared me") can never be read as clearance.
    """
    clearance = ("cleared" if not any_yes
                 else _CLEARANCE_BY_ANSWER[yes_no(follow_up_line)])
    return {
        "verb": "config-write",
        "target": "config/limits",
        "payload": {"clearance": clearance, "parq_date": now[:10]},
    }


def _entries(limits: dict[str, Any]) -> list[dict[str, Any]]:
    """`config/limits.entries` has no sub-structure of its own in the schema,
    so `pain-triage` stores it as a JSON string and mirrors it in state as a
    list. A cold start reads back the string; parse at that boundary."""
    entries = limits.get("entries") or []
    return json.loads(entries) if isinstance(entries, str) else entries


def last_symptom_date(limits: dict[str, Any]) -> str | None:
    """The date of the athlete's most recent `stop`-level report, or `None`
    when nothing has ever been reported.

    Every `config/limits` entry is dated by `opened_at`, and `pain-triage`
    rewrites `opened_at` to today whenever it re-opens an entry for that area
    (rule S8, pain_triage.py `_reopen_entry`). So the newest `opened_at` over
    ALL entries, resolved or not, is the last symptom, and a fresh report
    moves it forward. That is what "consecutive" means in rule S5: the run
    is measured from this date, and a new report restarts it at zero.
    """
    dated = [entry["opened_at"] for entry in _entries(limits)
             if entry.get("opened_at")]
    return max(dated) if dated else None


def logged_days_since_symptom(state: dict[str, Any]) -> int:
    """Rule S5's window: how many symptom-free days the athlete has LOGGED
    since her last symptom. A day counts when all three hold.

    1. A `Sessions` row carries that local date, so training was logged.
       `state["sessions_by_date"]` is that map (hydrate.py `_sessions_by_date`).
    2. The date is strictly after `last_symptom_date`. The day a symptom was
       reported is not a symptom-free day.
    3. The session was not left `halted`, which is what `pain-triage` does to
       the day it stops (rule L12).

    Calendar days are not a legal substitute. Counting them let an athlete who
    crashed, trained nothing for two weeks and re-screened take the brake off
    with no recovery demonstrated at all, which is build-plan s11 risk 19
    ("a PEM crash has no trigger; `progression: manual` self-clears") built
    rather than prevented.

    No dated entry means no anchor to count from, which fails closed at zero:
    `progression: manual` is only ever written alongside an entry, so the
    pairing missing is corruption, not consent.
    """
    since = last_symptom_date(state.get("limits", {}))
    if since is None:
        return 0
    sessions = state.get("sessions_by_date") or {}
    return sum(1 for day, session in sessions.items()
               if day > since and session.get("status") != HALTED)


def progression_writes(state: dict[str, Any]) -> list[Write]:
    """Rule S5: a completed `screen` re-run is one of the two things that
    clears `progression: manual` (build-plan s6 skill table). It clears
    nothing on its own; the logged-day window has to hold too."""
    if state.get("limits", {}).get("progression") != "manual":
        return []
    if logged_days_since_symptom(state) < SYMPTOM_FREE_DAYS:
        return []
    return [{"verb": "config-write", "target": "config/limits",
             "payload": {"progression": "auto"}}]
