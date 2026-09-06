"""Turn `schema/notion-schema.json` into a folder of markdown notes.

The twin of `ddl.py`, and the second entry in `storage.PROFILES`. Both
modules answer the same seven names, so `storage.next_create_write` picks
one and the rest of `intake` never learns which store it is writing to.

The vault's conventions live in `references/vault-layout.md`, the twin of
`references/db-create.md`: the directory layout, the front matter, the
table encoding, and which columns a note carries. The model reads that
document and performs the writes. This module only names the folder and
the ordered column list, which is everything a payload can say without
opening a file.

No filesystem, by type. A vault root arrives as `str` and leaves as `str`,
never as `pathlib.Path`. A module that never imports `pathlib` cannot open
a file by accident, and that guard is the reason every skill seam is still
a pure function of `(line, state)` that runs in a sandbox with no disk and
no network. A path is also never rewritten here: `~` stays `~` and a
relative segment stays where it was typed, because the model performs the
write and a normalised path is a value the athlete never gave.

ponytail: writing works, reading does not. Within one chat `state` never
goes cold, so a first "set me up" and every set logged after it land in the
vault. A second chat cannot rebuild `state`, because nothing parses a
session note back yet: `tools/mock-notion/hydrate.py` has a Notion reader
and no vault one. The upgrade path is one shell pass over `sessions/*.md`
per read verb, behind the same `MockNotionReader` interface, and it is the
next task rather than this one.
"""

from __future__ import annotations

from typing import Any

import readers

ID = "obsidian"
ROOT_KEY = "storage_root"
LAYOUT_REF = "references/vault-layout.md"

ROOT_PROMPT = "First, where should I put your logs? Give me the full path to a folder in your vault, like /home/you/vault/training."
ROOT_REASK = "That isn't a path I can use. Paste the full path to a folder in your vault, starting with / or ~."

root_parse = readers.vault_path

# One markdown note per session, with its sets as the rows of one table in
# that note. `Sets` and `Sessions` both resolve to this one folder, which is
# the honest answer to "where do Sets rows live": inside the session note
# (`references/vault-layout.md`).
NOTE_FOLDER = "sessions"

# The properties a note never carries, keyed by database so a third
# database is a row here and not a new branch. Each one is recoverable from
# what the note already shows, and a stored copy would be a second source of
# truth that a hand edit could put out of step: `Session` is the note the
# row sits in, `Set` restates the row, `write_key` joins the note's frozen
# `Start time` and `Timezone` with the row's `Exercise`, `Set index` and
# `attempt`, and `e1RM` is a Notion formula a markdown table cannot compute
# (`references/vault-layout.md`).
NOT_STORED: dict[str, frozenset[str]] = {
    "Sets": frozenset({"Session", "Set", "write_key", "e1RM"}),
    "Sessions": frozenset(),
}


def folder(root: str) -> str:
    """The one folder every session note goes in, under the vault root."""
    return f"{root.rstrip('/')}/{NOTE_FOLDER}"


def columns(db: str, schema: dict[str, Any]) -> list[str]:
    """The table columns one database contributes, in schema order."""
    properties = schema["databases"][db]["properties"]
    skipped = NOT_STORED.get(db, frozenset())
    return [name for name in properties if name not in skipped]


def create_payload(db: str, root: str,
                   schema: dict[str, Any]) -> dict[str, Any]:
    """The `database-create` arguments for one database against a vault.

    The caller hands the schema over, because this module reads no file:
    `storage.next_create_write` has already loaded it to walk the database
    list, so passing it costs nothing and keeps the vault profile pure.
    """
    return {
        "parent": {"type": "vault_path", "path": root},
        "title": db,
        "schema": {"folder": folder(root), "columns": columns(db, schema)},
    }
