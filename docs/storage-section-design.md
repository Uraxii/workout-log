# The storage section of intake

**Status.** Phase 1 shipped in commit e5b3e14: `storage_platform` is a live
question, `storage.py` gates every create, and `fixtures/13-storage-refusal`
pins the refusal. Phases 2 to 4 are still design; `conventions.py` is still
the TODO stub they describe.

This is an explanation document. It says what the storage section asks, where
each answer lands, who honours it, and what happens when the athlete names a
store this build cannot write to. `docs/build-plan.md` stays the authority for
content; `docs/architecture.md` stays the authority for structure.

The order this answers, verbatim: "we need a specific section asking the user
where they want the data stored and adopt those conventions", and "Intake
question. The llm should be able to figure out how to store the data
correctly. We don't need to tell it how to do it."

## The tension, and how it resolves

The second sentence pulls against the repo. Correctness here rests on a fixed
schema, pure scripts, and 24 fixtures that replay byte for byte against
`tools/mock-notion`. A model improvising storage at write time would have no
proof behind it, and the failure would be a training log that quietly went
somewhere wrong.

The resolution is that these two things are talking about different layers,
and the five verbs already sit on the line between them.

**The data model stays deterministic and proven.** Which entities exist
(`Sets`, `Sessions`, `Exercises`, `Locations`), which fields each carries,
what type each field holds, which enum values are legal, the identity keys
(`write_key`, `session_key`, rule L8), the unit each magnitude is logged in,
and the e1RM rule in
`.claude/skills/load-adjust/scripts/read_layer.py`. None of that is the
model's to decide, in any store, ever. `schema/notion-schema.json` is the
single source and the fixtures assert it.

**The store's own conventions are the model's to figure out.** How to reach
the store, how to authenticate, how to page a list, how to stay under Notion's
three requests per second, how to discover that a database of that name is
already sitting under the parent page, and how to thread each returned data
source id back into `state["databases"]` before the next create. The model
does all of this today and no script knows about any of it. That is what "the
LLM should be able to figure out how to store the data correctly" already
describes. The storage section puts a name on it rather than inventing a new
mechanism for it.

**A store this build has no DDL for gets refused, not improvised.** See
"Refusing a store" below. Nothing is written, so nothing is lost.

Read as a table:

| Question | Decided by | Proven by |
|---|---|---|
| Which entities and fields exist | `schema/notion-schema.json` | every fixture |
| What value goes in a field | the skill scripts, pure | every fixture |
| Row identity and dedup | `rows.py`, `writer.py` | 01, 03, 09 |
| The `CREATE TABLE` text | `intake/scripts/ddl.py` | 05-first-run, 12-intake-parent |
| Create order across relations | `ddl.create_order`, from the relation graph | 05-first-run |
| Which store, and where in it | the athlete, asked | 13-storage-refusal |
| Display names of the containers | the athlete, asked on collision | 13-storage-existing |
| Auth, paging, rate limits, id threading | the model, at run time | not provable offline, by construction |
| The mapping onto an unproven store | nobody. Refused | 13-storage-refusal asserts zero writes |

## Why this is one section and not a second question table

Two questions already sit ahead of PAR-Q+ and already do this job:
`notion_parent_page_id` and `timezone`, rows 0 and 1 of
`questions.FIELD_STEPS`, each carrying `before_safety: True`. They are the
storage section with no name on it.

So the section is not new machinery. `FIELD_STEPS` rows gain a `section` key,
`ALL_IDS` derives the pre-safety block from `section == "storage"` instead of
from `before_safety`, and `before_safety` is deleted. One field replaces
another; the count of mechanisms does not go up. Building a second table
beside the first would be the second-registry smell that
`principle-redesign-from-first-principles` names, and the re-ask rule
(`questions.parse` returns `None`, cursor stays put) would have to be written
twice.

The conditional slot needed below already exists too. `parq_followup` is
marked pre-answered with `"n/a"` the moment all seven PAR-Q+ items come back
NO, and is then skipped with no spoken line. The collision question uses that
same machinery.

## The questions, in ask order

Every row below is one row of `questions.FIELD_STEPS`. `parse` is the reader
in `answer`. Returning `None` re-asks the same step and writes nothing, which
is the single re-ask rule for the whole table (ticket workout-log-481).

### 1. `storage_platform` (phase 1, new)

**Prompt.** "Where do you want your training log kept? Notion is what I can
write to today. Name anything else and I'll tell you straight away rather than
half build it."

**Parse.** `readers.platform`. Lowercases, strips, and returns the first
recognisable store word in the line. Returns `None` only for a line with no
word in it at all, so an empty line re-asks. It returns `"airtable"` for
"airtable": that is a parsed answer, not a parse failure, and it is refused
downstream with a reason. Re-asking "airtable" forever would be the wrong
failure, because the athlete answered the question correctly.

**Re-ask.** "I need the name of a place to put it. Notion is the one I can
write to today."

**Default shipped.** `notion`, named in the prompt. The question still earns
its place: it is the sentence the order asks for, the answer decides whether
any write happens at all, and no default can be inferred from anything the
athlete has said before this point.

**Lands on.** `config/athlete.storage_platform`, string.

### 2. `notion_parent_page_id` (exists, row 0 today)

Unchanged prompt, reader, re-ask and key. It moves to second because naming
the store has to come before naming a page inside it.

The key name still says `notion_`. Renaming it to `storage_parent_id` would
mean a schema change, a `hydrate.py` change, and a migration on a live
workspace, and would buy nothing until a second store exists. That is a
deliberate ceiling. Rename it in the same change that adds the second store,
not before.

**Lands on.** `config/athlete.notion_parent_page_id`, string, dashed
8-4-4-4-12.

### 3. `storage_existing` (phase 2, new, conditional)

**Fires only when** `state["storage_existing"]` is a non-empty list. The seam
is a pure function of `(line, state)` and cannot query, so the caller
discovers the collision and threads it in, exactly the way it already threads
back each returned data source id. An empty list marks the step pre-answered
`"n/a"` and it is skipped silently, so an athlete with a clean page answers
zero naming questions.

**Prompt.** "There's already a database called Sets on that page. Use it, or
should I make my own set and put a word in front of the names, like Lift
Sets?" The names in the prompt come from the collision list, not from a
hardcoded string.

**Parse.** `readers.container_choice`. Returns `"reuse"` for a line meaning
use it, or the prefix word for a line offering one. `None` otherwise.

**Re-ask.** "Use the ones that are there, or give me a word to put in front of
mine."

**Default shipped.** Reuse. `writer.database_create` already keys on
`(db name, parent)` and adopts a match, which is rule L8's query-before-create.
The question earns its place anyway because adoption is the dangerous default:
a database called `Sets` that someone else built has different columns, and
adopting it writes rows into a shape the schema never declared. Making the
athlete look at the collision once is cheaper than discovering it in her
training data.

**Lands on.** `config/athlete.storage_container_prefix`, string, empty for
reuse.

This one row covers both convention kinds it touches: whether existing
databases are reused, and what the new ones get called. Splitting it into a
standing "do you want a prefix" preference would put a knob in front of every
athlete to serve the one who has a collision.

### 4. `timezone` (exists, row 1 today)

Unchanged prompt, reader, re-ask and key. Now named as part of the section
rather than as a loose pre-safety row.

**Lands on.** `config/athlete.timezone`, IANA name.

### 5. `units` (exists, position 9 today; moves here in phase 2)

Unchanged prompt, reader, re-ask and key. It moves ahead of PAR-Q+ because it
decides what goes in `Sets.Unit` on every row, which makes it a storage
convention rather than a profile fact. Moving it costs the athlete nothing:
same one question, earlier.

**Lands on.** `config/preferences.units`, enum `lb` or `kg`.

### 6. `week_start` (phase 2, new)

**Prompt.** "Does your training week start on Monday or Sunday?"

**Parse.** `readers.week_start`. Returns `"monday"` or `"sunday"`. `None`
otherwise.

**Re-ask.** "Monday or Sunday? One or the other."

**Default shipped.** Monday, which is what ISO 8601 says and what
`date.isocalendar()` returns.

**Why it earns its place.** `Sessions.week_index` is a stored number, written
at session open, rule L18, computed today as
`date.fromisoformat(local_date).isocalendar().week` in
`.claude/skills/session-runner/scripts/rows.py:43`. For an athlete whose week
starts on Sunday, every Sunday session lands in the previous week's number.
That is wrong data, written once and kept, and no later read repairs it. The
question sits in the storage section rather than late in the profile
specifically so it is answered before session 1 can open, which means there is
never a mid-stream change of meaning for a number already on file.

**Lands on.** `config/preferences.week_start`, enum `monday` or `sunday`.

### 7. `date_order` (phase 3, new)

**Prompt.** "When you type a date like 3/4, do you mean 3 April or March 4th?"

**Parse.** `readers.date_order`. Returns `"day_first"` or `"month_first"`.
`None` otherwise.

**Re-ask.** "Day first or month first? An example is fine: tell me what 3/4
means to you."

**Default shipped.** `iso`, meaning only `YYYY-MM-DD` is accepted, which is
exactly what happens today.

**Why it earns its place, and why it waits for phase 3.** Today
`_FIX_DATE_RE` in `.claude/skills/session-runner/scripts/lifecycle.py:31`
accepts `\d{4}-\d{2}-\d{2}` and nothing else, so "fix 3/4 set 2" is simply not
understood. There is no ambiguity to settle because there is no input to be
ambiguous. Asking this question in phase 1 would be a knob with no consumer,
which `principle-experience-first` says no to. It ships in the same change
that widens that regex, so the question and the thing it decides arrive
together. Rule: the store never holds anything but ISO 8601. `hydrate.py`
compares `Start time` lexically and keys `sessions_by_date` on `Date`, so the
stored format is a correctness constraint, not a preference. This answer
governs what the athlete may type and what she reads back, never what is
written.

**Lands on.** `config/preferences.date_order`, enum `iso`, `day_first`, or
`month_first`.

## Every new config key

`writer.config_write` rejects any key `schema/notion-schema.json` does not
declare, proven the hard way in
`.nikki-agents/decisions.tsv` ("BLOCKED workout-log-mqs and
workout-log-ayf.16"). So each key below is a schema edit that must land in the
same change as the question that writes it.

The split between the two pages: `config/athlete` holds facts about the store
and this install, `config/preferences` holds how the athlete wants values
shaped. `units` and `nutrition_strictness` already sit that way.

| Key | Page | Type | Phase | Honoured by |
|---|---|---|---|---|
| `storage_platform` | `config/athlete` | string | 1 | `storage.is_proven`, gating `ddl.next_create_write` and `hydrate` |
| `notion_parent_page_id` | `config/athlete` | string | exists | `ddl.create_payload` `parent` |
| `notion_data_sources` | `config/athlete` | JSON string | exists | `hydrate.py`, every later `row-create` target |
| `timezone` | `config/athlete` | IANA name | exists | `Sessions.Timezone`, frozen at open, rules L3 and L4 |
| `storage_container_prefix` | `config/athlete` | string, may be empty | 2 | `ddl.create_payload` `title` |
| `units` | `config/preferences` | enum `lb`, `kg` | exists | `Sets.Unit`, `grammar.py`, `measures.py` |
| `week_start` | `config/preferences` | enum `monday`, `sunday` | 2 | `rows.week_index`, rule L18 |
| `date_order` | `config/preferences` | enum `iso`, `day_first`, `month_first` | 3 | `lifecycle._FIX_DATE_RE`, and date rendering in `say` |

`intake_cursor` keeps working unchanged: it is a flat index into
`questions.ALL_IDS`, so adding rows to the storage section shifts the index
and a half-finished intake resumes at the right question by construction.

## Where store-specific mapping lives

Two files hold every Notion fact in the repo today, and that does not change:

- `schema/notion-schema.json`, for property display names, Notion property
  types, enum options, and the e1RM formula expression.
- `.claude/skills/intake/scripts/ddl.py`, for the `CREATE TABLE` text, the
  type-to-column table, and the relation-graph create order.

Those two together are the Notion profile. Naming them that is the whole of
the abstraction. There is no registry, no adapter interface, and no dispatch
on platform, because there is one store and one user, and an interface with
one implementation is a layer that teaches a reader nothing. A second store
would arrive as a sibling module and a sibling profile, and the dispatch table
gets written on the day the second one exists, not before.

Phase 1 adds one small module beside them:

- `.claude/skills/intake/scripts/storage.py`, which owns one body of
  knowledge: which stores this build can write to, what the athlete is told
  when hers is not one of them, and what a container is called.

Phase 2 adds a second:

- `.claude/skills/intake/scripts/conventions.py`, which owns turning a stored
  value into the athlete's shape and back: week numbering and date reading.
  Its consumers are `rows.week_index` and `lifecycle.try_fix_backfill`.

Both are splits by domain, not by execution step, per `docs/architecture.md`
"One script per skill".

## Refusing a store

The failure mode has to be loud and early, because the thing being prevented
is a half built workspace holding a week of training data in a shape nothing
can read back.

Two gates, both at a chokepoint every write already routes through, so no
handler can forget them. Same shape as `preconditions.no_sets_while_halted`
and `bounds.reject_implausible_writes`.

**Gate 1, create time.** `ddl.next_create_write` already returns `[]` when
`state["notion_parent_page_id"]` is missing. It gains one more condition:
return `[]` unless `storage.is_proven(state["storage_platform"])`. Not one
`database-create` is emitted for an unproven store, so nothing is created
under the athlete's page.

**Gate 2, cold start.** `hydrate.py` reads `config/athlete` on turn 1 of every
cold chat. An unproven `storage_platform` raises there, so `session-runner`
cannot open a session or write a set either, not just `intake`.

**What she hears.** `storage.refusal(name)` returns one line, said in place of
the next question:

> "I can't write to Airtable yet. Notion is the only one I've been proven
> against, and I'd rather say so now than build you half a log. I've written
> down that you asked for Airtable. Say 'notion' and I'll set that up instead."

**What is written.** Exactly one thing: the config-write recording
`storage_platform`. No `database-create`, no `row-create`, no catalog seeding.
The 913-row seed never starts.

**No fallback.** There is deliberately no local file mode and no degraded
store to fall back on. A fallback store would be a second store with no proof
behind it, which is the thing this gate exists to prevent.

**How a new store gets added.** Not at run time, and not by a model
improvising mid conversation. A store becomes proven the way Notion did: a
profile file, a DDL renderer, and fixtures that replay against a mock. A model
is welcome to write all three. It writes them into the repo, offline, before
any of the athlete's data moves, and the fixtures are the thing that says it
worked. That is the honest reading of "the LLM should be able to figure out
how to store the data correctly": it figures it out once, in a reviewable
artifact, not once per write with nobody watching.

## How this is proven offline

The awkward part of the brief is that a fixture cannot replay against a store
nobody has implemented. The answer is that the fixture does not have to. What
gets proven is the refusal, and a refusal is fully observable offline.

`expected.tsv` is long form, one line per emitted write field, so a fixture
that emits nothing has a nearly empty file, and that emptiness is asserted
byte for byte. Absence is the assertion.

**Phase 1, two fixtures.**

- `fixtures/13-storage-refusal`. The transcript answers "airtable" to the
  storage question. `expected.tsv` holds one `config-write` row for
  `storage_platform`, zero `database-create` rows, zero `row-create` rows, and
  the exact refusal line as the turn's `say` row. This is the fixture that
  proves data loss cannot happen, and it proves it by asserting an empty write
  set.
- `fixtures/05-first-run` gains the new first turn answering "notion". Its
  existing four `database-create` rows must still appear in the same order.
  That is the regression guard on the live path.

**Phase 2, one more.**

- `fixtures/13-storage-existing`. The transcript seeds a found `Sets`
  database, asserts the conditional question fires with the found name in it,
  and asserts that the reuse answer emits three `database-create` rows instead
  of four while the prefix answer emits four with prefixed titles.

**Negative control, for each.** Revert the gate against the final code, not
against the pre-change code, and confirm the refusal fixture goes red with
four `database-create` rows appearing. A red proven against code that no
longer exists proves nothing. That is the standard this repo already holds
itself to; see the "negative control" row in `.nikki-agents/decisions.tsv`.

**Phase 4, only when a second store has a real user.** A round-trip probe:
write one throwaway row through the five verbs, read it back through the two
read verbs, compare. A store passes only when the value survives the trip. The
probe is generic over stores because the five verbs are, and it is provable
offline because `tools/mock-notion` is itself a store, so one fixture asserts
the probe passing against the mock and one asserts it failing against a
deliberately lossy mock. This is written down here and deliberately not built,
because a check with no second store to check is speculative.

## Build order

Sequenced so the Notion path stays shippable and the first live run against a
real workspace is not held up.

**Phase 1, shipped in e5b3e14. The question, the gate, the refusal.** One schema key
(`storage_platform` on `config/athlete`). One reader. One new module,
`storage.py`, with `is_proven` and `refusal`. One added condition in
`ddl.next_create_write`. One added check in `hydrate.py`. Two fixtures. The
section key on `FIELD_STEPS` rows, replacing `before_safety`.

An athlete who answers "notion" sees exactly one extra turn and everything
downstream is unchanged. This is the phase that can ship in a day, and it is
the one that makes the section real: from here on, storage is something she
was asked about rather than something assumed.

**Phase 2, still design. The conventions that already have consumers.** `week_start` with
its honouring point in `rows.week_index`. The conditional `storage_existing`
question with its honouring point in `ddl.create_payload`'s `title`. `units`
and `timezone` move into the section. `conventions.py` arrives. Fixtures
regenerate, including the reordered ones.

**Phase 3, still design. The convention whose consumer has to be built.** `date_order`,
landing in the same change that widens `_FIX_DATE_RE` to accept a slashed
date, plus date rendering in the seams that speak one.

**Phase 4, still design. Only on a second real store.** Round-trip probe, sibling profile,
dispatch on platform. Not before.

## What this design refuses to do

- No plugin or adapter framework for backends that have no user. That option
  was rejected explicitly and the rejection still holds; see the "storage
  portability" row in `.nikki-agents/decisions.tsv`.
- No per-property renaming. Property names are the schema's, because
  `confirm_line`, the mock writer's validator and all 24 fixtures assert them,
  and a second source of truth for them would drift. Container display names
  are renameable because they touch exactly one line,
  `ddl.create_payload`'s `title`, and every later write routes by data source
  id rather than by name.
- No non-ISO storage format for dates, ever. `hydrate.py` sorts on those
  strings.
- No silent adoption of a database this build did not create, once a collision
  is visible.

## Open questions for the main thread

These are choices I made in the reversible direction because I have no channel
to the athlete. Each is recorded in `.nikki-agents/decisions.tsv`.

1. `date_order` is deferred to phase 3 rather than asked in phase 1, because
   its only consumer today rejects non-ISO dates outright. If she wants to
   type "fix 3/4" sooner, phase 3 moves up.
2. The prefix answer is reachable only through the collision question, so an
   athlete with a clean page cannot ask for prefixed names. Adding a standing
   naming question would cost every athlete a turn to serve that case.
3. `notion_parent_page_id` keeps its Notion-specific name. Renaming costs a
   migration on a live workspace and buys nothing until a second store exists.
4. `units` moving ahead of PAR-Q+ regenerates three fixtures. If regenerating
   them is unwelcome, `units` can stay where it is and the section documents
   it as a member without moving it.
