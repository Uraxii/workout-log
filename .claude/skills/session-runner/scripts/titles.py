"""What a `Sets` row is called in Notion.

Notion takes exactly one title column per data source and shows it as the
row's name everywhere: the table's first column, a search result, an
@-mention. `confirm_line` used to be that column, but it holds one line per
entry rather than one per row, so every row of `squat 225x5x3` except the
last landed unnamed (ticket workout-log-4sc). The confirm line's shape is
right for what it is; it was the wrong thing to name a row with.

So the title is derived here from what the row already carries, and derived
for the whole turn on the way out of the `log_set` seam, the same shape
`preconditions.no_sets_while_halted` and `bounds.reject_implausible_writes`
already use. A handler cannot forget to set it, because no handler sets it.
"""

from __future__ import annotations

from typing import Any

import catalog as catalog_lib
import rows as row_shapes

TITLE = "Set"
SET_TARGET = "Sets"
# A Sets row with no exercise, no set index, no note and no magnitudes. No
# handler emits one today; the title is still a name, never an empty string.
UNNAMED = "Set"


def title_for(payload: dict[str, Any], known: dict[str, str]) -> str:
    """`<exercise> set <n>, <magnitudes>`, dropping any part this row lacks.

    Row 2 of a multi-row entry says `set 2` and its own magnitudes, so it
    reads as the set it is rather than as a repeat of the entry. `Exercise`
    already holds the name, so a row's title and its confirm line cannot
    disagree about what the exercise is called. Its measure kind comes from
    what this athlete has logged, then from the shipped defaults.
    """
    note = payload.get("Notes")
    if note:
        return f"Note: {note}"
    name = payload.get("Exercise")
    measure = catalog_lib.measure_of(name, known) if name else None
    index = payload.get("Set index")
    head = " ".join(part for part in (name, f"set {index}" if index else None) if part)
    magnitudes = row_shapes.magnitudes_text(measure, payload) if measure else ""
    if head and magnitudes:
        return f"{head}, {magnitudes}"
    return head or magnitudes or UNNAMED


def name_every_set(turn: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    """Title every `Sets` row the turn writes. Wired into `log_set.log_set`.

    A `stale` payload is skipped: it is a merge that flips one checkbox on a
    row already written and already named, not a new row (`writer.py`
    upserts on `write_key`), and nothing in it says what that row held.
    """
    known = turn["state"].get("known", state.get("known", {}))
    for write in turn["writes"]:
        payload = write["payload"]
        if write["target"] != SET_TARGET or payload.get("stale"):
            continue
        payload[TITLE] = title_for(payload, known)
    return turn


def _self_check() -> None:
    """python3 titles.py"""
    known = {"Barbell Squat": "weight_reps", "Otago Sit to Stand": "level_reps"}
    row = {"Exercise": "Barbell Squat", "Set index": 2, "Load": 225,
           "Unit": "lb", "Reps": 5}
    assert title_for(row, known) == "Barbell Squat set 2, 225 lb x 5"
    assert title_for({**row, "Set index": 3}, known) == "Barbell Squat set 3, 225 lb x 5"
    assert title_for({"Exercise": "Otago Sit to Stand", "Set index": 1, "level": 3,
                      "Reps": 8}, known) == "Otago Sit to Stand set 1, 3 x 8"
    # A program prescribes a shipped default name this athlete has never
    # logged, so `known` cannot answer and the defaults file does
    # (fixture 04-today).
    assert title_for({"Exercise": "Barbell Squat", "Set index": 1, "Load": 225,
                      "Unit": "lb", "Reps": 5}, {}) == "Barbell Squat set 1, 225 lb x 5"
    # A name no table carries still titles its row, from the row's own shape.
    assert title_for({"Exercise": "zercher squat", "Set index": 1, "Load": 135,
                      "Unit": "lb", "Reps": 5}, {}) == "zercher squat set 1"
    # Every part can be missing, and none of them empties the title.
    assert title_for({"Exercise": "Barbell Squat", "Set index": 4}, known) == "Barbell Squat set 4"
    assert title_for({"Set index": 4}, known) == "set 4"
    assert title_for({"Notes": "185 felt heavy"}, known) == "Note: 185 felt heavy"
    assert title_for({}, known) == UNNAMED

    turn = {"writes": [{"verb": "row-create", "target": "Sets", "payload": dict(row)},
                       {"verb": "row-create", "target": "Sets",
                        "payload": {"write_key": "k", "stale": True}},
                       {"verb": "row-create", "target": "Sessions", "payload": {"Status": "closed"}}],
            "confirm_line": "x",
            "state": {"known": {"Barbell Squat": "weight_reps"}}}
    named = name_every_set(turn, {})
    assert named["writes"][0]["payload"][TITLE] == "Barbell Squat set 2, 225 lb x 5"
    assert TITLE not in named["writes"][1]["payload"]  # stale merge, row already named
    assert TITLE not in named["writes"][2]["payload"]  # not a Sets row
    print("titles.py self-check: ok")


if __name__ == "__main__":
    _self_check()
