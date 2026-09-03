# Database creation payload

`intake` never hand-copies `schema/notion-schema.json`. It reads the schema at
call time and maps each declared property type to a SQL DDL column keyword,
because the hosted `notion-create-database` MCP tool takes DDL, not the REST
property object (`research/19-notion-database-create-api.md`). The call is
generated, not authored twice (build-plan s5.1, s2 rule L8).

## The renderer owns the payload

`scripts/ddl.py` reads `schema/notion-schema.json` and renders the call. There
is no type-mapping table here and no payload skeleton to copy, because a
payload hand-built from prose drifts from the schema: tickets
workout-log-29l, -3lw, -6zr and -8ms were four symptoms of that one cause.

	from ddl import create_payload, load_schema
	create_payload(db, parent_page_id)

- `load_schema()["databases"]` is the create order, which is schema
  declaration order: `Sets`, then `Sessions`. There is nothing to sort,
  because no column is a relation. Notion holds logs only, so every value is
  a string, number, date, select or checkbox and no database points at
  another.
- `create_payload()` returns the `notion-create-database` arguments: `parent`
  (`{"type": "page_id", "page_id": ...}`), `title`, and `schema`, a SQL DDL
  `CREATE TABLE` statement. `COLUMN_DDL` in that module is the type table.
- **One create per turn** still, so the returned data source id lands in
  `state["databases"]` and a rerun adopts rather than duplicates.

The rules the output must satisfy are in
`research/19-notion-database-create-api.md`, each with a primary
`developers.notion.com` URL, and are enforced offline by
`tools/mock-notion/notion_ddl.py`.

Query-before-create (rule L8): before calling `notion-create-database`,
`intake` searches the parent page for a database already named `Sets` or
`Sessions`; if found, it adopts that id and issues no create call. The offline
mock (`tools/mock-notion/writer.py` `database_create`) reproduces this by
keying on `(db name, parent)` and appending nothing to the TSV on the second
call.

## Nothing is seeded

There is no seeding step and no rate-limit wait. The exercise list lives in
the package at `exercises/defaults.json` (92 names) with its aliases beside it
at `exercises/aliases.json` (125), and the agent reads both when it builds a
program. Neither is ever written to the athlete's workspace: a catalog is not
a log. A lift the defaults do not carry is logged under the name she typed.

`fixtures/05-first-run` asserts the whole install, and its only
`database-create` calls are `Sets` and `Sessions`.
