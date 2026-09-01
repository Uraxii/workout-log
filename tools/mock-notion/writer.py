"""Offline stand-in for the Notion MCP write verbs (build-plan s6, s9).

Accepts the two write verbs any skill may use for data (`row_create`,
`config_write`), plus `database_create`, `intake`'s one-time schema-creation
call (build-plan s5.1). Every payload validates against
schema/notion-schema.json, and each verb appends one TSV line per emitted
field so a fixture can be compared byte for byte. All three are
query-before-create (rule L8): a payload whose identity key already exists
is an upsert, not an ignored duplicate (phase 3 defect 1) — it merges into
the existing row and appends only the fields that changed value, so a
resend with identical content still appends nothing.

`Sessions` has no payload-derivable identity in the schema (`identity:
["page_id"]`): a real page id does not exist until after the row is
created, and the one caller that updates a session's `Status` after open
(`pain-triage`) sends a bare `{"Status": ...}` with no identity field at
all. Phase 3 defect 1 settles this without a schema change (out of this
phase's scope): a write carrying the frozen open fields (`Date`,
`Timezone`, `Start time`, rules L3, L4) keys on that tuple; any other
`Sessions` write targets whichever session is currently open. See
`_resolve_session`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

TSV_HEADER = ("verb", "target", "field", "value")
DEFAULT_SCHEMA = Path(__file__).resolve().parents[2] / "schema" / "notion-schema.json"
_SESSION_OPEN_FIELDS = ("Date", "Timezone", "Start time")  # rules L3, L4: frozen at open


class SchemaViolation(ValueError):
    """Payload names a database, property, or enum value the schema lacks."""


class MockNotion:
    """One TSV per replay run. Not concurrency safe; one runner owns one file."""

    def __init__(self, out_path: Path, schema_path: Path = DEFAULT_SCHEMA) -> None:
        self.out_path = out_path
        self.schema: dict[str, Any] = json.loads(schema_path.read_text())
        self.rows: dict[str, dict[str, dict[str, Any]]] = {}
        self.config: dict[str, dict[str, str]] = {}
        self._next_n: dict[str, int] = {}
        self._by_key: dict[tuple, str] = {}
        self._databases: dict[tuple[str, str], str] = {}
        self._session_by_open: dict[tuple, str] = {}
        self._open_session: str | None = None
        self._header_written = False
        self.out_path.write_text("")

    def database_create(self, db: str, parent: str) -> str:
        """Create one Notion database under `parent`, or adopt the one
        already created there (build-plan s5.1, rule L8: same
        query-before-create discipline as `row_create`). A second call for
        the same `(db, parent)`, i.e. a second "set me up", appends nothing
        and returns the existing id.
        """
        if db not in self.schema["databases"]:
            raise SchemaViolation(f"unknown database {db!r}")
        key = (db, parent)
        existing = self._databases.get(key)
        if existing is not None:
            return existing
        db_id = f"db-{db}"
        self._databases[key] = db_id
        self.emit("database-create", db, {"Parent": parent})
        return db_id

    def row_create(self, db: str, payload: dict[str, Any]) -> str:
        """Create one row, or upsert into the row already holding its
        identity key (`Sessions`: see `_resolve_session`).

        Returns the page id, `<db lowercased>-<n>` in creation order. Appends
        one TSV line per field whose value changed, in schema declaration
        order. A payload matching an existing identity with no changed
        fields (a resend, rule L9) appends nothing.
        """
        return self._create(db, payload, record=True)

    def config_write(self, page: str, key: str, value: str) -> None:
        """Set one key on one config page body. Rewriting the same value is a
        no-op and appends nothing.

        Defect 4: `program/current` and `program/history/<date>` name their
        allowed fields `headers`, not `keys` (schema is frozen this phase,
        not a typo to fix there). Both lists mean the same thing here, the
        allowed field names on that page body; a table-shaped program page
        and a key-value config page differ in presentation, not in what
        `config_write` needs to validate, so one check covers both rather
        than adding a second code path per page shape."""
        pages = self.schema["config_pages"]
        if page not in pages:
            raise SchemaViolation(f"unknown config page {page!r}")
        spec = pages[page]
        allowed = spec.get("keys", spec.get("headers", []))
        if key not in allowed:
            raise SchemaViolation(f"{page}.{key} not in schema")
        enum = spec.get("enums", {}).get(key)
        if enum is not None and value not in enum:
            raise SchemaViolation(f"{page}.{key}={value!r} not in {enum}")
        if self.config.get(page, {}).get(key) == value:
            return
        self.config.setdefault(page, {})[key] = value
        self.emit("config-write", page, {key: value})

    def seed_row(self, db: str, payload: dict[str, Any]) -> str:
        """Insert a row without emitting TSV, for fixture `@` preamble rows."""
        return self._create(db, payload, record=False)

    def _create(self, db: str, payload: dict[str, Any], record: bool) -> str:
        self._validate(db, payload)
        schema_db = self.schema["databases"][db]
        if db == "Sessions":
            page_id, is_new = self._resolve_session(payload)
        else:
            existing = self._find(db, schema_db, payload)
            page_id, is_new = (existing, False) if existing is not None else (self._new_id(db), True)
        if is_new:
            self.rows.setdefault(db, {})[page_id] = {}
            self._index(db, schema_db, payload, page_id)
        changed = self._merge(db, page_id, schema_db, payload)
        if record and changed:
            self.emit("row-create", db, changed)
        return page_id

    def _new_id(self, db: str) -> str:
        n = self._next_n.get(db, 0) + 1
        self._next_n[db] = n
        return f"{db.lower()}-{n}"

    def _resolve_session(self, payload: dict[str, Any]) -> tuple[str, bool]:
        """Defect 1's identity: a full open write (`Date`, `Timezone`,
        `Start time` all present) keys on that tuple, so a genuine resend of
        the open write adopts the same row. Any other write (a `Status`
        change with no open fields, e.g. `pain-triage`'s halt) targets
        whichever session is currently open; there is exactly one at a time
        in this model (rule L16)."""
        if all(payload.get(k) is not None for k in _SESSION_OPEN_FIELDS):
            key = tuple(payload[k] for k in _SESSION_OPEN_FIELDS)
            existing = self._session_by_open.get(key)
            page_id = existing if existing is not None else self._new_id("Sessions")
            self._session_by_open[key] = page_id
            self._open_session = page_id
            return page_id, existing is None
        if self._open_session is None:
            raise SchemaViolation("Sessions write with no open session to merge into")
        return self._open_session, False

    def _merge(self, db: str, page_id: str, schema_db: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        """Update the stored row in schema property order, returning only
        the fields whose value changed (defect 1's upsert semantics)."""
        stored = self.rows[db][page_id]
        changed = {}
        for name in schema_db["properties"]:
            if name not in payload:
                continue
            value = payload[name]
            if stored.get(name) != value:
                stored[name] = value
                if value is not None and value is not False:
                    changed[name] = value
        return changed

    def _find(self, db: str, schema_db: dict[str, Any], payload: dict[str, Any]) -> str | None:
        keys = schema_db.get("identity", [])
        if keys and all(payload.get(k) is not None for k in keys):
            return self._by_key.get((db, tuple(payload[k] for k in keys)))
        return None

    def _index(self, db: str, schema_db: dict[str, Any], payload: dict[str, Any], page_id: str) -> None:
        keys = schema_db.get("identity", [])
        if keys and all(payload.get(k) is not None for k in keys):
            self._by_key[(db, tuple(payload[k] for k in keys))] = page_id

    def _validate(self, db: str, payload: dict[str, Any]) -> None:
        """Raise SchemaViolation on an unknown db, property, or enum value."""
        databases = self.schema["databases"]
        if db not in databases:
            raise SchemaViolation(f"unknown database {db!r}")
        props = databases[db]["properties"]
        for name, value in payload.items():
            if name not in props:
                raise SchemaViolation(f"{db}.{name} not in schema")
            enum = props[name].get("enum")
            if enum is not None and value is not None and value not in enum:
                raise SchemaViolation(f"{db}.{name}={value!r} not in {enum}")

    def emit(self, verb: str, target: str, fields: dict[str, Any]) -> None:
        """Append TSV lines. Writes TSV_HEADER first if the file is new."""
        with self.out_path.open("a") as f:
            if not self._header_written:
                f.write("\t".join(TSV_HEADER) + "\n")
                self._header_written = True
            for field, value in fields.items():
                f.write(f"{verb}\t{target}\t{field}\t{value}\n")
