"""The seam for `screen`: PAR-Q+ verbatim, follow-ups only on YES (build-plan
s6, s6.1 rule S8). Same shape as `intake_turn` and `log_set`:

    python3 screen.py                 # {"line":..., "state":...} on stdin, Turn on stdout
    from screen import screen_turn    # in-process, called by `intake` inline

Deterministic and pure besides one local, static read of the verbatim
question text (`references/parq-plus.md`), so the seven questions are never
hand-copied into this script (build-plan s9, mirrors `intake`'s db-create
payload rule). No network, no Notion.

`state["screen"]`: `{"cursor": 0..7, "stage": "asking"|"followup"|"done",
"any_yes": bool}`. `cursor` counts answered questions, so a resumed
conversation (fresh process, `state` carried over) picks up the next
unanswered one. `stage` stays `"followup"` until the athlete answers the
clearance question yes or no; nothing else advances it (ticket R4).

The clearance and `progression: manual` rules live in `clearance.py`, which
`intake` reaches through this module's re-exports.
"""

from __future__ import annotations

import copy
import re
import sys
import json
from pathlib import Path
from typing import Any, TypedDict

from clearance import (SYMPTOM_FREE_DAYS, Write, clearance_write, is_yes,
                       logged_days_since_symptom, progression_writes, yes_no)

REFERENCES = Path(__file__).resolve().parent.parent / "references" / "parq-plus.md"
_QUESTION_RE = re.compile(r'^\d+\.\s+"(.+)"$', re.MULTILINE)


class Turn(TypedDict):
    writes: list[Write]
    say: str
    state: dict[str, Any]


def _questions() -> list[str]:
    """The seven verbatim PAR-Q+ questions, parsed once from the reference
    file so this script carries no second copy of licensed text."""
    text = REFERENCES.read_text()
    found = _QUESTION_RE.findall(text)
    if len(found) != 7:
        raise ValueError(f"expected 7 PAR-Q+ questions in {REFERENCES}, found {len(found)}")
    return found


QUESTIONS = _questions()
FOLLOWUP_PROMPT = ("Has a clinician already cleared you for exercise? Answer "
                    "yes or no first, then name the condition and the date you "
                    "were cleared.")
CLEARANCE_REASK = ("I need a plain yes or no: has a clinician already cleared "
                    "you for exercise? Clearance stays pending until you "
                    "answer, so no session can open.")
ALL_NO_SAY = "All clear on PAR-Q+. Cleared for physical activity."
PROGRESSION_CLEARED_SAY = ("Progression goes back to automatic: a fresh screen "
                            f"plus {SYMPTOM_FREE_DAYS} logged days with no "
                            "symptom reported (rule S5).")
# The count goes in the line the athlete reads, so the brake she cannot
# otherwise inspect says how far along she is and what it is waiting for.
PROGRESSION_HELD_SAY = ("Progression stays manual: rule S5 also needs "
                         f"{SYMPTOM_FREE_DAYS} days of training logged with no "
                         "symptom reported, and you have logged {logged} since "
                         "your last one.")
ON_FILE_SAY = "PAR-Q+ already on file."

_SAY_BY_CLEARANCE = {
    "cleared": "Noted, and clearance recorded. Cleared for physical activity.",
    "referred": ("Noted. That needs a clinician's clearance before I program "
                 "anything; light walking only until then."),
    "pending": CLEARANCE_REASK,
}


def _complete(state: dict[str, Any], screen_state: dict[str, Any],
              any_yes: bool, line: str) -> Turn:
    """The end of a pass: write clearance, and on a cleared re-screen decide
    rule S5's exit from `progression: manual`."""
    writes = [clearance_write(any_yes, line, state.get("now", ""))]
    clearance = writes[0]["payload"]["clearance"]
    say = _SAY_BY_CLEARANCE[clearance] if any_yes else ALL_NO_SAY

    if clearance == "pending":
        state["screen"] = screen_state  # stage stays "followup": ask again
        return {"writes": writes, "say": say, "state": state}

    if clearance == "cleared":
        progression = progression_writes(state)
        writes += progression
        if progression:
            state["limits"] = {**state.get("limits", {}), "progression": "auto"}
            say = f"{say} {PROGRESSION_CLEARED_SAY}"
        elif state.get("limits", {}).get("progression") == "manual":
            held = PROGRESSION_HELD_SAY.format(
                logged=logged_days_since_symptom(state))
            say = f"{say} {held}"

    screen_state["stage"] = "done"
    state["screen"] = screen_state
    return {"writes": writes, "say": say, "state": state}


def screen_turn(line: str, state: dict[str, Any]) -> Turn:
    """One PAR-Q+ turn, for `screen` firing on its own (build-plan s6: also
    re-fires on any health change, outside `intake`). Ask the next question,
    or process the answer to the last one asked, and write clearance once
    the pass completes."""
    state = copy.deepcopy(state)
    screen_state = state.get("screen", {"cursor": 0, "stage": "asking", "any_yes": False})
    stage = screen_state.get("stage", "asking")
    cursor = screen_state.get("cursor", 0)

    if stage == "followup":
        return _complete(state, screen_state, True, line)
    if stage != "asking":
        return {"writes": [], "say": ON_FILE_SAY, "state": state}

    if cursor > 0 and is_yes(line):
        screen_state["any_yes"] = True

    if cursor < 7:
        screen_state["cursor"] = cursor + 1
        state["screen"] = screen_state
        return {"writes": [], "say": QUESTIONS[cursor], "state": state}

    if screen_state["any_yes"]:
        screen_state["stage"] = "followup"
        state["screen"] = screen_state
        return {"writes": [], "say": FOLLOWUP_PROMPT, "state": state}

    return _complete(state, screen_state, False, "")


def main() -> int:
    request = json.load(sys.stdin)
    json.dump(screen_turn(request["line"], request.get("state", {})), sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
