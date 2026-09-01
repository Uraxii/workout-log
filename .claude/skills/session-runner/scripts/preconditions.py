"""Rule S2 in the logging path itself: a halted session takes no set writes.

`trainer-core` is the documented gate (build-plan s6 skill table), but it is
a separate seam, and "loaded unconditionally before every other skill" is
prose that nothing executes. `log_set` is reachable on its own, so the rule
has to hold at this seam too, or it does not hold at all (workout-log-qdb).

The check reads the writes a turn actually produced, not the line the user
typed. A line-shaped check only catches the handlers someone remembered to
route through it; a write-shaped one catches every handler in `log_set.py`
including ones not written yet, because there is no way to emit a `Sets` row
out of this seam except through the turn it returns. `done for today` writes
only `Sessions` and still passes, which is what S2 says ("no SET writes")
and what `fixtures/03-session-status` proves.

The refusal wording lives in `trainer_core.py` and is imported, never
copied: two copies of a user-facing string drift.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any

# `<skills>/session-runner/scripts` -> `<skills>/trainer-core/scripts`, the
# same relative walk `rows.py` and `catalog.py` use for shared repo data, and
# it holds in the built ZIP too (every skill unpacks as a sibling directory).
_TRAINER_CORE_SCRIPTS = Path(__file__).resolve().parents[2] / "trainer-core" / "scripts"
if str(_TRAINER_CORE_SCRIPTS) not in sys.path:
    sys.path.append(str(_TRAINER_CORE_SCRIPTS))

import trainer_core  # noqa: E402  (resolved by the path append above)

SET_TARGET = "Sets"


def no_sets_while_halted(turn: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    """S2, rule L12: if this turn would write a `Sets` row while the session
    is halted, drop the whole turn and refuse instead, naming the failed
    precondition. `before` is the turn's own pre-call state, returned
    unchanged so the cursor never advances either (L12's second half)."""
    refusal = trainer_core.halted_set_refusal(before)
    if refusal is None:
        return turn
    if not any(write["target"] == SET_TARGET for write in turn["writes"]):
        return turn
    return {"writes": [], "confirm_line": refusal, "state": copy.deepcopy(before)}
