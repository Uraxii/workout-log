"""Offline stand-in for the Notion MCP write verbs (build-plan s6, s9).

Two write verbs any skill may use for data (`row_create`, `config_write`),
plus `database_create`, `intake`'s one-time schema-creation call (build-plan
s5.1). Every payload validates against schema/notion-schema.json and appends
one TSV line per emitted field.

All three are query-before-create (rule L8). A payload whose identity key
already exists is an upsert, not an ignored duplicate (phase 3 defect 1): it
merges into the existing row and appends only the fields whose value changed,
so a resend of identical content appends nothing. `Sessions` has no
payload-derivable identity in the schema; `_resolve_session` is what stands
in for one.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import notion_ddl
from payload_rules import (SchemaViolation, check_config_key, check_fields,
                           properties_of)

__all__ = ["MockNotion", "SchemaViolation", "TSV_HEADER"]

TSV_HEADER = ("verb", "target", "field", "value")
DEFAULT_SCHEMA = Path(__file__).resolve().parents[2] / "schema" / "notion-schema.json"
_SESSION_OPEN_FIELDS = ("Date", "Timezone", "Start time")  # rules L3, L4: frozen at open


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

    def database_create(self, db: str, payload: dict[str, Any]) -> str:
        """Create one Notion database, or adopt the one already created under
        the same parent page (build-plan s5.1, rule L8: same
        query-before-create discipline as `row_create`). A second call for
        the same `(db, parent page)`, i.e. a second "set me up", appends
        nothing and returns the existing data source id.

        `payload` is the `notion-create-database` call verbatim, checked by
        `notion_ddl`. The returned id is a data source id: relation columns
        in later calls must name it, which is what orders the creates.
        """
        properties_of(self.schema, db)
        notion_ddl.validate_create(payload, set(self._databases.values()))
        key = (db, payload["parent"]["page_id"])
        existing = self._databases.get(key)
        if existing is not None:
            return existing
        db_id = f"ds-{db}"
        self._databases[key] = db_id
        self.emit("database-create", db, {
            "Parent": payload["parent"]["page_id"],
            "Schema": payload["schema"],
        })
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
        no-op and appends nothing."""
        if self._set_config(page, key, value):
            self.emit("config-write", page, {key: value})

    def _set_config(self, page: str, key: str, value: str) -> bool:
        """Validate and store one config key, False when unchanged."""
        check_config_key(self.schema, page, key, value)
        if self.config.get(page, {}).get(key) == value:
            return False
        self.config.setdefault(page, {})[key] = value
        return True

    def seed_row(self, db: str, payload: dict[str, Any]) -> str:
        """Insert a row without emitting TSV, for fixture `@` preamble rows."""
        return self._create(db, payload, record=False)

    def seed_config(self, page: str, key: str, value: str) -> None:
        """`seed_row` for config pages: set one key, emit no TSV."""
        self._set_config(page, key, value)

    def _create(self, db: str, payload: dict[str, Any], record: bool) -> str:
        check_fields(self.schema, db, payload, check_enums=True)
        schema_db = self.schema["databases"][db]
        key = None
        if db == "Sessions":
            page_id, is_new = self._resolve_session(payload)
        else:
            key = self._identity(db, schema_db, payload)
            existing = self._by_key.get(key) if key else None
            page_id, is_new = (existing, False) if existing is not None else (self._new_id(db), True)
        if is_new:
            self.rows.setdefault(db, {})[page_id] = {}
            if key:
                self._by_key[key] = page_id
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

    def _identity(self, db: str, schema_db: dict[str, Any],
                  payload: dict[str, Any]) -> tuple | None:
        """This payload's `_by_key` key, `None` when it carries no value for
        every declared identity property."""
        keys = schema_db.get("identity", [])
        if not keys or any(payload.get(k) is None for k in keys):
            return None
        return (db, tuple(payload[k] for k in keys))

    def emit(self, verb: str, target: str, fields: dict[str, Any]) -> None:
        """Append TSV lines. Writes TSV_HEADER first if the file is new."""
        with self.out_path.open("a") as f:
            if not self._header_written:
                f.write("\t".join(TSV_HEADER) + "\n")
                self._header_written = True
            for field, value in fields.items():
                f.write(f"{verb}\t{target}\t{field}\t{value}\n")
