# Architecture, phase 1

Structure only; `docs/build-plan.md` is the authority for content.

## File tree

```
schema/notion-schema.json                    # the one schema: 4 dbs, 7 measure kinds, config pages
tools/mock-notion/writer.py                  # offline Notion: 3 write verbs, appends TSV
tools/mock-notion/reader.py                  # offline Notion: 2 read verbs, appends TSV
tools/mock-notion/hydrate.py                 # turn-1 state rebuilt from reads alone
tools/mock-notion/replay.py                  # phase proof runner: transcript -> writes -> diff
.claude/skills/<skill>/SKILL.md              # the LLM half: conversation, retrieval, gating
.claude/skills/<skill>/scripts/*.py          # the deterministic half: parse, arithmetic, row shaping
fixtures/<NN-name>/transcript.txt            # input, one user line per turn
fixtures/<NN-name>/expected.tsv              # the assertion
```

`schema/notion-schema.json` is the single source of truth for database names,
properties, types, enums and the `measure_kinds` table: `intake` creates the
databases from it, the mock writer validates against it, `confirm_line` renders
magnitudes in its declaration order.

## The script seam

Skill-side scripts are Python 3 stdlib, pure, no I/O. The LLM does the
conversation; the script does the parse, the arithmetic and the row shaping, so
a fixture replays it with no LLM and no Notion.

```
log_set(line: str, state: dict) -> Turn
Turn = {"writes": [Write], "confirm_line": str, "state": dict}
Write = {"verb": "row-create"|"config-write", "target": str, "payload": dict}
```

- **In**: one user chat line, plus `state`, which is JSON and is the whole
  input besides the line: frozen session clock and zone (rules L3, L4), open
  session id and cursor, catalog rows in scope, per-exercise carry-forward.
- **Out**: writes not yet applied, the line the agent says back, and the next
  turn's `state`. The caller applies the writes; the script never calls Notion.
- **Two callers, one contract**: in process (`from log_set import log_set`) for
  the replay runner, or `python3 log_set.py` with `{"line", "state"}` on stdin
  and a `Turn` on stdout for an agent that can only shell out.
- **Never empty**: an unparseable line still returns a write, the verbatim
  `Notes` row of ladder rung 5.

## Mock writer contract

Accepts the three write verbs a skill may use (build-plan s6), plus a
fixture-only seeder:

- `row_create(db, payload) -> page_id`. Validates db, property names and enum
  values against the schema; raises `SchemaViolation` otherwise. Query before
  create on the schema's `identity` key (rule L8): a match is an **upsert**,
  not an adopt-and-ignore (phase 3 defect 1) — the payload merges into the
  stored row and only the fields whose value changed get appended, so a
  resend with identical content still appends nothing. Page ids are
  `<db lowercased>-<n>` in creation order, so ids are stable across runs.
  `Sessions` has no payload-derivable identity in the schema (`identity:
  ["page_id"]`, unusable: a real page id does not exist until after the row
  is created, and `pain-triage`'s halt write carries only `{"Status": ...}`,
  no identity field at all). `_resolve_session` settles this without a
  schema change: a write carrying the frozen open fields (`Date`,
  `Timezone`, `Start time`, rules L3, L4) keys on that tuple; any other
  `Sessions` write targets whichever session is currently open (there is
  exactly one at a time, rule L16). L9's idempotency read as `identity`
  alone, not `source_message_id`: `write_key` already varies by `Set index`
  within a turn, so it is each row's real per-row identity, and a
  multi-row turn (a ladder, an EMOM) no longer needs the `#<offset>`
  suffix `source_message_id` hack phase 2 used to work around the
  collision (see `write_key` below).
- `config_write(page, key, value)`. Same query-before-create; rewriting an
  identical value appends nothing. `program/current` and
  `program/history/<date>` name their allowed fields `headers`, not `keys`
  (schema is frozen this phase); `config_write` validates both the same
  way, since a table-shaped program page and a key-value config page differ
  in presentation, not in what needs validating.
- `database_create(db, parent)`. `intake`'s one-time schema creation, one
  call per database. See "Phase 5 note: intake and screen" below.
- `seed_row(db, payload)`. Fixture preamble only, appends nothing.

One TSV per run. One line per field whose value is neither null nor `false`, in
schema declaration order, so written defaults (`Set type working`, `Side both`,
`attempt 0`) are asserted and unset columns are asserted by absence.

## Mock reader contract

Two read verbs, in `tools/mock-notion/reader.py`:

- `config_read(page) -> dict[str, str]`. Returns every key written to that
  page so far. A page the schema's `config_pages` does not declare raises
  `SchemaViolation`, because a page name that is not in the schema is a
  programmer bug and stays loud. A declared page nothing has written yet
  returns `{}`. Those are two behaviours on purpose: an undeclared page is a
  typo, an empty page is a cold start, and a cold start is the ordinary
  turn-1 case rather than an error.
- `row_query(db, where=None) -> list[dict]`. An unknown db, or a `where` key
  that is not a property of that db, raises `SchemaViolation`. Every key in
  `where` matches exactly. There are no ranges, no ordering and no limit,
  because every turn-1 hydration read is an exact match and anything more is
  speculative. Rows come back in creation order, each a copy of the stored
  row plus a `page_id` key. No match returns `[]`.

Rows come back raw, in the unit they were logged in.
`.claude/skills/load-adjust/scripts/read_layer.py` already owns e1RM, unit
conversion and ranking, so the store stays dumb and one place converts.

One TSV line per read call, not one per returned field:

```
config-read	<page>	*	<keys returned>
row-query	<db>	<filter>	<rows returned>
```

`<filter>` is `*` when there is no filter, otherwise the `where` pairs as
`k=v` joined by `,` in sorted key order. The payload is left out deliberately:
the write rows that produced it already assert it byte for byte, and the `say`
row downstream asserts what the user was told about it, so re-emitting it
doubles the file and adds no information. The call plus its result count
proves the read happened, proves its order against the other rows, and proves
the empty case.

### Reads, and the third write verb

`docs/build-plan.md:271` names `config-write` and `row-create` "the only two
**write** verbs any skill may use". A read is not a write, so a read verb does
not touch that rule. `docs/build-plan.md:193` goes further and budgets one:
the ceiling for one logged set is "1 create, at most 1 read, and 0 questions
on the happy path". The spec assumed a read verb. It was simply never built.

`replay.py` enforces no per-turn read ceiling, because no seam issues a read
at all. A seam is a pure function of `(line, state)`, so its per-turn read
count is zero and a ceiling on it could never fail. A check that cannot fail
is worse than no check. Hydration is a turn-1 cost the caller pays, off the
s3.2 budget the same way `intake`'s database-create turn already is.

`database_create` is a documented third **write** verb, settled here rather
than left open. `writer.py` implements it beside the other two, `intake` is
its only caller and calls it once per database (build-plan s5.1), and AGENTS.md
names all three. Ticket R12 (`workout-log-5o8`) keeps the rest of its scope and
no longer owns this question.

### Hydration belongs to the caller

The seam is a pure function of `(line, state)` by contract, so building
`state` is the caller's job: the LLM in production, `replay.py` in a fixture.
That is why adding reads changed no skill-side script.
`tools/mock-notion/hydrate.py` holds `hydrate(reader) -> state`, the
harness's copy of what each SKILL.md's "Turn 1, from cold" section tells the
LLM to do.

## Fixture format

`transcript.txt`: tab separated `@` directives plus user lines.

```
@tz	UTC
@units	lb
@now	2026-09-01T09:00:00+00:00
@exercise	Squat (Barbell)	weight_reps
185x5
```

`@now` may repeat mid transcript, which is how phase 3 crosses midnight without
a second file. Everything not starting with `@` or `#` is one user turn,
numbered from 1 as `source_message_id` `msg-<n>`.

`@cold` marks a chat boundary: the conversation ended, the in-memory `state` is
gone, and the next turn hydrates from the store instead. It tags the turn that
follows it, the same way `@rest_node` already does.

`fixtures/07-cold-start` is what proves it. Day 1 writes a program and a
session, `@cold` throws the state away, and day 2 rebuilds it from reads alone
and must produce output identical to the warm path in `fixtures/04-today`.
`fixtures/05-cold-start` is renamed `fixtures/05-first-run`, because it is a
first-run install transcript and never crosses a chat boundary.

`expected.tsv`: header `verb, target, field, value`, then one line per emitted
write field and one line per read call. Long form, not a wide row table,
because the four databases and the config pages have different columns and
this compares exactly with no projection of one onto the other.

Write and read rows come first, interleaved in emission order, so read/write
ordering within a turn is visible in the file. One `say` row per turn follows
them, in turn order:

```
say	<skill>	<source_message_id>	<JSON encoded text>
```

`target` is the seam that spoke, `field` is that turn's `source_message_id`,
`value` is the exact string the user reads (`log_set`'s `confirm_line`, every
other seam's `say`). JSON encoding keeps a multi-line script such as a PAR-Q+
follow-up on one TSV line. Four columns either way, so one file and one
byte-for-byte compare cover writes and reads together.

### What the say rows prove, and what they do not

- **Asserted exact.** Every string every seam returns, on every turn of every
  fixture. That covers all the wording the spec calls mandatory: `screen`'s
  seven PAR-Q+ questions (`screen.py` parses them from
  `references/parq-plus.md`, so the assertion pins that file too),
  `trainer-core`'s refusals, `program-design`'s no-template refusal script,
  `pain-triage`'s stop hand-off and its refusal to clear on a bare
  confirmation, `load-adjust`'s ask-first deload line. Reword any of them and
  a fixture goes red.
- **Asserted by anchor or substring.** Nothing, and no substring mode exists.
  A seam is a pure function of (chat line, state), so every string it returns
  is reproducible byte for byte and no wording is legitimately variable. Add
  a softer mode when a seam first needs one (a clock reading, a random pick),
  not before.
- **Unasserted.** Prose a model composes around a seam's return value. The
  harness runs no LLM, so that text never reaches the TSV and no fixture can
  speak to it. Mandatory wording that lives only in SKILL.md prose and never
  in a script return value is unasserted for the same reason.

Regenerate an expectation from a real run instead of editing it by hand:

```
python3 tools/mock-notion/replay.py --update fixtures/06-safety
```

`write_key = sha256("<session_key>|<exercise_id>|<set_index>|<attempt>")[:16]`
(rule L8). `session_key = sha256("<start>|<tz>")[:16]` (phase 3 defect 2): the
client-side session identity, the frozen open time plus the frozen zone
(rules L3, L4), not the predicted Notion page id `session_id` used to be
hashed on. A predicted page id is only reproducible against the mock
writer's own deterministic `<db>-<n>` scheme; real Notion assigns opaque
UUIDs at write time, so hashing one is not computable before the write and
breaks at install. `session_key` is computable up front and stable across
a real install. `session_id` still fills the `Sessions` relation on a
`Sets` row; `session_key` only feeds the hash. Deterministic ids make both
hand checkable.

## Running a phase proof

```
python3 tools/mock-notion/replay.py fixtures/01-three-sets
```

Exit 0 on a byte-for-byte match, 1 with a unified diff. No network, no LLM, no
argument beyond the fixture directory.

## HYPOTHESIS, falsified by phase-2 fixtures

- **Long-form TSV.** Phase 2 replays 24 examples plus 5 rows; if that file
  becomes unreadable, switch to one wide TSV per database and keep exact
  compare by emitting the full schema column list.
- **`(line, state)` is enough.** A rule needing history beyond `state` (a PR
  check, a 14-day window) breaks the seam and forces a read verb.
- **Confirm-line rendering.** `<exercise> set <n>, <magnitudes>. <next
  target>.` with magnitudes in schema order is s4's stated shape but does not
  match s4's own sample lines; phase 2 fixtures settle the wording.
- **One script per skill.** `log_set.py` covers phase 1; if phase 2's grammar
  and phase 6's progression outgrow one module each, split by domain, never by
  execution step.
- **Clock granularity.** ~~Every turn in a fixture shares the `@now` in
  force, so `Timestamp` repeats. Rule L9's 120 s retype guard needs finer
  ticks; phase 3 decides whether that is a directive or a state field.~~
  Falsified the other way: phase 3 found the retype guard cannot be a
  content-plus-elapsed-time check in `log_set.py` at all, finer ticks or
  not — identical content in the same slot is completely ordinary training
  data (the same weight for two consecutive working sets), not evidence of
  a retype. Whether a new message IS the last one, retyped, is a
  conversation-layer judgment call with no reliable signal in `(line,
  state)` alone. `replay.py` gained `@resend` (a directive, settling that
  half of the question) to represent that judgment once made; once made,
  the existing `write_key` identity dedup in `writer.py` already makes it
  a no-op, so no state field or elapsed-time arithmetic was needed.

## Known costs

- `tools/mock-notion/` is the plan's s8 path, and a hyphen is not importable,
  so `replay.py` inserts its own directory on `sys.path`. Rename to
  `tools/mock_notion/` if a third consumer ever needs to import the writer.
- Property names are verbatim from s1.2 to s1.8, so casing is mixed (`Set index`
  beside `set_index`). They are Notion display names, so the plan is authority.

Hydration pays for three things the schema does not store where a reader would
look for them:

- **No timezone key anywhere in `config_pages`.** The stored
  `Sessions.Timezone` is the only record of the frozen zone (rules L3, L4), so
  hydration recovers `tz` from the last `Sessions` row. An install with no
  session yet has no zone to recover (`workout-log-ayf.16`).
- **The program cursor is counted, not read.** The schema declares
  `Sessions.Program`, `Sessions.Day` and `Sessions.Cursor`, and no seam writes
  any of them (`workout-log-ayf.15`). Hydration therefore derives the cursor
  by counting `Sessions` rows with `Status: closed`, since each rotation node
  consumes exactly one session, rest nodes included. The ceiling: that count
  runs across all history, not per program, so a second program's cursor
  starts wherever the first one left off.
- **`program/current` stores a display name.** It holds `name` ("GZCLP"), not
  the library id (`gzclp`), so hydration resolves the id by scanning
  `library/*.json` for a matching `name`. Restructuring that page is ticket R2
  (`workout-log-xo0`), not this change.

## Phase 5 note: intake and screen

`intake` and `screen` use the same `(line, state) -> {"writes", "say",
"state"}` seam as `log_set`, with `say` in place of `confirm_line` (the next
question, not a set confirmation). `intake` imports `screen`'s module
directly for its safety block, so the PAR-Q+ text and the clearance-write
rule live in one file (`.claude/skills/screen/scripts/screen.py`), not two.
`replay.py` gained an `@skill` directive to route a fixture's turns to a
named seam (default `session-runner`, unchanged) and an `@intake_cursor`
directive that seeds a resumed conversation's cursor. `@intake_cursor` is
**deprecated and superseded**: the read it stood in for now exists as
`config_read("config/athlete")["intake_cursor"]`, see "Mock reader contract"
above. The directive stays in `transcript.py` for now only because retiring
it would change `fixtures/05-intake-resume`'s expectation, and this wave was
forbidden to regenerate a fixture it does not own. Ticket
`workout-log-ayf.17` owns the retirement. The
writer gained one more verb, `database_create(db, parent)`, query-before-create
like the other two, for `intake`'s one-time schema-creation call (build-plan
s5.1).

## Phase 3 note: lifecycle, write identity, `halted`

Three identity defects, all in `writer.py`'s dedup, none in the schema
(frozen this phase): (1) `Sessions`' declared identity (`page_id`) is
unusable from a payload, so a second write minted a phantom second row;
settled by `_resolve_session`, see "Mock writer contract" above. (2)
`write_key` hashed the predicted `Sessions` page id, which breaks at a
real install (opaque UUIDs, not `<db>-<n>`); settled by `session_key`
(frozen open time plus zone), see "Fixture format" above. (3) L9's
`source_message_id`-alone idempotency assumed one row per message; a
multi-row turn broke it and phase 2 worked around it with a `#<offset>`
suffix. Settled by dedup on `identity` (`write_key`) alone, which already
varies per row within a turn; the suffix is gone, every row keeps its
turn's real `message_id`.

`session-runner`'s scripts split further: `catalog.py` gained
`make_lookup`/`name_for` (pure catalog-only helpers, moved out of
`log_set.py`), and a new `lifecycle.py` holds session opening
(`open_session`, rules L1, L3, L4) and the commands phase 2 left as Notes
rows (`note`, `undo`, `fix set <n> <correction>`, `fix <date> set <n>
<correction>` for L15's 7-day backfill, a rest-node acknowledgement, and
`done for today`). `log_set.py` tries each in order before falling to
grammar parsing, so a command word never reaches the ladder.

A genuinely new session (as opposed to reopening one closed at the exact
same frozen instant) resets `cursor` in `state`: `Set index` is scoped to
`(session, exercise)` per rule L7, and a cursor carried over from a prior,
now-closed session would mislabel a new session's set 1 as a continuation
of the old one. `carry` and `scope` are left alone (out of this phase's
evidence; no fixture showed them wrong).

`halted` was already in the schema's `Status` enum (phase 1); this phase
is what makes it reachable and reversible through the writer's upsert.
`pain-triage` (frozen, unmodified this phase) still only implements the
halt itself; rule L12 gives it sole authority over the `halted -> closed`
exit, but that skill has no acknowledgement branch to test against yet, so
`fixtures/03-session-status` closes through `session-runner`'s `done for
today` instead, to prove the upsert mechanism a real hand-off would use.
That is a scope substitution, not a claim that `session-runner` owns the
transition; see the phase-3 report for the citation.
