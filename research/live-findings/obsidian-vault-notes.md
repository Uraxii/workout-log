# The Obsidian vault store

In plain words: today this trainer can only put your workouts into Notion, and
it refuses everything else on purpose. This document says exactly how to add a
second place to put them, a folder of markdown files that Obsidian opens, so
that somebody who has never seen this repo can build it without having to make
any of the calls again.

**Status.** Design only. Nothing here is implemented. Written 2026-09-06
against `master` at `9dc5ed84e7d0779e9fd49f6da1930f206a43ab08`.

This is an explanation document, the same kind as
`/var/home/nicole/Projects/workout-log/docs/storage-section-design.md`, which
stays the authority for the intake storage section and which this document
supersedes on three points, each marked SUPERSEDES below.

**Fixed inputs from the owner, not re-opened here.** Desktop only, no phone.
A brand-new test vault, never an existing one. The agent reaches the vault
with ordinary file tools against a path. No Obsidian MCP server, no Local REST
API plugin, no Obsidian Git.

---

## 1. The property that must not break

In plain words: the Python in this repo never touches the internet or the
athlete's files. It takes a chat line, returns a list of writes, and the model
performs them. That is what lets these skills run in a sandbox with no network.
Adding a filesystem store does not change it.

`AGENTS.md` states it. `docs/architecture.md` "The script seam" states the
contract: every skill seam is a pure function of `(line, state)` returning
`{"writes", <say key>, "state"}`.

It survives, unchanged, and here is why the reasoning is not wishful:

- The skill scripts already never reach Notion. `intake.py` returns a
  `database-create` write; something else performs it. Nothing in
  `.claude/skills/` has ever held a Notion token.
- All store I/O today lives in two places: the model, in production, and
  `tools/mock-notion/`, in the fixtures. A vault changes what those two do and
  nothing else.
- The one file I/O the skill scripts do is reading package data:
  `ddl.py` reads `schema/notion-schema.json`, `rows.py` reads
  `exercises/defaults.json`. That is shipped reference data, not the athlete's
  store, and the vault profile does the same and no more.

**The guard.** The new file at risk is
`/var/home/nicole/Projects/workout-log/.claude/skills/intake/scripts/vault.py`,
which computes vault paths and could very easily be tempted to check whether
one exists. It takes the vault root as `str` and returns `str`, never
`pathlib.Path`. A module that never imports `pathlib` cannot open a file by
accident. That is a type-level guard, which beats a comment or a lint rule.

If you find yourself needing a real filesystem read inside a skill script,
stop. That is the design breaking, not a detail. Say so loudly and re-open
this document.

---

## 2. What the log looks like on disk

**The decision: one markdown note per session. The session's own fields are
YAML front matter. Its sets are the rows of one markdown table in the body.**

```
<storage_root>/
  config/athlete.md
  config/preferences.md
  config/limits.md
  program/current.md
  program/history/2026-09-01.md
  agent/progression-state.md
  sessions/2026-09-01.md
  sessions/2026-09-03.md
```

`<storage_root>` is whatever path the athlete gives. She can point at a vault
root or at a subfolder inside a vault, and nothing in the store cares. There
is no configurable subfolder name, because there is nothing for one to buy.

A session note:

```markdown
---
Title: 2026-09-01 A1
Date: 2026-09-01
Timezone: UTC
Status: closed
Start time: 2026-09-01T18:00:00+00:00
End time: 2026-09-01T18:45:00+00:00
Program: GZCLP
Day: A1 (squat T1, bench T2)
week_index: 36
Readiness: 4
---

| Exercise | Set index | Timestamp | Load | Unit | load_kind | Reps | source_message_id | confirm_line |
|---|---|---|---|---|---|---|---|---|
| Barbell Squat | 1 | 2026-09-01T18:00:00+00:00 | 225 | lb | absolute | 5 | msg-3 | |
| Barbell Squat | 2 | 2026-09-01T18:00:00+00:00 | 225 | lb | absolute | 5 | msg-3 | |
| Barbell Squat | 3 | 2026-09-01T18:00:00+00:00 | 225 | lb | absolute | 5 | msg-3 | Barbell Squat set 1-3, 225 lb x 5. Set 4 at 225 lb. |
```

### Why this shape

Obsidian's unit is the note, and a session is the natural note. You open a
date, you see what you did that day. The join that Notion expresses with
`Sets.Session` is expressed here by containment, which costs nothing and reads
better.

`Date` is frozen at open (rule L4, `schema/notion-schema.json`
`Sessions.Date.frozen_at`), so the filename can carry the date and never has
to be renamed. Renames break Obsidian links, so a store shape that needed one
would have been wrong. The frozen field is what makes this safe, and it is
already there.

Two sessions on the same local date get ` 2`, ` 3` appended
(`sessions/2026-09-01 2.md`). Note that `hydrate._sessions_by_date` already
keys on `Date` alone and keeps the last one, so the store is no worse than the
reader. See open question 3.

### The alternatives, and why each lost

- **One note per set.** Hundreds of near-empty notes; the file list and graph
  become useless; a human cannot edit a session as a unit.
- **One append-only `log.md`.** Every read pulls the whole history; Obsidian's
  backlinks and outline buy you nothing on one giant file.
- **A folder per exercise.** Reads beautifully for "how is my squat going" and
  fails at writing: a mixed session would land in six files with no
  transaction. The exercise view is a Dataview query away; the session is the
  unit of writing.
- **Everything in YAML front matter, sets as a list under a key.** Machine
  perfect, human hostile. Editing a set means editing YAML.
- **Two notes per day, `sessions/<date>.md` and `sets/<date>.md`,** mirroring
  Notion's two databases exactly. No new concepts, but the athlete has to open
  a second file to see what she lifted, and two files per day must stay in
  sync. Containment wins on the axis this whole change exists for.

### The strongest argument against it, stated plainly

A markdown table with 10 to 16 columns is not a nice thing to look at, and
`schema/notion-schema.json` declares 31 properties on `Sets`. Notion hides
columns in views; a markdown table cannot. If the table turns out to be
unreadable in practice, the fallback is not a different file shape, it is a
Dataview or Bases view note that renders a friendly subset, and the raw table
stays the storage. Do not solve it by splitting the row across two places.

### Which columns actually appear

A column appears in a note's table when at least one row in that note carries a
value for it that is not the schema's declared default. Otherwise it is left
out, and a missing column reads back as the default. This is what Notion
already does with an unset property, so it is not a new rule, and it is what
keeps a plain squat session at nine columns instead of thirty-one.

Four properties are never stored, because the store can regenerate each one
and a stored copy would be a second source of truth that a human edit could
put out of step:

| Property | Regenerated from | Why not store it |
|---|---|---|
| `Session` | the note the row is in | that is the whole point of containment |
| `Set` | `Exercise`, `Set index`, and the magnitudes | it is the Notion title, restating the row; a markdown table needs no title |
| `write_key` | `Timestamp`, the note's `Timezone`, `Exercise`, `Set index`, `attempt`, joined with `\|` | every part is already visible in the row |
| `e1RM` | `.claude/skills/load-adjust/scripts/read_layer.py` | it is a Notion `formula`; a markdown table cannot compute |

The `write_key` one deserves its reason spelled out, because it is the
identity key that rule L8 dedups on. If a human edits `Set index` in the
table, a derived `write_key` changes with it and the row keeps matching what
you can see. A stored `write_key` would go stale in exactly the same edit and
would then disagree with the visible row. Derived is not worse here; it is
better.

`e1RM` is safe to drop because `tools/schema/check_e1rm.py` already holds the
Notion formula and `read_layer.e1rm` to one answer, so the vault gets the same
number from the half that is already proven.

### Config pages

**The decision: one config page is one note, and every key is a YAML
front-matter key. A value that is a JSON document is written as a YAML block
scalar.**

A config page is already a flat map of string keys to string values
(`writer.config_write(page, key, value)`), and YAML front matter is exactly
that. Obsidian renders it in the Properties panel for free. Page names map
straight to paths: `config/athlete` becomes `config/athlete.md`,
`program/history/2026-09-01` becomes `program/history/2026-09-01.md`.

Two keys hold JSON today and are long: `program/current.body` and
`agent/progression-state.progression`. They go in as block scalars (`body: |-`
and the JSON indented under it).

**Named risk.** Obsidian's Properties editor rewrites front matter when
somebody edits properties in the UI, and it may reformat a block scalar. I have
not tested this and will not assert it either way. The exposure is small
because config pages are agent-written and the athlete changes them by talking,
not by opening the panel. If the round-trip check in section 6 catches
mangling, the fallback is to move long values into the note body under a
`## <key>` heading as a fenced ```json block. That is a store-profile change,
not a schema change, and it touches one file.

---

## 3. Reading state back on a cold start

In plain words: when a new chat starts, the agent has forgotten everything and
has to work out from the files what program you are on and what you have
already lifted. This is how it does that without opening a year of workouts.

Today `tools/mock-notion/hydrate.py` issues nine reads, in a fixed order, and
`expected.tsv` asserts that order. Against a vault each one maps to a file
operation:

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

**The decision: there is no index file. The store's query engine is the
shell.** `row-query Sets *` is one `grep`/`awk` pass over
`sessions/*.md`, not one file read per session. A year at three sessions a
week is 156 small notes, and one command reads all of them and returns a few
kilobytes. The answer to "how does it not read every file ever written" is
that it does read them, in one tool call, projecting what the caller needs.

**The alternative I built first and then deleted: a derived
`sessions/index.md`,** one table row per session, rewritten on every session
write. It lost on two counts. It is a copy of data whose source of truth is the
session notes, which is the drift shape
`principle-code-quality` calls an unowned value, and it would have needed a
rebuild-by-sweep command and a check that the sweep agrees with the index.
All of that machinery exists to avoid a cost the shell does not actually charge.
Do not add it. If a read genuinely gets slow, the fix the repo already named is
the one to take: `hydrate.py`'s own comment says to add a range filter to
`row_query` and filter on `Timestamp`.

**Why `row-query Sets *` cannot return a projection.** `from_sets.known_exercises`
needs each row's magnitudes, not only its `Exercise`, because
`catalog.infer_measure(row)` reads them when the shipped defaults do not carry
the name. So the read returns whole rows. Returning fewer would be a read verb
that lies about its own filter, and every later reader would inherit the lie.

---

## 4. What a store profile is

In plain words: the list of things the code has to know about a place before it
can write there. The surprising answer is that it is short, because the model
does the actual store work and a reference document tells it how.

A profile is one module per store, and `storage.py` holds the registry. Five
names:

| Field | Notion | Obsidian |
|---|---|---|
| `ID: str` | `"notion"` | `"obsidian"` |
| `ROOT_KEY: str` | `"storage_root"` | `"storage_root"` |
| `ROOT_PROMPT: str`, `ROOT_REASK: str`, `root_parse(line) -> str \| None` | the Notion page-link question and `readers.page_id` | the vault-path question and a new `readers.vault_path` |
| `create_payload(db, root) -> dict` | `{parent, title, schema}` with a `CREATE TABLE` string | `{parent, title, schema}` with the folder and the ordered column list |
| `LAYOUT_REF: str` | `references/db-create.md` | `references/vault-layout.md` |

And in `storage.py`:

```python
PROFILES = {"notion": ddl, "obsidian": vault}
PROVEN = frozenset(PROFILES)

def profile(state): ...          # the module for state["storage_platform"]
def next_create_write(state): ...  # moved here from ddl.py, dispatches
```

`PROVEN` is derived from `PROFILES`, never written out a second time. Adding a
third store is one dict entry and cannot leave a stale proven-set behind.

`next_create_write` moves out of `ddl.py` into `storage.py`, because the loop
("the next database still missing, one per turn, gated on `is_proven` and on a
root being answered") is store-agnostic and only `create_payload` differs.
`ddl.py` keeps `render`, `create_payload`, `load_schema` and `COLUMN_DDL`, and
becomes the Notion profile in name as well as in fact.

### Everything else lives in the layout reference, not in Python

`docs/storage-section-design.md` already assigns store conventions to the
model at run time: auth, paging, rate limits, id threading. The vault's
conventions belong in the same place. `references/vault-layout.md` is the
vault's twin of `references/db-create.md` and must carry:

1. The directory layout in section 2, verbatim.
2. The front-matter and table encoding, including the column-omission rule and
   the four regenerated properties.
3. That `Sets` rows live inside `Sessions` notes, keyed by the note itself.
4. That `formula` columns are not stored and come from
   `load_adjust.read_layer` on read.
5. The read plan in section 3, one shell operation per read verb.
6. Idempotency: rule L8 against a vault means the note exists or it does not,
   and a table row with that derived `write_key` exists or it does not. A
   re-send merges into the matching row and changes nothing if nothing changed,
   the same contract `writer.row_create` holds today.
7. That performing one `row-create Sessions` may touch one file and nothing
   else. There is no index to keep in step.

### Are the other skills already store-agnostic?

Yes, and I checked rather than assumed. `grep -rn "import storage"` over
`.claude/skills` and `tools` returns four call sites: `ddl.py`,
`questions.py`, `readers.py` (a docstring only), and `hydrate.py`.
`program-design` and `session-runner` emit `row-create` and `config-write` with
schema field names and know nothing about any store. The blast radius of this
change is `intake` plus the harness.

---

## 5. The write verbs

**The decision: the verb vocabulary survives unchanged. No new verbs.**

| Verb | Against a vault |
|---|---|
| `database-create(db, payload)` | make the `sessions/` folder, return its path as the id. Both `Sets` and `Sessions` resolve to the same folder, which is the honest answer to "where do Sets rows live". |
| `row-create(db, payload)` | `Sessions`: create or update the session note. `Sets`: append or merge one row in that note's table. |
| `config-write(page, key, value)` | set one front-matter key in one note. |
| `config-read(page)` | parse one note's front matter. |
| `row-query(db, where)` | one shell pass over `sessions/*.md`, filtered. Exact match only, as today. |

I looked for a filesystem operation no verb carries, and did not find one that
earns a verb:

- **Delete.** Nothing in the repo deletes anything today.
- **Rename.** The only candidate is correcting a session's date, and `Date` is
  frozen at open (rule L4). There is nothing to rename.
- **The index rewrite.** Deleted from the design in section 3, so it cannot
  need a verb.

The one thing worth arguing about is whether "the model does more than one
file operation to satisfy one verb" means the verb is a fiction. It does not.
The verb vocabulary is what the skill scripts emit. How a store satisfies a
verb is the store's business, exactly as Notion updating its own indexes behind
one API call is Notion's business. That division is already written down in
`docs/storage-section-design.md`.

---

## 6. What happens to `PROVEN` and to `fixtures/13-storage-refusal`

`PROVEN` becomes `frozenset(PROFILES)`, so it is `{"notion", "obsidian"}` and
"airtable" is still refused. The fixture keeps its job, keeps its name, and
gets a new expected line.

`storage.refusal` must render the store list from the registry rather than
holding it in a string, so a third store cannot leave the sentence stale.
With two stores registered, the exact replacement line, which
`fixtures/13-storage-refusal/expected.tsv` asserts byte for byte:

```
I can't write to Airtable yet. Notion and Obsidian are the ones I've been proven against, and I'd rather say so now than build you half a log. I've written down that you asked for Airtable. Say 'notion' or 'obsidian' and I'll set that up instead.
```

The joining rule for `refusal()`: capitalize each id, join with `" and "` for
two and with `", "` plus a final `", and "` for three or more; the closing
sentence joins the lowercase ids the same way with `or`.

Two more spoken lines change, and both are in `questions.FIELD_STEPS`:

```
Where do you want your training log kept? Notion and Obsidian are what I can write to today. Name anything else and I'll tell you straight away rather than half build it.
```

```
I need the name of a place to put it. Notion and Obsidian are the ones I can write to today.
```

Render both from the registry too. Four fixtures carry the prompt and must be
regenerated: `05-first-run`, `12-intake-parent`, `12-parq-reask`,
`13-storage-refusal`.

### New fixtures

- `fixtures/15-vault-first-run`, the Obsidian twin of `05-first-run`. Answers
  "obsidian", gives a vault path, asserts the two `database-create` writes
  carry vault payloads, and asserts the rest of the question flow is
  byte-identical to the Notion run.
- `fixtures/15-vault-cold-start`, the Obsidian twin of `07-cold-start`. This is
  the one that matters, because it asserts that a chat boundary against a vault
  rebuilds the same `state` the Notion run rebuilds.

---

## 7. What `make check` proves

In plain words: the repo's proof today is 26 recorded conversations replayed
against a fake Notion. To prove the vault, give the same harness a second fake
store that writes real markdown files into a temporary folder and reads them
back, then check that both stores answer the same questions the same way.

`tools/mock-notion/writer.py` is already nearly store-neutral: it validates
payloads against the schema and keeps rows and config in dicts. The only Notion
in it is `notion_ddl.validate_create`.

Three additions to `make check`:

1. **Payload validity.** `tools/mock-vault/vault_layout.py` is the vault's
   `notion_ddl.py`: it asserts a `database-create` payload names a folder under
   the vault root and a column list that matches the schema.
2. **The differential.** For every fixture, replay it a second time through a
   vault backend that writes real files under a temporary directory, then
   assert `hydrate(vault_reader) == hydrate(notion_reader)`. This is the
   round-trip probe `docs/storage-section-design.md` deferred to phase 4, now
   buildable because the second store exists. **Read
   `tools/replay/check_replay.py` first**: it is already a
   glob-derived differential check wired into `make check`, and this one should
   be its sibling, not a new pattern.
3. **The two new fixtures** replay the ordinary way.

What `make check` still cannot prove, and needs a human with Obsidian open:

- that the table renders readably,
- that the Properties editor does not mangle a block scalar,
- that the athlete's real vault path is writable.

Say so in the commit body rather than claiming the vault is proven.

---

## 8. The smallest first increment

**One task: make `intake` accept "obsidian" without refusing, and emit two
`database-create` writes with vault payloads.**

That is enough for the owner to say "set me up", answer "obsidian", paste a
path to a brand-new vault folder, and watch `config/athlete.md` and
`sessions/` appear. Nothing else is needed for that, because within one chat
`state` never goes cold, so session logging works on day one with no read path
at all.

The known ceiling: the SECOND chat does not work yet, because nothing parses
the notes back. That is the next task, not this one. Write it down as a
`ponytail:` comment naming the ceiling, the way this repo already does in
`hydrate.py`.

Concretely, that first task is:

1. `.claude/skills/intake/scripts/vault.py`. New. `ID`, `ROOT_KEY`,
   `ROOT_PROMPT`, `ROOT_REASK`, `root_parse`, `create_payload`, `LAYOUT_REF`.
   Strings in, strings out, no `pathlib`.
2. `.claude/skills/intake/scripts/storage.py`. `PROFILES`,
   `PROVEN = frozenset(PROFILES)`, `profile(state)`,
   `next_create_write(state)` moved in from `ddl.py`, `refusal()` rendering
   from the registry.
3. `.claude/skills/intake/scripts/ddl.py`. Delete `next_create_write`; add
   `ID`, `ROOT_KEY`, `ROOT_PROMPT`, `ROOT_REASK`, `root_parse`, `LAYOUT_REF`
   so it is a profile like the other one.
4. `.claude/skills/intake/scripts/readers.py`. Add `vault_path`.
5. `.claude/skills/intake/scripts/questions.py`. The `notion_parent_page_id`
   row becomes one `storage_root` row whose prompt, reask, parse and key come
   from the profile. `prompt_for`, `reask_for` and `parse` take the profile.
6. `.claude/skills/intake/scripts/intake.py`. Call
   `storage.next_create_write`; pass the profile to the question functions.
7. `schema/notion-schema.json`. Add `storage_root` to
   `config_pages["config/athlete"].keys`. Keep `notion_parent_page_id` in the
   list; see section 9.
8. `tools/mock-notion/hydrate.py`. Read `storage_root`, falling back to
   `notion_parent_page_id` when it is absent.
9. `.claude/skills/intake/references/vault-layout.md`. New, contents per
   section 4.
10. `.claude/skills/intake/references/questions.md` and
    `.claude/skills/intake/SKILL.md`. The storage question now names two
    stores and the root question varies by store.
11. `tools/intake/check_questions_docs.py`. Render prompts per profile.
12. `fixtures/15-vault-first-run`. New.
13. Regenerate `05-first-run`, `12-intake-parent`, `12-parq-reask`,
    `13-storage-refusal`.

Touch them in that order. Steps 1 to 6 are the code, step 7 unblocks the
write, 8 to 11 keep the docs and the checker honest, and 12 to 13 are the
proof. Do not run `python3 tools/mock-notion/replay.py --update` before step 6
is finished; a regenerated fixture is only worth its bytes if the code behind
it is the code you meant.

Task two, after the owner has seen files appear: the read path, section 3,
plus `tools/mock-vault/` and the differential in section 7, plus
`fixtures/15-vault-cold-start`.

---

## 9. Three points where this supersedes `docs/storage-section-design.md`

**SUPERSEDES 1. `notion_parent_page_id` gets renamed to `storage_root`, and
`notion_data_sources` does not.** The old doc said to rename the parent page
id "in the same change that adds the second store". Agreed, and the reason is
sharper than a tidier name: a vault path is not a page id, so the key's meaning
changes, and one key holding two meanings across stores is the loose type
`principle-code-quality` warns about. `notion_data_sources` keeps its ugly name
because its meaning does not change, it is `{container: id}` in both stores,
and renaming it would cost a second migration read for nothing. A rename that
touches the athlete's stored data has to buy something; one of these two does
and the other does not.

The migration is one line in `hydrate.py`, reading `storage_root` and falling
back to `notion_parent_page_id`. That is a read of legacy athlete data, not a
compatibility shim, and the repo already does exactly this: see the `tz`
fallback to the last session's `Timezone` in `hydrate._session_state`, whose
comment reads "a workspace set up before the question existed".

**SUPERSEDES 2. There is one root question, not two.** The alternative was a
second `FIELD_STEPS` row for the vault path, skipped when the store is Notion,
using the pre-answered `"n/a"` machinery that `parq_followup` already uses. It
loses because it is a parallel branch beside the old path, which is the exact
bolt-on shape `principle-redesign-from-first-principles` names. Built knowing
both stores from day one, the question "where inside the store" is one
question whose words the store owns. The cost is threading the profile through
`prompt_for`, `reask_for` and `parse`, which is four signatures.

**SUPERSEDES 3. The phase-4 round-trip probe becomes phase 1 of this work,
because it is now the cheapest real proof available.** The old doc deferred it
as speculative with no second store to check. There is a second store now, and
`tools/replay/check_replay.py` has since landed a differential-check pattern
to copy.

`schema/notion-schema.json` keeps its filename. I considered renaming it to
`log-schema.json` since it is mostly store-neutral, and decided against it: it
still carries the Notion `e1RM` formula expression with `prop("Set type")` in
it, so a store-neutral name would be a lie. Rename it the day that expression
moves out.

`storage.container_name` stays the TODO stub it is today. It belongs to the
old doc's phase 2, the collision-and-prefix question, which nothing in this
change needs. Do not fill it in on the way past.

---

## 10. The prior research, objection by objection

`research/01-storage-options.md` recommends dropping Obsidian. Here is every
reason it gave, and whether it still stands.

| Objection from research/01 | Verdict |
|---|---|
| Obsidian Git's own README says it is "very unstable" on mobile and the maintainer does not recommend it there. "The mobile leg is the whole point, so this fails on its own terms." | **DIES-WITH-MOBILE.** Twice over: mobile is not a requirement, and the owner ruled out Obsidian Git entirely. |
| The Local REST API plugin binds to localhost inside a running Obsidian, so the agent can only reach the vault when the desktop is awake. "For a phone-first log that is fatal." | **DIES-WITH-MOBILE.** The log is not phone-first, and there is no Local REST API in this design. The agent runs on the desktop and the vault is a local folder it already has. |
| Obsidian Sync is $4 to $8 a month and "gives an agent nothing". | **SURVIVES as a fact, DIES as an objection.** Nothing here needs Sync. |
| Obsidian Publish is $8 to $10 a month with no agent write path. | **SURVIVES as a fact, irrelevant.** Sharing is not a requirement. |
| Obsidian scores "poor" on mobile edit and has no web-plus-auth surface at all. | **SURVIVES.** Real, accepted cost. No reading the log from a browser, no link to a coach. |
| Roughly 8 setup steps for a friend to replicate, against Notion's 4. | **SURVIVES, and gets worse.** A friend now needs a local agent with filesystem access. The README's "published for others to run" claim now has two audiences with very different setup costs. Worth a line in the README when this ships. |
| Third-party Obsidian MCP servers are a churning corner of GitHub, "treat any pick as a moving target". | **SURVIVES as a fact, DIES as an objection.** No MCP server here. |
| Offline: good. Lock-in: none, plain text. "Git gives you exactly the bytes you wrote." | **SURVIVES, and these are now the reasons to do it.** |

**The row the research never had.** Every Obsidian option in that table assumed
a bridge: Git, the Local REST API, or an MCP server. "A plain folder the local
agent writes with ordinary file tools" is not in the table at all. That is why
the recommendation flips, and it is worth being precise about: no fact about
Obsidian changed, an option was missing.

I did not lean on `docs/limitations.md`. Its L-15 entry describes `Exercise` as
a required relation, and `schema/notion-schema.json` declares it `rich_text`
with a note that identity is the name, so that entry is stale. Nothing here
depends on it.

---

## 11. What this document does not decide

The implementer's judgment starts here.

1. **The exact filename format for session notes** beyond "the date leads and
   `Date` is frozen so it never changes". Whether the day label joins it is
   yours.
2. **Whether Obsidian's Properties editor mangles a YAML block scalar.** Needs
   one real test in the real app. Section 2 names the fallback either way.
3. **The exact shape of `tools/mock-vault/`,** including whether it subclasses
   `writer.MockNotion` or stands beside it. Read `writer.py` and
   `check_replay.py` and decide there.
4. **The markdown table parser.** Whether it is a regex, `csv` with `|` as the
   delimiter, or hand-rolled. Stdlib only, and it lives in `tools/mock-vault/`,
   never in a skill script.
5. **Whether a Dataview or Bases view note ships with the vault** so the athlete
   gets a friendly per-exercise view. Nice to have, not part of the store.
6. **Conflict policy** when the athlete hand-edits a session note between
   chats in a way the parser cannot read. A follow-up, not this change.
7. **Vault backup or sync.** Out of scope entirely.
8. **Whether one install can write to both stores at once.** It cannot, and
   nothing here plans for it. One `storage_platform`, one store.

---

## 12. Open questions for the owner

1. **Two sessions on the same local date.** The design gives the second note a
   ` 2` suffix, matching what `hydrate._sessions_by_date` already half-handles
   by keeping the last one. If two-a-days matter, that reader needs fixing
   first and it is a separate ticket.
2. **The wide table.** Nine columns for a plain squat session, up to sixteen
   with RPE, notes and per-side reps. Worth eyeballing one real note in Obsidian
   before task two starts.
3. **The README's "published for others to run" claim.** A vault store makes
   this repo harder for a non-technical friend, not easier. Does that claim
   need re-scoping, or does the vault stay the owner's own path while Notion
   stays the shared one?
4. **The live Notion install.** The `storage_root` rename means the existing
   `config/athlete` page keeps a `notion_parent_page_id` key that nothing
   writes any more. Leave it, or have intake rewrite it once on the next run?
   Leaving it is the reversible choice and is what this design assumes.

---

## CORRECTION, appended 2026-09-06 after the first live vault run

In plain words: one statement in section 2 of this document is wrong, and it
would have quietly broken the app's protection against logging the same set
twice. The document is append-only, so the error stays visible above and this
note supersedes it.

**Section 2 says `write_key` rebuilds from the row's own `Timestamp`. It does
not.** `.claude/skills/session-runner/scripts/rows.py:42-47` builds it as
`session_key|exercise_id|set_index|attempt`, and `session_key` comes from the
session's START time, frozen once when the session opens
(`session_open.py:38`, from the same `now` that fills `Start time`).

Verified by the main session against the real files, not inferred:
the live note `sessions/2026-09-01.md` carries one `Start time` of
`09:00:00+00:00` against row timestamps of `09:05`, `09:09` and `09:13`.

Consequence had it shipped: a vault reader following section 2 would compute
three different session keys for one session, and rule L8's duplicate check
would stop matching from the second set onward.

Already fixed in the code and in
`.claude/skills/intake/references/vault-layout.md` at commit `c0919e4`.
Section 2 of this document is the remaining stale copy. Anyone rewriting the
vault layout must read THIS note, not section 2.

Two further corrections from the same run:
- Eight `Sessions` properties have no emitter at all (`Title`, `Program`,
  `Day`, `Cursor`, `Session RPE`, `Bodyweight`, `Bodyweight unit`, `Notes`),
  so section 2's example note showed keys nothing writes.
- Unquoted dates round-trip through YAML as `datetime` objects, not ISO
  strings, so a future vault reader has to re-serialize them.
