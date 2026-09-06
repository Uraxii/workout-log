# Vault layout

`intake` never hand-copies `schema/notion-schema.json`. It reads the schema at
call time, and `scripts/vault.py` renders the `database-create` payload from
it, the same way `scripts/ddl.py` does for Notion
(`references/db-create.md`). That payload names a folder and an ordered column
list, and stops there. Everything else a folder of markdown notes needs is in
this document, because no code renders it: the model reads this and performs
the file writes.

## The directory layout

	<storage_root>/
	  config/athlete.md
	  config/preferences.md
	  config/limits.md
	  program/current.md
	  program/history/2026-09-01.md
	  agent/progression-state.md
	  sessions/2026-09-01.md
	  sessions/2026-09-03.md

`<storage_root>` is the path the athlete gave, exactly as she typed it
(`readers.vault_path`). It is a vault root or a folder inside a vault, and
nothing in the store cares which. There is no configurable subfolder name.

`vault.create_payload(db, root, schema)` returns `parent`
(`{"type": "vault_path", "path": <storage_root>}`), `title`, and `schema`, a
`folder` and a `columns` list. Both `Sets` and `Sessions` resolve to the same
`sessions/` folder, because a `Sets` row lives inside the session note it
belongs to, keyed by that note. Containment is the join Notion writes as
`Sets.Session`.

## A session note

One markdown note per session. The session's own fields are YAML front matter.
Its sets are the rows of one markdown table in the body.

	---
	Date: 2026-09-01
	Timezone: UTC
	Status: closed
	Start time: 2026-09-01T18:00:00+00:00
	End time: 2026-09-01T18:45:00+00:00
	week_index: 36
	Readiness: 4
	---

	| Exercise | Set index | Timestamp | Load | Unit | load_kind | Reps | source_message_id | confirm_line |
	|---|---|---|---|---|---|---|---|---|
	| Barbell Squat | 1 | 2026-09-01T18:00:00+00:00 | 225 | lb | absolute | 5 | msg-3 | |
	| Barbell Squat | 2 | 2026-09-01T18:00:00+00:00 | 225 | lb | absolute | 5 | msg-3 | |
	| Barbell Squat | 3 | 2026-09-01T18:00:00+00:00 | 225 | lb | absolute | 5 | msg-3 | Barbell Squat set 1-3, 225 lb x 5. Set 4 at 225 lb. |

A value that contains `|` is written `\|`, so the pipe does not end the cell.

The file name carries the date, which is safe because `Date` is frozen at open
(rule L4, `Sessions.Date.frozen_at`) and a rename would break Obsidian links.
A second session on the same local date appends ` 2`, then ` 3`
(`sessions/2026-09-01 2.md`).

Front-matter keys and column headers are the schema's property names, spelled
as declared. A key or a column appears in a note when at least one value in
that note is not the property's declared `default`. Otherwise it is left out,
and a missing key or column reads back as the default. Notion does the same
with an unset property, so this is not a new rule, and it is what keeps the
plain squat session above at nine columns instead of thirty-one.

Four properties are never stored:

| Property | Comes back from |
|---|---|
| `Session` | the note the row is in |
| `Set` | `Notes`, or `Exercise`, `Set index` and the magnitudes (`session_runner.titles.title_for`) |
| `write_key` | the note's `Start time` and `Timezone`, then `Exercise`, `Set index` and `attempt`, joined with `\|` (`session_runner.rows.write_key`) |
| `e1RM` | `load_adjust.read_layer.e1rm` |

A stored copy of any of the four would be a second source of truth that a hand
edit to the visible row could put out of step. A derived `write_key` moves
with the row instead. Both session fields it needs, `Start time` and
`Timezone`, are in the note's front matter, so every row in one note derives
the same session half. The row's own `Timestamp` is not one of them: it moves
set by set, and the session half does not.

`e1RM` is a Notion `formula`, and a markdown table cannot compute one.
`formula` columns are never stored and are computed on read by
`load_adjust.read_layer.e1rm`, which `tools/schema/check_e1rm.py` already
holds to the same answer as the Notion expression.

`vault.NOT_STORED` is that same list in code, so the payload's column list
already excludes it: `Sets` contributes 27 of its 31 schema properties, and
`Sessions` all 15. Regenerate both counts with:

	python3 -c "import sys; sys.path.insert(0, '.claude/skills/intake/scripts'); import ddl, vault; s = ddl.load_schema(); print({d: len(vault.columns(d, s)) for d in s['databases']})"

## Config notes

One config page is one note, and every key is a front-matter key. The page
name is the path: `config/athlete` is `config/athlete.md`, and
`program/history/2026-09-01` is `program/history/2026-09-01.md`. A value
holding a JSON document is written as a YAML block scalar (`body: |-` with the
JSON indented under it). Two keys hold JSON today, `program/current.body` and
`agent/progression-state.progression`.

**Untested.** Obsidian's Properties editor rewrites front matter when somebody
edits properties in the panel, and it may reformat a block scalar. Nobody has
tested this, and this document asserts it neither way. If a block scalar does
come back mangled, the fallback is to move long values out of the front matter
into the note body, under a `## <key>` heading, as a fenced json block.

## Reading a vault back

`tools/mock-notion/hydrate.py` issues nine reads in a fixed order. Against a
vault, each one is a file operation:

| Read verb | Vault operation |
|---|---|
| `config-read config/preferences` | parse `config/preferences.md` front matter |
| `config-read config/limits` | parse `config/limits.md` |
| `config-read config/athlete` | parse `config/athlete.md` |
| `config-read program/current` | parse `program/current.md` |
| `config-read agent/progression-state` | parse `agent/progression-state.md` |
| `row-query Sets *` | one shell pass over `sessions/*.md` table rows |
| `row-query Sessions *` | one shell pass over `sessions/*.md` front matter |
| `row-query Sessions Status=open` | filter that same result |
| `row-query Sessions Status=closed` | filter that same result |

There is no index file. The store's query engine is the shell: `row-query
Sets *` is one pass over `sessions/*.md`, not one read per session.

`row-query Sets *` returns whole rows, not a projection.
`from_sets.known_exercises` needs each row's magnitudes as well as its
`Exercise`, because `catalog.infer_measure(row)` reads them when the shipped
defaults do not carry the name.

**Known ceiling: writing works, reading does not.** Within one chat `state`
never goes cold, so a first "set me up" and every set logged after it land in
the vault. A second chat cannot rebuild `state`, because nothing parses a
session note back yet: `hydrate.py` has a Notion reader and no vault one. The
table above is the plan for that reader, not a description of code that
exists. `vault.py` carries the same ceiling as a `ponytail:` comment.

## One write touches one file

Rule L8 against a vault is two existence questions. The note exists or it does
not. A table row with that derived `write_key` exists or it does not. A
re-sent `row-create` merges into the matching row and changes nothing if
nothing changed, the same contract `tools/mock-notion/writer.py` `row_create`
holds today.

Performing one `row-create Sessions` may touch one file and nothing else.
There is no index to keep in step, and no second note to write.
