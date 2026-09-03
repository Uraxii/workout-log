"""What the repo's own schema permits a payload or a filter to name.

`notion_ddl` and friends own Notion's rules for a `CREATE TABLE` call. This
owns the other kind: whether `schema/notion-schema.json` declares the
database, the property and the enum value a caller just used. `writer.py`
checks a write payload with it and `reader.py` checks a query filter, so the
two cannot drift about what "not in schema" means.
"""

from __future__ import annotations

from typing import Any


class SchemaViolation(ValueError):
    """Payload names a database, property, or enum value the schema lacks."""


def properties_of(schema: dict[str, Any], db: str) -> dict[str, Any]:
    """The declared properties of one database, raising on an unknown name."""
    databases = schema["databases"]
    if db not in databases:
        raise SchemaViolation(f"unknown database {db!r}")
    return databases[db]["properties"]


def check_fields(schema: dict[str, Any], db: str, fields: dict[str, Any],
                 check_enums: bool) -> None:
    """Every key in `fields` is a declared property of `db`.

    `check_enums` is on for a write, where the value is being stored, and off
    for a query filter, where an unmatched value is a legitimate empty result
    rather than a violation.
    """
    properties = properties_of(schema, db)
    for name, value in fields.items():
        if name not in properties:
            raise SchemaViolation(f"{db}.{name} not in schema")
        enum = properties[name].get("enum") if check_enums else None
        if enum is not None and value is not None and value not in enum:
            raise SchemaViolation(f"{db}.{name}={value!r} not in {enum}")


def check_config_key(schema: dict[str, Any], page: str, key: str,
                     value: str) -> None:
    """One config page key and its value.

    Defect 4: `program/current` and `program/history/<date>` name their
    allowed fields `headers`, not `keys`. Both mean the same thing here, so
    one check covers both rather than a code path per page shape.
    """
    pages = schema["config_pages"]
    if page not in pages:
        raise SchemaViolation(f"unknown config page {page!r}")
    spec = pages[page]
    if key not in spec.get("keys", spec.get("headers", [])):
        raise SchemaViolation(f"{page}.{key} not in schema")
    enum = spec.get("enums", {}).get(key)
    if enum is not None and value not in enum:
        raise SchemaViolation(f"{page}.{key}={value!r} not in {enum}")
