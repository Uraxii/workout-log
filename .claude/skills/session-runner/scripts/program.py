"""Program-cursor reads (build-plan s9 phase 4, docs/program-format.md
"Today, in one lookup"). `session-runner` never invents a program: `state
["program"]` is program-design's verbatim `library/*.json` template, read
back from `program/current` or threaded through the shared `state`; this
module only answers "what is today" from `program_cursor` and how it
advances (rule L17, L18). Pure functions, no I/O.

The cursor is `{"program": <name>, "node": <index>, "cycle": <n>}` and it
names the program it belongs to, because a cursor is meaningless against a
different rotation. `cursor_after` is the only way to build one, so a caller
cannot hand over a cursor whose program it forgot to state; handing over
anything else raises instead of being quietly discarded, which is what used
to happen to a hydrated cursor that missed a private companion key
(workout-log-ayf.20).
"""

from __future__ import annotations

import re
from typing import Any

import catalog

_TODAY_RE = re.compile(r"^what.*today\??$|^today'?s? (workout|session|plan)\??$", re.IGNORECASE)
_SWAP_RE = re.compile(r"^swap\s+(.+)$", re.IGNORECASE)


CURSOR_KEYS = frozenset(("program", "node", "cycle"))


def cursor_after(program: dict[str, Any], sessions_closed: int) -> dict[str, Any]:
    """Where `program`'s rotation stands after `sessions_closed` of its own
    sessions. The public constructor, and the only one: each rotation node
    consumes exactly one session, rest nodes included, so counting is the
    whole rule and no caller needs to restate the modulo."""
    length = len(program["rotation"])
    return {"program": program["name"],
            "node": sessions_closed % length,
            "cycle": sessions_closed // length}


def _checked(cursor: Any) -> dict[str, Any]:
    if not isinstance(cursor, dict) or CURSOR_KEYS != set(cursor):
        raise ValueError(
            f"program_cursor {cursor!r} is not a cursor; build it with "
            "program.cursor_after(program, sessions_closed)")
    return cursor


def ensure_cursor(state: dict[str, Any]) -> dict[str, Any]:
    """The cursor for `state["program"]`, started at the top of the rotation
    when there is none, or when the one on hand belongs to another program:
    a stale cursor could index past the end of a shorter rotation. A cursor
    that is not a cursor raises rather than being replaced, so a caller that
    got the shape wrong hears about it instead of getting a plausible
    answer for the wrong day."""
    program = state["program"]
    cursor = state.get("program_cursor")
    if cursor is not None and _checked(cursor)["program"] == program["name"]:
        return cursor
    state["program_cursor"] = cursor_after(program, 0)
    state["cursor_advanced"] = False
    return state["program_cursor"]


def current_node(program: dict[str, Any], cursor: dict[str, Any]) -> dict[str, Any]:
    return program["rotation"][cursor["node"]]


def advance(program: dict[str, Any], cursor: dict[str, Any]) -> dict[str, Any]:
    """`(node + 1) % len(rotation)`, cycle increments on wrap
    (program-format.md "Today, in one lookup"): the same operation for a
    rest node or a finished work day."""
    node = (cursor["node"] + 1) % len(program["rotation"])
    cycle = cursor["cycle"] + (1 if node == 0 else 0)
    return {"program": program["name"], "node": node, "cycle": cycle}


def advance_once(state: dict[str, Any]) -> None:
    """Advances the cursor at most once per session: a rest-node ack and a
    same-session `done for today` must never both fire (L17's rest-day
    shortcut and L11's close would otherwise skip two nodes for one day)."""
    if state.get("cursor_advanced"):
        return
    cursor = ensure_cursor(state)
    state["program_cursor"] = advance(state["program"], cursor)
    state["cursor_advanced"] = True


def _active_prescription(block: dict[str, Any]) -> dict[str, Any]:
    """`stages[stage_index]` merged over the block. No read verb
    exists yet for `stage_index` (build-plan s9 phase 4 leaves per-exercise
    progression to `load-adjust`, phase 6), so this reads stage 0, the same
    default a first-ever session would use."""
    prescription = dict(block)
    stages = block.get("stages")
    if stages:
        prescription.update(stages[0])
    return prescription


def describe_block(block: dict[str, Any]) -> str:
    """One line naming a block's exercise and its active prescription,
    measure-agnostic (build-plan s4's opener shape; no line count is
    asserted, lim L-49)."""
    label = block.get("label", "")
    prefix = f"{label} " if label else ""
    if "sequence" in block:
        steps = ", ".join(f"{s['exercise']} {s['duration_s']}s" for s in block["sequence"])
        return f"{prefix}{block.get('sets', 1)}x [{steps}]"
    prescription = _active_prescription(block)
    name = block["exercise"]
    if "duration_s" in prescription:
        return f"{prefix}{name} {prescription['duration_s']}s"
    if "level" in prescription:
        return f"{prefix}{name} level {prescription['level']}, {prescription.get('sets', 1)}x{prescription.get('reps', '')}"
    if "rep_range" in prescription:
        lo, hi = prescription["rep_range"]
        return f"{prefix}{name} {prescription.get('sets', 1)}x{lo}-{hi}"
    amrap = ", AMRAP last set" if prescription.get("amrap_last") else ""
    return f"{prefix}{name} {prescription.get('sets', 1)}x{prescription.get('reps', '')}{amrap}"


def describe_today(node: dict[str, Any]) -> str:
    """`Day <label> - <opener>` (build-plan s4). A rest node (program-
    format.md: empty `blocks`) states the label and how to move on, no
    exercise (rule L17, lim L-14); a work node names the block count and
    details up to three, matching the spec's own example's shape (name the
    day, highlight the lead lift, not a full workout dump)."""
    if not node["blocks"]:
        return f"Day {node['label']} - rest. Say 'done' when you're ready to move on."
    blocks = node["blocks"]
    lines = [describe_block(b) for b in blocks[:3]]
    more = f" (+{len(blocks) - 3} more)" if len(blocks) > 3 else ""
    plural = "" if len(blocks) == 1 else "s"
    return f"Day {node['label']} - {len(blocks)} exercise{plural}. " + "; ".join(lines) + more


def first_exercise_id(node: dict[str, Any]) -> str | None:
    """The block session-runner scopes to, so a bare set line needs no name
    (build-plan s4's own example: the opener names Squat, the next line is
    a bare `185x5`). `None` for a rest node or an all-sequence node."""
    for block in node["blocks"]:
        if "exercise" in block:
            return block["exercise"]
    return None


def try_today(text: str, state: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any] | None:
    """"what am i doing today" (s4, s9 phase 4): reads
    `rotation[program_cursor.node]`, one turn, no writes. Primes `scope` to
    the lead block so the next bare `185x5` needs no name (rule D)."""
    if _TODAY_RE.match(text) is None:
        return None
    program = state.get("program")
    if program is None:
        return {"writes": [], "confirm_line": "No active program yet; ask for a plan first.", "state": state}
    cursor = ensure_cursor(state)
    node = current_node(program, cursor)
    exercise_id = first_exercise_id(node)
    if exercise_id is not None:
        state["scope"] = [exercise_id, catalog.measure_of(exercise_id)]
    return {"writes": [], "confirm_line": describe_today(node), "state": state}


def try_swap(text: str, state: dict[str, Any], ctx: dict[str, Any], lookup) -> dict[str, Any] | None:
    """`swap <exercise>`: session-only (lim L-21's other half). Never
    rewrites `program`; just re-scopes, so the next sets logged name the
    swap, like naming any exercise directly."""
    match = _SWAP_RE.match(text)
    if match is None:
        return None
    name = match.group(1).strip()
    found = lookup(name)
    if found is None:
        return {"writes": [], "confirm_line": f"No exercise named '{name}'.", "state": state}
    exercise_id, measure = found
    state["scope"] = [exercise_id, measure]
    return {"writes": [], "confirm_line": f"Swapped to {exercise_id} for today's sets.",
           "state": state}
