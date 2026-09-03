"""The natural-key replacement for the sha256 `write_key`.

Today `write_key = sha256("<session_key>|<exercise_id>|<set_index>|
<attempt>")[:16]` and `session_key = sha256("<start>|<tz>")[:16]`
(docs/architecture.md, rule L8). A language model cannot compute sha256
by hand, so on a host with no script execution the key must be a string
the model can build by concatenation from fields the row already carries.

The separator is `SEPARATOR`, a pipe and not a slash: rule L3 freezes
`Timezone` to the device IANA zone, and `America/New_York` carries a
slash, so a slash-separated key would not split back into five
components. No component may contain a pipe. The exercise component is
the catalog slug, never the display Name, so a rename does not change
the key.
"""

from __future__ import annotations

SEPARATOR: str = "|"


def session_key(start_time_local: str, timezone: str) -> str:
    """The frozen open instant plus the frozen zone (rules L3, L4)."""
    ...  # TODO


def write_key(session: str, exercise_slug: str, set_index: int,
               attempt: int) -> str:
    """Joins the four components with `SEPARATOR`. The result is readable
    in the Notion UI on purpose, so a malformed key is visible instead of
    opaque."""
    ...  # TODO


def parse_write_key(key: str) -> tuple[str, str, str, int, int]:
    """Returns (start_time_local, timezone, exercise_slug, set_index,
    attempt). Exists so a key can be checked against the row that carries
    it; raises ValueError on a key that does not split into five
    components."""
    ...  # TODO


def matches_row(key: str, row: dict[str, object]) -> bool:
    """True when every component of `key` agrees with the corresponding
    property on `row`. This is the guard that catches the one silent
    failure mode the natural key introduces, a model that composes a key
    that does not describe its own row."""
    ...  # TODO
