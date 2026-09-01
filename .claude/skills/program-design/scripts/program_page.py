"""The `program/current` page body: one module owns both halves of the round
trip.

`program-design` writes this page and `hydrate` reads it back on turn 1, so
the key names live here rather than in each caller (workout-log-xo0: the
rotation used to survive only in memory, because the page stored five header
strings and nothing else, and `session-runner` then read a `rotation` key
nobody had ever written).

A Notion config page is key/value text, so the template body rides as one
JSON string under `body`. `json.dumps` escapes tabs and newlines, so the
value stays a single TSV cell. The five header keys stay beside it, plain,
because the user hand-reads this page (build-plan s1.8).
"""

from __future__ import annotations

import json
from typing import Any, NamedTuple

FORMAT_VERSION = 1  # `docs/program-format.md` "Top level"
HEADER_KEYS = ("name", "origin", "progression_unit", "dose", "days")


class ProgramPage(NamedTuple):
    """What a cold read of `program/current` yields when it yields anything."""
    program: dict[str, Any]
    template_id: str
    started_at: str


def page_body(program: dict[str, Any], template_id: str, started_at: str) -> dict[str, Any]:
    """The full payload of one `config-write` to `program/current`.

    `started_at` is what makes the rotation cursor per-program: the sessions
    that count toward it are the ones closed since this program was picked
    (workout-log-ayf.15), so a second program starts its rotation at day one
    instead of wherever the first left off."""
    body = {key: program[key] for key in HEADER_KEYS}
    body["template_id"] = template_id
    body["started_at"] = started_at
    body["body"] = json.dumps(program, separators=(",", ":"))
    return body


def read_page(page: dict[str, str]) -> ProgramPage | None:
    """`None` when there is no usable active program, which covers four cases
    a caller must not tell apart: nothing written yet, a body that is not
    JSON, a body from a `format_version` this code does not speak, and a body
    missing the `rotation` the cursor indexes.

    All four recover the same way, by picking a program again, so none of
    them earns a migration path or a repair attempt (one user, zero
    installs). What a caller must never get is a half-built program, which is
    why this returns nothing rather than a partial."""
    raw = page.get("body")
    if not raw:
        return None
    try:
        program = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(program, dict) or program.get("format_version") != FORMAT_VERSION:
        return None
    if not isinstance(program.get("rotation"), list) or not program["rotation"]:
        return None
    if not program.get("name"):
        return None
    return ProgramPage(program, page.get("template_id", ""), page.get("started_at", ""))


def _self_check() -> None:
    """python3 program_page.py"""
    program = {"format_version": 1, "name": "T", "origin": "o",
               "progression_unit": "session", "dose": "sets", "days": 3,
               "rotation": [{"id": "A", "label": "A", "blocks": []}]}
    body = page_body(program, "t", "2026-09-01T09:00:00+00:00")
    assert set(body) == set(HEADER_KEYS) | {"template_id", "started_at", "body"}
    assert "\t" not in body["body"] and "\n" not in body["body"]
    page = read_page(body)
    assert page is not None and page.program == program
    assert page.template_id == "t" and page.started_at.startswith("2026-09-01")
    assert read_page({}) is None, "cold page"
    assert read_page({"body": "{not json"}) is None, "malformed body"
    assert read_page({"body": json.dumps({**program, "format_version": 99})}) is None
    assert read_page({"body": json.dumps({**program, "rotation": []})}) is None
    assert read_page({"body": json.dumps({**program, "name": ""})}) is None
    assert read_page({"body": "[]"}) is None, "not an object"
    print("program_page.py self-check: ok")


if __name__ == "__main__":
    _self_check()
