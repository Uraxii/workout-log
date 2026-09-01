"""The seam for `trainer-core`: `gate_turn(line, state) -> Turn` (build-plan
s6, s6.1 rules S1, S2). Same shape as `log_set`, `screen_turn`, `intake_turn`:

    python3 trainer_core.py             # {"line":..., "state":...} on stdin, Turn on stdout
    from trainer_core import gate_turn  # in-process, called before every coaching turn

`trainer-core` gates, it never writes (build-plan s6 skill table): `Turn.writes`
is always `[]`. An empty `say` means no objection, so the caller's own skill
runs the turn untouched; a non-empty `say` is a refusal that names the failed
precondition, per S1's requirement that a refusal is never generic
(`references/scope-and-refusals.md`).

`state["session_status"]` is `None` until a session opens, then `"open"` or
`"halted"`; `pain-triage` is the only writer of `"halted"` (rule L12).
`state["limits"]` mirrors `config/limits`: `{"clearance": str, "entries": [...]}`.
`state["has_program"]` mirrors whether `program/current` exists. Neither this
module nor the fixture harness reads Notion; both are set by the caller from
whatever it already has in hand, same convention as `screen`'s `state["screen"]`.
"""

from __future__ import annotations

import copy
import json
import sys
from typing import Any, TypedDict

_ACK_WORDS = frozenset({"ok", "okay", "got it", "understood", "noted", "yes", "acknowledged"})
_CLEARED = frozenset({"cleared", "not_required"})

# The one wording for S2. Every seam that could write a set says this exact
# line, so a reader hears one voice whichever seam the turn reached
# (`references/scope-and-refusals.md` S2).
HALTED_SAY = ("Session is halted (Status: halted) until you acknowledge the "
              "hand-off. No sets logged until then.")


class Write(TypedDict):
    verb: str
    target: str
    payload: dict[str, Any]


class Turn(TypedDict):
    writes: list[Write]
    say: str
    state: dict[str, Any]


def halted_set_refusal(state: dict[str, Any]) -> str | None:
    """S2, rule L12, stated for any seam that can write a set: `None` when
    the session is not halted, otherwise the refusal that seam must return
    instead of the writes. `session-runner` imports this rather than keeping
    a second copy of the wording (`preconditions.py`)."""
    return None if state.get("session_status") != "halted" else HALTED_SAY


def _halted_refusal(line: str) -> str | None:
    """The gate's own line-aware half: an acknowledgement of the hand-off is
    the one line it lets through un-refused."""
    if line.strip().lower() in _ACK_WORDS:
        return None
    return HALTED_SAY


def _open_precondition_failure(state: dict[str, Any]) -> str | None:
    """S1: the precondition that failed, named, never a generic decline."""
    clearance = state.get("limits", {}).get("clearance")
    if clearance not in _CLEARED:
        return f"Precondition failed: clearance is {clearance!r}, not cleared."
    if not state.get("has_program"):
        return "Precondition failed: no program/current exists."
    return None


def gate_turn(line: str, state: dict[str, Any]) -> Turn:
    """Runs before any other skill sees the turn (build-plan s6 skill table:
    trainer-core loads unconditionally). `trainer-core` never writes; it only
    passes or refuses."""
    state = copy.deepcopy(state)

    if state.get("session_status") == "halted":
        refusal = _halted_refusal(line)
        if refusal is not None:
            return {"writes": [], "say": refusal, "state": state}

    if state.get("session_status") is None:
        refusal = _open_precondition_failure(state)
        if refusal is not None:
            return {"writes": [], "say": refusal, "state": state}

    return {"writes": [], "say": "", "state": state}


def main() -> int:
    request = json.load(sys.stdin)
    json.dump(gate_turn(request["line"], request.get("state", {})), sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
