"""Fixture transcript parsing: `@directive` setup lines plus user chat turns.

Split out of `replay.py` (house limit, docs/architecture.md "One script per
skill" applies the same way to the harness): parsing a transcript into a
`Fixture` is one body of knowledge, replaying it against the mock writer and
diffing the result is another.
"""

from __future__ import annotations

from typing import NamedTuple

DIRECTIVE_PREFIX = "@"


class Turn(NamedTuple):
    """One user chat line with the clock, message id and seam in force."""

    line: str
    now: str
    message_id: str
    skill: str
    resend: bool = False  # rule L9: replay against the ORIGINAL turn's pre-call state
    rest_node_label: str | None = None  # @rest_node: see parse_transcript
    cold: bool = False  # @cold: hydrate this turn's state from the store


class Fixture(NamedTuple):
    """A parsed transcript: setup directives plus the ordered user turns."""

    timezone: str
    units: str
    catalog: list[dict[str, str]]
    turns: list[Turn]
    intake_cursor: str | None


def parse_transcript(text: str) -> Fixture:
    """Split `@directive` setup lines from user chat lines.

    Directives, tab separated: `@tz <iana>`, `@units lb|kg`,
    `@exercise <Name> <measure>`, `@now <iso8601>`, which may repeat
    mid-transcript so a fixture can cross midnight (rule L4); `@skill <name>`,
    which routes every following turn to that seam until it repeats (phase 5:
    `intake`, `screen`; default `session-runner`); `@intake_cursor <n>`,
    seeding a resumed intake's cursor (lim L-48); and `@resend`, repeating
    the previous turn verbatim against that turn's own pre-call state (rule
    L9: a resend, not a second message). Blank and `#` lines drop out;
    every other line is one user turn, `source_message_id` `msg-<n>` (L9).
    `@rest_node <label>` stands in for a template that ships a rest node
    (docs/program-format.md's own mini example is the shape:
    `{"id": "REST", "label": <label>, "blocks": []}`, no seam has a verb to
    author one at runtime): it tags the next turn, and `replay()` appends
    that node to `state["program"]["rotation"]` before calling it, phase 4's
    proof for rule L17's program-cursor rest-day advance (build-plan s9).
    `@cold` says the chat ended and in-memory state is gone: it tags the
    next turn the same pending-flag way, and `replay()` rebuilds that
    turn's state from the store's read verbs alone (`hydrate.py`).
    """
    timezone = ""
    units = ""
    catalog: list[dict[str, str]] = []
    turns: list[Turn] = []
    now = ""
    msg_n = 0
    current_skill = "session-runner"
    intake_cursor = None
    pending_rest_node = None
    pending_cold = False

    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        if line.startswith(DIRECTIVE_PREFIX):
            parts = line.split("\t")
            directive = parts[0]
            if directive == "@tz":
                timezone = parts[1]
            elif directive == "@units":
                units = parts[1]
            elif directive == "@now":
                now = parts[1]
            elif directive == "@exercise":
                catalog.append({"name": parts[1], "measure": parts[2]})
            elif directive == "@skill":
                current_skill = parts[1]
            elif directive == "@intake_cursor":
                intake_cursor = parts[1]
            elif directive == "@rest_node":
                pending_rest_node = parts[1]
            elif directive == "@cold":
                pending_cold = True
            elif directive == "@resend":
                last = turns[-1]
                turns.append(Turn(line=last.line, now=last.now, message_id=last.message_id,
                                  skill=last.skill, resend=True))
            else:
                raise ValueError(f"unknown directive {directive!r}")
            continue
        msg_n += 1
        turns.append(Turn(line=line, now=now, message_id=f"msg-{msg_n}", skill=current_skill,
                          rest_node_label=pending_rest_node, cold=pending_cold))
        pending_rest_node = None
        pending_cold = False

    return Fixture(timezone=timezone, units=units, catalog=catalog, turns=turns, intake_cursor=intake_cursor)
