"""The seam for `load-adjust`: `adjust_turn(line, state) -> Turn` (build-plan
s6, s6.1 rules S5, S7, s1.6, s1.7). Same shape as `log_set`, `triage_turn`:

    python3 load_adjust.py               # {"line":..., "state":...} on stdin, Turn on stdout
    from load_adjust import adjust_turn  # in-process, from the replay runner

No upstream skill in this build writes a per-exercise progression rule into
`state` yet (`session-runner` never calls `load-adjust`, `program-design`
never hands it a block), so this seam owns a small, self-contained turn
grammar instead of inventing a Notion read this phase has no verb for
(`docs/architecture.md` "script seam": `(line, state)` is the whole input).
Three line shapes, checked in this order:

1. `setup\t<exercise>\taxis=...\tincrement=...\t...` seeds or replaces that
   exercise's progression rule (`docs/program-format.md` "Progression rule"
   shape: `axis`, `increment`, `rep_range`, `on_miss`, `deload_pct`,
   `after_misses`, plus `current` and optional `hrt`). No writes: this
   mirrors what a real caller would already have in hand from reading
   `program/current` (same convention `trainer_core.py` documents for its
   own mirrors).
2. A yes/no reply to a pending deload ask (rule S7's "deloads ask first").
3. `<exercise>\t<sets>[\trpe=<n>]` reports one session's sets and evaluates
   the rule (arithmetic lives in `rules.py`). `<sets>` is comma-separated:
   `185x8` (absolute), `bw+25x8` (added), `bw-25x8` (assist), or bare `8`
   for a `level`/`variation` axis.

Anything else is free text: a bare reassurance ("I'm fine") or a performance
question, both handled with no writes. A line that looks like shape 1 or 3
but carries a number the grammar cannot read is refused out loud by name,
with nothing written and nothing guessed (ayf.12); `say.unreadable` argues
why that beats both a traceback and a silent "Noted.".

HYPOTHESIS: `axis: level` reuses the same top-of-rep-range trigger as
`axis: weight` rather than Otago's session-count `advance_when`
(`sessions_at_stage`); that dosage-based advance is real but unbuilt this
pass (see SKILL.md).
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any, TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-design" / "scripts"))

import parse
import program_page
import rules
import say

_YES = frozenset({"yes", "y", "do it", "sure", "go ahead"})
_NO = frozenset({"no", "n", "not yet", "hold off", "skip it"})
_REASSURANCE = frozenset({"i'm fine", "im fine", "fine", "all good", "i am fine", "good"})


class Write(TypedDict):
    verb: str
    target: str
    payload: dict[str, Any]


class Turn(TypedDict):
    writes: list[Write]
    say: str
    state: dict[str, Any]


def _write(state: dict[str, Any], name: str, fields: dict[str, Any]) -> Write:
    """Per-exercise progression state, on `agent/progression-state`: the
    agent's own bookkeeping, not the athlete's program. There is no
    `Exercises` row to hang it on: Notion holds logs only, and this is not a
    log. `program_page` owns the page shape and rejects a field it does not
    carry, so a rule cannot invent a column the way it could on a database."""
    progression = program_page.merge_progression(
        state.setdefault("progression", {}), name, fields)
    return program_page.progression_write(progression)


def _stored_value(cfg: dict[str, Any], result: dict[str, Any]) -> Any:
    """`next_target` reads as `"<num> <unit>"` text; `stage_index` and
    `variation_index` are plain numbers (rules S7, lim L-20). `next_stage`
    always targets `stage_index`, independent of the block's own axis."""
    if result["outcome"] == "bump" and cfg["axis"] == "weight":
        return say.fmt(cfg, result['value'])
    return int(result["value"])


def _evaluate_turn(state: dict[str, Any], name: str, cfg: dict[str, Any],
                   rest: str) -> tuple[list[Write], str]:
    parts = rest.split("\t")
    set_rows, kind = parse.sets(parts[0])
    result = rules.evaluate(cfg, set_rows, kind, parse.rpe(parts[1:]))
    result["kind"] = kind

    writes: list[Write] = []
    if "field" in result:
        writes.append(_write(state, name, {result["field"]: _stored_value(cfg, result),
                                           "fail_count": cfg["fail_count"]}))
    elif "fail_count" in result:
        writes.append(_write(state, name, {"fail_count": result["fail_count"]}))
    return writes, say.OUTCOME[result['outcome']](name, cfg, result)


def _decline_or_accept(state: dict[str, Any], name: str, cfg: dict[str, Any],
                       text: str) -> tuple[list[Write], str]:
    pending = cfg["pending_deload"]
    cfg["pending_deload"] = None
    if text in _YES:
        cfg["current"] = pending["proposed"]
        cfg["fail_count"] = 0
        field = rules.TARGET_FIELD[cfg["axis"]]
        value = say.fmt(cfg, pending['proposed'])
        return [_write(state, name, {field: value, "last_deload_at": "today",
                                     "fail_count": 0})], \
            f"{name}: deloaded to {value}."
    cfg["declined_streak"] = cfg["fail_count"]
    return [_write(state, name, {"deload_declined_at": "today"})], \
        f"{name}: keeping the current load. Won't ask again for this streak (rule L-22)."


def _performance_question(name: str | None, cfg: dict[str, Any] | None, state: dict[str, Any]) -> str:
    hrt = (cfg or {}).get("hrt") or state.get("athlete", {}).get("hrt")
    if hrt in say.HRT_NOTE:
        return say.HRT_NOTE[hrt]
    return f"No trend data yet for {name}." if name else "Ask about one exercise by name."


def _is_manual(state: dict[str, Any]) -> bool:
    """Rule S5's hard off switch, read from `config/limits.progression`."""
    return state.get("limits", {}).get("progression") == "manual"


def _route(text: str, state: dict[str, Any]) -> tuple[list[Write], str]:
    """Every branch of the turn grammar. A branch returns here, never to the
    seam's caller, so the S5 gate sees every write this module makes."""
    # The progression RULE per exercise, seeded by a `setup` line and held
    # for this chat. Not a store: `state["progression"]` is the part that
    # persists, and `agent/progression-state` is where it goes.
    rules_by_exercise = state.setdefault("rules_by_exercise", {})

    if text.startswith("setup\t"):
        fields = text.split("\t")[1:]
        name, cfg = fields[0], parse.setup_config(fields[1:])
        rules_by_exercise[name] = cfg
        return [], f"Progression set for {name}."

    pending = next((n for n, c in rules_by_exercise.items()
                    if c.get("pending_deload")), None)
    if pending and text.lower() in _YES | _NO:
        return _decline_or_accept(state, pending, rules_by_exercise[pending],
                                  text.lower())

    if "\t" in text:
        name, rest = text.split("\t", 1)
        cfg = rules_by_exercise.get(name)
        if cfg is not None:
            return _evaluate_turn(state, name, cfg, rest)

    if text.lower() in _REASSURANCE:
        return [], say.NO_BARE_CLEAR if _is_manual(state) else "Noted."

    if text.endswith("?") or text.lower().startswith(("why", "how")):
        name = next((n for n in rules_by_exercise if n.lower() in text.lower()), None)
        return [], _performance_question(name, rules_by_exercise.get(name), state)

    return [], "Noted."


def adjust_turn(line: str, state: dict[str, Any]) -> Turn:
    """The seam's one exit. `_route` decides the turn, then rule S5's off
    switch drops every write it produced, and the state those writes came
    from. A branch added to `_route` cannot return around this (9vm), and a
    token the grammar cannot read cannot raise past it (ayf.12): the refusal
    discards `routed` wholesale, so a rule half-built before the bad field
    cannot survive into the next turn.

    `strip` spares tabs on purpose. `"Squat\t"` stripped to `"Squat"` fell
    through to a bare "Noted." — the silent no-op that cost the athlete the
    set. Keeping the tab routes it to the grammar, which refuses out loud."""
    routed = copy.deepcopy(state)
    try:
        writes, line_out = _route(line.strip(" \r\n"), routed)
    except parse.Unreadable as bad:
        return {"writes": [], "say": say.unreadable(bad), "state": copy.deepcopy(state)}
    if writes and _is_manual(state):
        return {"writes": [], "say": say.MANUAL, "state": copy.deepcopy(state)}
    return {"writes": writes, "say": line_out, "state": routed}


def main() -> int:
    request = json.load(sys.stdin)
    json.dump(adjust_turn(request["line"], request.get("state", {})), sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
