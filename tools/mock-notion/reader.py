"""Offline stand-in for the Notion MCP read verbs, over `writer.MockNotion`.

Reads live beside writes, never inside them (docs/architecture.md "One
script per skill" applies the same way to the harness: `writer.py` owns
what a payload may say, this owns what a caller may ask).

Both verbs append one TSV line per read CALL, not per returned field. A
read's payload is already asserted byte for byte by the `row-create` /
`config-write` rows that produced it and by the `say` row the caller
derives from it, so re-emitting it doubles the file for no new information.
The call plus its result count proves the read happened, in what order, and
proves the empty case:

    config-read     <page>  *       <number of keys returned>
    row-query       <db>    <filter>        <number of rows returned>
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import writer
from payload_rules import SchemaViolation, check_fields, properties_of

NO_FILTER = "*"  # `<field>` on a config read, `<filter>` on an unfiltered query


class MockNotionReader:
    """The two read verbs against one store's rows and config bodies."""

    def __init__(self, store: writer.MockNotion) -> None:
        self.store = store

    def config_read(self, page: str) -> dict[str, str]:
        """One config page body, copied, or `{}` when nothing wrote it yet.

        A cold start reads pages that do not exist: that is the ordinary
        turn-1 case, not an error, so it is never `None` and never raises.
        A page the schema does not declare is a programmer bug and stays
        loud.
        """
        if page not in self.store.schema["config_pages"]:
            raise SchemaViolation(f"unknown config page {page!r}")
        body = dict(self.store.config.get(page, {}))
        self.store.emit("config-read", page, {NO_FILTER: len(body)})
        return body

    def row_query(self, db: str, where: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Rows matching every key in `where` exactly, in creation order.

        Exact match only: every turn-1 hydration read is exact match, so
        ranges, ordering and limits stay unbuilt until something needs one.
        Each row is a copy of the stored fields plus `page_id`, which the
        caller cannot do without: `Sessions` declares `identity:
        ["page_id"]`, and a rebuilt catalog is keyed by it.

        Values come back raw, unconverted.
        `.claude/skills/load-adjust/scripts/read_layer.py` already owns
        e1RM, unit conversion and ranking, so one place converts and the
        store stays dumb.
        """
        properties_of(self.store.schema, db)
        criteria = where or {}
        # An unmatched enum VALUE is an empty result, not a violation.
        check_fields(self.store.schema, db, criteria, check_enums=False)
        found = [
            {**row, "page_id": page_id}
            for page_id, row in self.store.rows.get(db, {}).items()
            if all(row.get(key) == value for key, value in criteria.items())
        ]
        self.store.emit("row-query", db, {filter_text(criteria): len(found)})
        return found


def filter_text(where: dict[str, Any]) -> str:
    """`k=v` pairs joined by `,` in sorted key order, `*` when unfiltered."""
    if not where:
        return NO_FILTER
    return ",".join(f"{key}={where[key]}" for key in sorted(where))


def _self_check() -> None:
    """The branches no fixture reaches: the three refusals, and the cold
    read of a schema page nothing has written.

        python3 tools/mock-notion/reader.py
    """
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        store = writer.MockNotion(Path(tmp) / "out.tsv")
        reader = MockNotionReader(store)

        assert reader.config_read("config/limits") == {}, "cold page must be {}"
        store.config_write("config/limits", "clearance", "cleared")
        assert reader.config_read("config/limits") == {"clearance": "cleared"}
        body = reader.config_read("config/limits")
        body["clearance"] = "tampered"
        assert store.config["config/limits"]["clearance"] == "cleared", "must copy"

        assert reader.row_query("Sessions") == []
        first = store.row_create("Sessions", {"Date": "2026-09-01", "Timezone": "UTC",
                                              "Start time": "2026-09-01T18:00:00+00:00",
                                              "Status": "open"})
        store.row_create("Sessions", {"Date": "2026-09-02", "Timezone": "UTC",
                                      "Start time": "2026-09-02T18:00:00+00:00",
                                      "Status": "closed"})
        every = reader.row_query("Sessions")
        assert [row["Date"] for row in every] == ["2026-09-01", "2026-09-02"], "creation order"
        assert every[0]["page_id"] == first, "page_id is required"
        assert len(reader.row_query("Sessions", {"Status": "open"})) == 1
        assert reader.row_query("Sessions", {"Status": "halted"}) == []

        for call in (lambda: reader.config_read("config/nope"),
                     lambda: reader.row_query("Nope"),
                     lambda: reader.row_query("Sessions", {"Nope": 1})):
            try:
                call()
            except SchemaViolation:
                continue
            raise AssertionError("a name the schema lacks must raise")

        assert filter_text({}) == NO_FILTER
        assert filter_text({"b": 2, "a": 1}) == "a=1,b=2", "sorted key order"
    print("reader.py self-check: ok")


if __name__ == "__main__":
    _self_check()
