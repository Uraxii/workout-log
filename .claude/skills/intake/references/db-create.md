# Database creation payload

`intake` never hand-copies `schema/notion-schema.json`. It reads the schema at
call time and maps each declared property type to a Notion API property
type, so the create payload is generated, not authored twice (build-plan s5.1,
s2 rule L8).

## The renderer owns the payload

`scripts/ddl.py` reads `schema/notion-schema.json` and renders the call. There
is no type-mapping table here and no payload skeleton to copy, because a
payload hand-built from prose drifts from the schema: tickets
workout-log-29l, -3lw, -6zr and -8ms were four symptoms of that one cause.

	from ddl import create_order, create_payload
	create_payload(db, parent_page_id, data_source_ids)

- `create_order()` returns the database names in relation-graph order, so a
  relation column always names a data source that an earlier call returned.
  It is derived from the schema; adding a relation reorders the creates with
  no code change.
- `create_payload()` returns the `notion-create-database` arguments: `parent`
  (`{"type": "page_id", "page_id": ...}`), `title`, and `schema`, a SQL DDL
  `CREATE TABLE` statement. `COLUMN_DDL` in that module is the type table.
- `data_source_ids` maps an already-created database name to the id its call
  returned. **One create per turn**: the tool answers with the new data
  source id, and the next database needs it.

The rules the output must satisfy are in
`research/19-notion-database-create-api.md`, each with a primary
`developers.notion.com` URL, and are enforced offline by
`tools/mock-notion/notion_ddl.py`.

Query-before-create (rule L8): before calling `notion-create-database`,
`intake` searches the parent page for a database already named `Sets` (or
`Sessions`, `Exercises`, `Locations`); if found, it adopts that id and issues
no create call. The offline mock (`tools/mock-notion/writer.py`
`database_create`) reproduces this by keying on `(db name, parent)` and
appending nothing to the TSV on the second call.

## Catalog seeding, after the four databases exist

`Exercises` is seeded from `exercises/catalog.json` (913 rows: free-exercise-db
plus `exercises/extra.json` plus the alias table). Each row is one
`row_create("Exercises", ...)` call. Notion Free is rate-limited to roughly 3
requests per second, so 913 rows is a one-time step of **roughly 5 minutes**;
`intake` tells the user this before starting and does not block the rest of
the conversation on it finishing. The offline proof does not replay all 913
rows (they are mechanical, one per catalog entry, and add nothing the fixture
format needs to assert); it asserts the four `database-create` calls only.
