# The trainer without scripts

> **Superseded in part.** This note was written against a Notion workspace
> holding four databases. It now holds two, `Sets` and `Sessions`, and nothing
> that is not a log: the exercise catalog is 92 package rows in
> `exercises/defaults.json`, the gym's plates are `config/preferences`, and
> per-exercise progression state is the `progression` key on
> `program/current`. An exercise is identified by its NAME; there is no slug
> and no id. Every argument below that prices seeding a catalog into Notion,
> or that reads a slug off an `Exercises` row, is describing a shape that no
> longer exists. `docs/build-plan.md` s1.5, s1.6 and s1.8 carry the
> replacement.

Design note. Explanation mode: it argues a shape and prices it. No code
changes with it. `docs/build-plan.md` stays the authority for content and
`docs/architecture.md` stays the authority for structure until a phase below
actually lands.

Written against `ee9aee2`, with `make check` green at 25 fixtures.

The order this answers, verbatim: "implementation needs to survive adding this
as a skill to the chat-GPT and Claude code webapp chats", and "We should be
able to do this without scripts, right?"

Folded in, also verbatim: "let's have the agent log in json. then translate
that to whatever structure the user needs for their logging location (notion,
obsidian, etc.)".

## The answer, and what it costs

Yes. Mostly. One rule genuinely cannot survive, and it is the one that keeps
your training log from filling with duplicate sets.

`write_key` is a sha256 hash. A model cannot compute sha256 by hand, and the
dangerous part is that it will not refuse. It will write sixteen plausible hex
characters and every one of them will be wrong, which defeats deduplication
silently and forever. That rule has to be redesigned, not translated. Section
"The write key" does it.

Everything else moves. Some of it moves and gets better. Set-line parsing and
pain-phrase matching are things a model does better than a word-matching
Python function, and both fail visibly, in a line you read.

The price, in one paragraph. Arithmetic gets less reliable, so the design
pushes the two pieces of arithmetic that matter into Notion formula columns
where nobody computes them by hand. Rounding gets less reliable, so the
design deletes unit conversion from the path that computes your next target.
Deduplication gets less reliable, and that is the residual risk this design
bounds rather than removes. Determinism goes away, so a second proof surface
has to exist beside the fixtures, it costs real money per run, and it cannot
gate a commit.

### The fact that forces it

`research/20-host-capability-matrix.md` says script execution is certain and
unconditional only in the Claude Code terminal. On claude.ai it depends on a
capability toggle you control. On ChatGPT web nobody at OpenAI has written
down whether a skill's bundled `scripts/` run at all.

The repo is already sitting in that failure. Count how many of the eighteen
lifecycle rules are cited in the seven `SKILL.md` files and their references,
against how many are cited only inside a `.py` file:

| Where the rule is written down | Rules | Which |
|---|---|---|
| In the prose, so it survives everywhere | 8 | L2, L3, L4, L7, L8, L10, L12, L17 |
| Only inside a Python file | 7 | L1, L9, L11, L14, L15, L16, L18 |
| In neither, carried by build-plan alone | 3 | L5, L6, L13 |

Reproduce it with:

	for r in L1 L2 L3 L4 L5 L6 L7 L8 L9 L10 L11 L12 L13 L14 L15 L16 L17 L18; do
	  echo "$r $(grep -rlw "$r" .claude/skills --include='*.md' | wc -l)"
	done

Seven of eighteen lifecycle rules disappear the moment Python does not run.
That includes L18, `week_index`, which is written once into a stored number
and never repaired, and L9, deduplication. This is not a hypothetical about a
host nobody uses yet. It is true of the ZIP that `make check` builds today.

## Where each rule lives after the change

Read "prose" as: stated normatively in a `SKILL.md` or a `references/` file,
in a form a model follows without running anything. Read "data" as: a file the
model reads and looks a value up in. Read "store" as: Notion computes it and
nobody else may write it.

| Rule | Lives in | Why |
|---|---|---|
| Set-line grammar, all six token families | prose | Natural-language parsing is what a model is for. Every reading is echoed in the confirm line and `fix` reverses it in one word |
| Fallback ladder, five rungs in order (s3.2) | prose | An ordered policy list, not a computation. Ordering is the whole rule |
| Grey-band tie-break order (G2) | prose | Three named sources checked in a fixed order. The reading is spoken back |
| Composed spoken numbers | prose | "one thirty five" to 135 is a language task. The script is worse at it |
| Exercise name to catalog row | data + prose | Alias table read whole. Catalog sharded by first letter. Match rules stated |
| `write_key` identity, L8 | prose + store | Redesigned as a natural key the model concatenates, then a query before every create. See below |
| `attempt` counter, L7 | prose + store | Read the highest existing `attempt` for that slot, add one. A read, not a hash |
| `Set index` scoping, L7 | prose + store | Highest `Set index` for that `(session, exercise)`, plus one. Already a read |
| Duplicate guard, L9, 120 s | prose | Already settled this way. See below |
| Idempotency on `source_message_id`, L9 | prose | Falsified for multi-row turns in phase 3. The natural key replaces it |
| e1RM | store | Already a Notion formula column. Zero model arithmetic. This is the pattern |
| `week_index`, L18 | store | Becomes a formula over `Date`. ISO week arithmetic is the worst thing to hand a model, and the result is stored once and never repaired |
| `Date` and `Timezone` freeze at open, L3, L4 | prose | Copy the device clock once. Every later day-boundary check reads the stored value and never recomputes |
| Day-boundary and resume checks, L5 | prose | Restated as "read the stored `Date`", which removes the arithmetic instead of making it reliable |
| Session lifecycle, L1, L11, L12, L13, L16 | prose | State-machine transitions with named triggers. Nothing to compute |
| Backfill window, L15, 7 days | prose | One date comparison at day granularity, and a wrong answer refuses rather than corrupts |
| Progression bump, hold, deload | prose + data | The decision is a table. The parameters are already in `library/*.json` |
| RPE cap streak (two sessions running) | data | Needs a stored counter. It has none today. See the gap below |
| Rounding a target to loadable plates | prose + data | Floor to the stored increment, in the logged unit, never converting |
| Unit conversion, lb and kg | deleted from the write path | Compute in the unit she logs and loads in. Display a mixed history as logged |
| PAR-Q+ seven questions | data | Already verbatim in `screen/references/parq-plus.md` |
| PAR-Q+ clearance decision | prose | A two-row decision table. Any YES to `pending`, all seven NO to `cleared`. Nothing to interpret |
| Pain phrase to enum, S3 | data + prose | Table already in `pain-triage/references/red-flags.md`. Precedence stated: `stop` beats `niggle` |
| Ottawa age branch, S4 | prose | Already prose by design. The reference says it is "read out loud by the agent, never checked by code" |
| `progression: manual` clearing, S5 | prose | Two named conditions, no arithmetic, and the safe failure is refusing to clear |
| Preconditions and refusals, S1, S2, S6, S7 | prose | Gates. Naming which one failed is the whole behaviour |
| Schema field names, types, enums | data | Generated field card per database. See below |
| Program templates | data | JSON transcribed verbatim into `program/current.body`. Already the design |
| Notion DDL, database creation | prose + data | Once per install, and the model already owns auth, paging, and id threading (`docs/storage-section-design.md`) |

### The alternative split, and why it loses

The obvious other answer is to keep the grammar and the arithmetic in code and
let the prose describe only the shapes, so the scripts stay the authority
everywhere and the prose is a summary a model falls back on.

Rejected, on one argument. On a host with no script execution the model acts
on the prose whatever the prose calls itself. For that to work the summary has
to be complete, and a complete summary of a rule is the rule. So the choice is
not between one authority and two, it is between one authority and two where
the second one is silently in charge on two of three hosts and nobody wrote it
to be. The seven orphan rules above are what that looks like after three
days of building.

Once the prose has to be complete, the only question left is which rules
*also* deserve code, and that is what the table answers.

Three rules from the table above deserve their own argument.

### The duplicate guard was already prose

L9's second guard says identical content in the same slot within 120 seconds
is a retype. `docs/architecture.md` records that phase 3 falsified this as a
code rule outright: identical content in the same slot is completely ordinary
training data, because the same weight for two consecutive working sets is
what training looks like. Whether a new message *is* the last one retyped is a
conversation-layer judgment with no reliable signal in `(line, state)`.

So this rule was never really in the scripts. `replay.py` gained an `@resend`
directive to stand in for the judgment once a human had made it. Moving it to
prose changes nothing except that it stops pretending to be code.

State it as: treat a repeat as a resend only when the athlete's own words say
so ("did that go through", "sorry, resend"), or when your own previous write
raised an error and you are retrying it. Never on identical content alone.
The 120 second window stays as a bound on how far back to look.

Rejected: keep an elapsed-time comparison in the prose so the rule reads the
same as build-plan.md. Rejected because it would make the model do the thing
phase 3 proved wrong, only less reliably.

### `week_index` moves into the store, and that kills a whole class

`Sessions.week_index` is computed today by
`.claude/skills/session-runner/scripts/rows.py` as
`date.fromisoformat(local_date).isocalendar().week`. It is written once at
session open and, as `docs/storage-section-design.md` says about the same
column, "That is wrong data, written once and kept, and no later read repairs
it."

ISO week numbers are the single worst arithmetic to hand a model. The rule
involves a Thursday, a year boundary that does not line up with the calendar
year, and a 53-week year. A model gets it right most of the time, which is the
bad case, because the wrong answers cluster in early January and go unnoticed.

`e1RM` already solved this exact problem in this exact repo. It is a Notion
formula column and no skill writes it. Do the same to `week_index`. The model
writes `Date`, which it only has to copy from the device clock, and Notion
computes the week from it. Nobody computes ISO weeks by hand, on any host,
ever again. It also makes the `week_start` question in
`docs/storage-section-design.md` section 6 a formula parameter instead of a
value baked into every historical row.

One thing to settle before this lands, and it is not settled here. The repo's
own DDL validator allows exactly two formula functions,
`tools/mock-notion/notion_columns.py:_FORMULA_FUNCTIONS = frozenset(("if",
"empty"))`, with a comment saying a real Notion function missing from the set
"fails loudly and gets added with its source". Whichever date function Notion
exposes for a week number has to be read off a vendor page and added there
with its URL, the way `e1RM`'s expression already cites
`developers.notion.com/reference/property-object#formula`. Naming one here
from memory would be the exact thing `research/20` refuses to do. If it turns
out Notion has no week function at all, the fallback is to store `Date` alone
and derive the week at read time in whatever is asking, which is worse for
querying and still better than a hand-computed number written once.

Rejected: ship a lookup table of date to week number. Rejected because it is
one file per year forever, and the model still has to find the row.

Rejected: have the model compute it and check its own work. Rejected because
there is nothing to check against. A wrong week number is self-consistent.

### The RPE streak has nowhere to live

`load-adjust`'s rule 4 holds a bump when RPE is at or above 9.5 for two
sessions running. `rules.py` keeps `high_rpe_streak` in a `cfg` dict, and the
schema has no column for it. `Exercises` stores `fail_count`,
`training_max`, `stage_index`, `variation_index`, `last_deload_at`, and
`deload_declined_at`, but not this.

That is a gap today, not one this design creates: the streak already dies at a
chat boundary. It matters more once the prose is the authority, because the
prose has to tell the model where to read the streak from, and there is no
answer. Fix: add `high_rpe_streak` to the `Exercises` properties. It is a
schema edit, so it is a ticket, not part of this note.

## The write key

The problem, stated plainly. Today:

	write_key  = sha256("<session_key>|<exercise_id>|<set_index>|<attempt>")[:16]
	session_key = sha256("<start>|<tz>")[:16]

A model cannot compute this. Worse, it will not say so. Asked for a hash it
produces sixteen confident hex characters, and a fake-but-unique key is the
worst possible failure: every write looks new, deduplication never fires
again, and nothing anywhere goes red.

### The replacement

Delete the hash. The key is the natural key, written out.

	session_key = "<Start time>|<Timezone>"
	write_key   = "<session_key>|<exercise_slug>|<set_index>|<attempt>"

Worked, with a real IANA zone rather than the fixtures' `UTC`:

	2026-09-01T09:00:00|America/New_York|Barbell_Squat|1|0

The separator is a pipe and not a slash on purpose. Rule L3 freezes
`Timezone` to the device IANA zone, and `America/New_York` contains a slash,
so a slash-separated key would not split back into five components. No
component of the key may contain a pipe, and none of them can: an ISO
timestamp, an IANA zone, a catalog slug, and two integers.

Four properties earn it.

**A model can produce it by concatenation.** There is no arithmetic. Every
component is something the model must already know to write the row at all:
the open session's frozen `Start time` and `Timezone` (rules L3 and L4), the
catalog slug, the set index it is about to write, and the attempt counter.

**It describes its own row, so a wrong one is checkable.** A hash is opaque by
construction. This key can be split back into five components and compared
against the properties on the row that carries it. That check is a function,
`tools/scriptless/keys.py:matches_row`, and it is the only defence against
the failure mode the natural key introduces.

**It is queryable through a connector.** Query before create becomes two
connector calls with no local state: filter `Sets` where `write_key` equals
the string, then create on no match or merge on a match. That is exactly the
upsert `writer.py` already implements, expressed in the two verbs a web host
actually has.

**It is readable in the Notion UI.** A malformed key is visible sitting in the
column next to `Load` and `Reps`, instead of being sixteen characters nobody
can evaluate.

The slug, not the display name. `Barbell_Squat`, never `Squat (Barbell)`.
`Exercises` carries both, and a rename changes `Name` while `slug` holds
still. Keying on the display name would silently fork the key space the first
time she renames a lift.

### What is lost

1. **Fixed width.** Sixteen characters becomes about fifty, and it varies.
   Costs nothing in a `rich_text` column, costs a little screen width.

2. **Opacity.** The old key leaked nothing. The new one embeds a timestamp and
   an exercise slug in a text field. In this schema that field sits in the
   same row as `Load` and `Reps`, so it leaks nothing new *there*. It does
   mean the key alone is no longer safe to paste somewhere public.

3. **A round trip per create.** A locally computed hash needed no read. A
   natural key needs a query before every create. Build-plan s3.2 budgets
   "1 create, at most 1 read, and 0 questions on the happy path", so this
   fits, but it consumes the entire read budget. Nothing else may read on the
   happy path.

4. **Twenty-five expected files change.** Every fixture asserts
   `write_key 590df2ecff4e15ca` and its siblings. They get regenerated with
   `replay.py --update`, not deleted, and they immediately prove the new key
   is per-row unique and stable across a rerun. One mechanical commit.

5. **The key is now composed, not derived.** A hash of the right inputs is
   correct by construction. A concatenation can be malformed by a model that
   pads a set index, writes `2026-09-01` where `2026-09-01T09:00:00` belongs,
   or uses the display name. `matches_row` catches it, and the eval's dedup
   case is the only thing that proves `matches_row` is being called. This is
   the residual risk of the whole design.

6. **Nothing new on the same-instant collision.** Two sessions opened at the
   identical frozen instant in the identical zone share a `session_key`, so
   they share every `write_key` under them. The sha256 version has exactly the
   same hole, because it hashes exactly the same two fields, and
   `docs/architecture.md` already names the case in its phase 3 note. The
   natural key neither worsens it nor fixes it. Rule L6 says session identity
   is the page id, so the fix, if one is ever wanted, is to put the session's
   page id in the key after the create rather than before it. Not designed
   here, because it has never happened.

### Rejected alternatives

**Ask the model to compute a short hash.** Rejected outright, and it is worth
saying why in the doc so nobody proposes it again. Models cannot compute
sha256 and do not know they cannot. The output is a plausible unique-looking
string, which passes every eyeball check and defeats deduplication forever.
A rule that fails loudly beats a rule that fails invisibly.

**Let Notion's page id be the identity, dedup on `source_message_id`.**
Rejected twice already, in this repo, with evidence. A page id does not exist
before the write (phase 3 defect 2). `source_message_id` alone assumed one row
per message, and an EMOM writes ten (phase 3 defect 3).

**Have the model pick a random UUID per set and remember it.** Rejected
because "remember it" is the thing no host guarantees. The whole point of the
key is that a cold chat with no memory recomputes the same value from the
store.

**No dedup. Let her delete duplicates.** Rejected. The failure she cannot see
is the one that matters: she types once on a flaky connection, two rows land,
and every progression read downstream is now computed over a set she never
did. Duplicate sets corrupt the trend, not just the table.

## What ships as data

One rule governs all of it. A data file a scriptless model can use must be
either small enough to read whole, or sharded on a key the model already
holds. Anything else is a script wearing a JSON hat.

By that rule the repo currently ships one file that fails badly.

### The catalog, 913 rows, 1.08 MB

`make skills` bundles `exercises/catalog.json` into the ZIP at
`session-runner/data/exercises/catalog.json`, 1,085,680 bytes. On Claude Code
`catalog.py` reads it. On a host with no script execution the model would have
to read a megabyte of JSON into context to look up one name, which it cannot
do. Most of that megabyte is `instructions` and `images`, neither of which any
runtime path touches.

Three changes.

**Cut the runtime fields.** A lookup needs `slug`, `name`, `measure`,
`equipment`, `primary_muscles`. Nothing else. That is roughly 60 bytes a row,
so about 55 KB for all 913.

**Shard on the first letter.** `exercises/index/<a-z>.tsv`, around 2 KB a
shard. The model knows the first letter of what the athlete typed, so the
lookup is one small read. Sharding on something the model already holds is
what makes this a data file rather than a search problem.

**Keep `aliases.json` whole.** 131 entries, 4.7 KB. It is the highest-value
table in the repo and it is small enough to sit in context for a whole
session. It is already the right shape.

Then the honest part. Seeding 913 rows into Notion is 913 creates, one at a
time, through a connector. On Claude Code that is a slow but real intake. On a
web chat it is not viable. Seed the 48 rows the ten templates name plus the 37
in `exercises/extra.json`, and let ladder rung 4 create the rest on demand,
which is what rung 4 is for. Those counts come from:

	python3 -c "import json,glob,re; \
	s=set(); [s.update(re.findall(r'\"exercise\": *\"([^\"]+)\"', \
	open(f).read())) for f in glob.glob('library/*.json')]; \
	print(len(s), len(json.load(open('exercises/extra.json'))))"

85 rows instead of 913 is the difference between an intake that finishes and
one that does not. The cost, stated: a rare exercise
gets a create-on-demand row with an inferred `measure` and empty
`primary_muscles`, instead of a seeded row with the catalog's metadata.

Rejected: ship `catalog.json` and tell the model to grep it. Grep is a script.
On a no-script host there is no grep.

Rejected: fetch the catalog from a URL at runtime. Rejected because the README
promises "no server, no account with anyone, no app", and because claude.ai
network egress is allowlisted and ChatGPT's is workspace policy.

### The red-flags table, 66 lines

Ships as it is. `pain-triage/references/red-flags.md` is already the exemplar:
small enough to read every time the skill fires, a two-column markdown table,
and the one behaviour that is not in the table (`stop` beats `niggle` in the
same line) is stated in a sentence above it.

One deliberate change in reading. `pain_triage.classify()` scans for exact
words. A model matches meaning, so "my knee popped on the third rep" and
"something gave in my back" both land on `stop` without either phrase being in
the table. That is an upgrade, and it is safe because the failure direction is
conservative: over-flagging `stop` halts a session, and a halted session is
recoverable in one acknowledgement.

So the prose must say the table is a floor and not a ceiling. Every row in it
must map as written. The model may map more.

### The program templates, ten JSON files

Two access patterns, so two shapes.

Picking needs a comparison across all ten. Add `library/index.md`, one row per
template: id, name, days per week, equipment, goal fit, `progression_unit`,
`dose`. About thirty lines, read at pick time.

Running needs one template in full, and the design already does the right
thing: `program-design` copies the chosen JSON verbatim into
`program/current.body`. The model transcribes it, it does not compute over it.

One computation hides in there. Blocks carry
`start: {"kind": "retest_pct", "test": "5rm", "pct": 0.85}`. State it in prose
as "85% of your tested 5RM, floored to a weight your gym can load", which is
one multiply and one floor, and it is spoken to the athlete before she lifts
it. Visible arithmetic is acceptable arithmetic.

### The schema itself, 153 lines

It is readable, and that is not the same as being the right thing to read. The
`Sets` entry carries a 700-character explanatory note about the e1RM formula
and a 300-character note about why `Set` is the title. Those exist for us.

Keep `schema/notion-schema.json` as the single source of truth, and generate a
**field card** per database into each skill's `references/`. A field card is
the property names, the types, the enum values, the defaults, which properties
are formulas that must never be written, and the `measure` kind to magnitude
column mapping. Around forty lines. It is what the model reads immediately
before a `row-create`.

Generated, never hand-written, so it cannot drift. That is
`tools/scriptless/cards.py`.

Rejected: hand-write the field cards once. Rejected because a hand-written
copy of a schema is a second schema, and the second one is always the stale
one.

## Proving it when the authority is prose

The 25 fixtures replay transcripts through pure Python seams with no model in
the loop. They prove the scripts. They cannot prove the prose, and no amount
of adding fixtures changes that, because there is no model in the loop to be
wrong.

`docs/architecture.md` already admits the boundary, in "What the say rows
prove, and what they do not": "Mandatory wording that lives only in SKILL.md
prose and never in a script return value is unasserted for the same
reason." That unasserted
region is about to become the whole system on two of three hosts.

### The insight that makes this cheap

`replay.py` already turns (transcript, seams) into a TSV of writes and reads.
The assertion machinery, the emission ordering, the byte-for-byte compare, all
of it exists and is trusted.

An eval case changes the producer and keeps the machinery. Run a real model
with the skill folder loaded, expose `tools/mock-notion`'s writer as tools
instead of importing it, and the model's tool calls land in the same TSV.
Same file format, same compare, different thing being proved.

### What a case looks like

	evals/<NN-name>/
	  prompt.txt     one organic user line per turn, no @directives
	  world.json     seeded store rows, plus the frozen clock and zone
	  case.json      the three assertion kinds below

Three assertion kinds, because a model's output has three different kinds of
determinism.

**Exact.** The structural write rows, in the `verb, target, field, value`
shape `fixtures/*/expected.tsv` already uses. Which database, which
properties, which enum values, the `write_key` string, the `Set index`
sequence, the row count. These are reproducible and a variation is a bug.

**Forbidden.** `(verb, target)` pairs that must not appear at all. A halted
session asserts zero `row-create Sets`. A retype asserts zero second row.
These are the safety assertions and they are the reason the suite exists.

**Judged.** The spoken lines, scored by a second model against three to five
criteria. "Does the confirm line name the exercise, the set number, the
magnitudes, and a next target." "Does the refusal name which precondition
failed." Never byte for byte, because the whole point is that the model
composes the sentence.

### The suite

Eight cases, not twenty-five, chosen to cover the classes where prose can
break in a way code could not:

1. One logged set, happy path, cold chat.
2. A retype, asserting zero second row (dedup).
3. A connector error on the create, then a retry, asserting zero second row.
4. A set attempted on a halted session, asserting zero `Sets` writes (S2, L12).
5. A grey-band `20x8` with no carry-forward, asserting the stated reading (G2).
6. PAR-Q+ with all seven NO, asserting `clearance: cleared`.
7. PAR-Q+ with one YES, asserting `clearance: pending` and no session opens.
8. A progression bump with a target rounded to loadable plates.

Cases 2, 3, 4, 6, and 7 are the safety set.

### How it runs, and what it costs

`make check` does not change. It stays offline, deterministic, free, and it
gates every commit. It proves the scripts and the data files, and it is still
the only thing in the repo that catches a bad edit in under a second.

A new `make eval` target runs the model suite. Three samples per case, because
one sample proves nothing about a stochastic system. It gates a release, not a
commit.

Cost, honestly. Eight cases at three samples is 24 model runs, each a few
turns with a skill folder of roughly 10,000 tokens in context. Call it low
tens of thousands of tokens a run and single-digit dollars for the full suite
on a mid-tier model. Wall clock is dominated by latency, so minutes rather
than hours. That is cheap weekly and cheap per release, and it is far too
expensive and too slow to sit in a commit loop. Say that out loud rather than
discovering it.

Thresholds. A safety case needs 3 of 3, and below that blocks the release.
Any other case needs 2 of 3, and below that files a bug.

### Rejected alternatives

**Make the eval the only proof and delete the fixtures.** Rejected. A
nondeterministic proof cannot bisect a regression, and it costs money to run,
so it will be run rarely and by then five things changed. The fixtures are the
fast net and they stay.

**Assert the model's prose byte for byte.** Rejected. It guarantees a red
suite on the next model update, and a suite that is red for reasons nobody
believes gets switched off inside a week.

**Run the eval on all three hosts.** Rejected as unbuildable. The eval runs
where the harness runs. It proves the prose is followable by a model, which is
the thing in doubt. It cannot prove claude.ai's container behaves, and
pretending otherwise would be the worst kind of green.

## What the scripts are for afterwards

Three jobs, none of them "the authority".

**The accelerator.** On Claude Code, calling `log_set.py` is faster, cheaper,
and exactly reproducible. The prose says so explicitly: if you can run
`scripts/`, run it and use its answer; if you cannot, follow the rules below.
Both paths must land the same writes. That sentence is the contract.

**The executable spec.** The scripts are how the prose gets tested at all. The
25 fixtures stay green and stay gating every commit. Nothing about this design
makes them less true, and the path they prove is the owner's own host.

**The build tools.** `tools/catalog/build.py`, `tools/package/*`,
`tools/schema/check_e1rm.py`, `library/check.py` run on a developer machine at
build time and never touch an athlete's host. "No scripts" says nothing about
these. Worth stating, because "scriptless" is easy to over-read.

### Keeping prose and script from drifting

The precedent is already in the repo. `tools/intake/check_questions_docs.py`
fails `make check` when the intake questions and their doc disagree.
`screen.py` goes further and parses the seven PAR-Q+ questions out of
`references/parq-plus.md`, so the reference file is not a copy of the rule, it
is the rule.

Generalise that into `tools/scriptless/drift.py`, wired into `make check`,
with three checks.

**Rule coverage.** Every rule id `docs/build-plan.md` defines must be cited in
at least one prose file under `.claude/skills/`. This check goes red today on
seven rules, which is the point of writing it.

**Table agreement.** The red-flags phrase table is parsed out of the markdown
and compared against `pain_triage.py`'s word sets, in the direction that must
hold: every table row honoured by the script. The reverse direction is
deliberately not asserted, because the table is a floor.

**Card currency.** The generated field cards match what `cards.py` renders
from `schema/notion-schema.json` right now.

Where a rule is a table, generate the markdown from the one source and let the
checker assert it is current. Drift becomes impossible instead of detected.
Where a rule is genuinely prose (the ladder order, the grey-band tie-break),
only coverage can be checked, and coverage is the check that catches the
failure mode the host matrix actually named.

This is the lesson going into structure rather than into a paragraph asking
people to remember. A rule that lives only in a `.py` file should fail the
build, not wait to be noticed missing on a host nobody tested.

Rejected: a review checklist item saying "put the rule in the prose too".
Rejected because that is how the current seven got missed.

## Worked example: one set, no script execution

Host: claude.ai with code execution off, or ChatGPT web. Nothing in `scripts/`
runs. The athlete types:

	185x5

### What the model reads

Already in context from the skill load: `trainer-core/SKILL.md` (the gate) and
`session-runner/SKILL.md`.

Read this turn, because it is turn 1 of a cold chat:

- `session-runner/references/sets-card.md`, the generated field card.
- `config_read("config/athlete")` for `timezone`, `units`, and
  `notion_data_sources`.
- `row-query Sessions where Status = open`.
- `row-query Sets where Session = <that page id>`, for the highest `Set index`
  and `attempt` per exercise (rule L7).
- `config_read("program/current")` for the program body and the cursor.

State recovered: an open session with `Date 2026-09-01`,
`Start time 2026-09-01T09:00:00`, `Timezone UTC`, `units lb`, the program
cursor's lead block is `Barbell_Squat`, no sets logged yet.

### The JSON it produces

One canonical record per set, store-independent. This is the contract the
owner asked for, and it is the natural output of a scriptless host, because
the model has to hold the parsed set somewhere before it maps it onto a store.

	{
	  "record": "set",
	  "schema_version": "2.1",
	  "session_key": "2026-09-01T09:00:00|UTC",
	  "write_key": "2026-09-01T09:00:00|UTC|Barbell_Squat|1|0",
	  "exercise_slug": "Barbell_Squat",
	  "set_index": 1,
	  "attempt": 0,
	  "measure": "weight_reps",
	  "set_type": "working",
	  "load": 185,
	  "unit": "lb",
	  "load_kind": "absolute",
	  "reps": 5,
	  "side": "both",
	  "pain_flag": "none",
	  "timestamp": "2026-09-01T09:00:00+00:00",
	  "source_message_id": "msg-1",
	  "confirm_line": "Squat (Barbell) set 1, 185 lb x 5. Set 2 at 185 lb."
	}

Note what is absent. No `week_index` and no `e1RM`, because Notion computes
both. No nulls: a `weight_reps` set carries no `duration_s` key at all, so
there is nothing to accidentally write as zero.

### What it writes to Notion

Query first, always:

	row-query Sets where write_key = "2026-09-01T09:00:00|UTC|Barbell_Squat|1|0"
	  -> []

Then one create, mapping the JSON through the field card onto Notion display
names:

	row-create Sets
	  Set               Squat (Barbell) set 1, 185 lb x 5
	  Session           <open session page id>
	  Exercise          <Barbell_Squat catalog page id>
	  Set index         1
	  Set type          working
	  Timestamp         2026-09-01T09:00:00+00:00
	  Side              both
	  Load              185
	  Unit              lb
	  load_kind         absolute
	  Reps              5
	  attempt           0
	  write_key         2026-09-01T09:00:00|UTC|Barbell_Squat|1|0
	  source_message_id msg-1
	  Pain flag         none
	  confirm_line      Squat (Barbell) set 1, 185 lb x 5. Set 2 at 185 lb.

Then it says the `confirm_line`. That is 1 read and 1 create, exactly the s3.2
budget.

The mapping from the JSON to those property names is one prose section per
store, in `session-runner/references/`. Notion is the only one written today.
Obsidian would be the same JSON rendered as a table row in a daily note, and
it needs the same query-before-create discipline against the same
`write_key`.

### The retype

She is not sure it went through and types `185x5` again. Three branches, and
the model has to pick.

**A, the ordinary case.** It is a second working set. `set_index` 2, key
`...|Barbell_Squat|2|0`, new row. Correct, because two sets at the same weight
is what a working set looks like.

**B, an explicit resend.** She says "did that go through" or "sorry, resend".
Recompute the same key `...|Barbell_Squat|1|0`, the query finds the row,
compare the fields, nothing changed, write nothing. Say "already logged: Squat
set 1, 185 lb x 5."

**C, a retry after an error.** The create timed out and the model does not
know whether it landed. Same key, the query answers it, no second row. This is
the case the natural key genuinely buys, and it is the one a hash bought too.

A against B is the conversation-layer judgment `docs/architecture.md` already
established, and it is only available to the model. Be honest about the
failure: a model that picks B when the truth is A loses a real set, and the
loss is silent in the data.

The bound is the confirm line. Branch B says "already logged", which reads
nothing like "set 2 logged", so she sees the wrong branch in the same breath
and one re-log recovers it. The prose rule is therefore: never take branch B
on identical content alone. Take it on her words, or on your own failed write.

## What gets worse, and by how much

| What degrades | Why | How the design bounds it | Residual |
|---|---|---|---|
| Arithmetic | A model does mental maths and cannot tell when it is wrong | e1RM and `week_index` become store formulas, so nobody computes them. What is left is one add, one percentage, one floor, each spoken to the athlete before she acts on it | Low. A wrong next target costs one set and is visible in the confirm line |
| Unit conversion | Multiplying by 0.45359237 compounds silently | Deleted from the write path. Compute and round in the unit she logs and loads in. Show a mixed history as logged | Low, at the cost of a mixed lb and kg history no longer ranking on one scale |
| Rounding to plates | Needs the gym's increment | The increment is data on `Locations` and `Exercises`. The rule is floor only, so there is no direction to get wrong and no tie to break | Low. Worst case, a target one increment light |
| Dedup | No hash. Identity is a string the model composes, and one malformed component makes a row invisible to the next query | `matches_row` checks a key against its own row. Query before every create. Eval cases 2 and 3 are the only proof it happens | **Medium, and the largest residual** |
| Date maths | ISO weeks, day boundaries, elapsed time | `week_index` becomes a formula. Every day-boundary check is restated as "read the stored `Date`, never recompute". Elapsed time survives only in the 3 hour resume ask, where being wrong costs a redundant question | Low, after the formula move |
| Grammar | A model parses instead of a tested parser | Every reading is echoed in the confirm line and `fix` reverses it in one word. A model is better on the messy inputs and worse on adversarial ones, and the athlete is not adversarial | Low, and self-correcting |
| Catalog coverage | 913 creates through a connector is not viable on a web host | Seed the 85 rows the library and extras name. Rung 4 creates the rest on demand | Medium. A rare lift gets a thinner catalog row |
| Determinism | The same input no longer produces the same writes byte for byte | Two proofs instead of one. Fixtures stay exact, offline, and per commit. Evals are predicate and judged, per release | **The largest developer cost.** A prose regression cannot be bisected |

**The single worst one, for the athlete: deduplication.** It is the only
degradation that is silent, permanent, and corrupts data rather than annoying
someone. Every other row on that table produces a wrong number she can see, or
a question she did not need. A malformed `write_key` produces a log that looks
right and is not.

**The single worst one, for whoever maintains this: determinism.** A code
regression bisects in minutes. A prose regression shows up as a case going
from 3 of 3 to 2 of 3, three commits after the edit that caused it.

Both are bounded, neither is removed. That is the honest price of the answer
being yes.

## The phased path

The rule for the ordering: nothing here delays the first live Notion run on
Claude Code, and nothing throws away a fixture.

**Phase 1. Do the live run.** The build works on Claude Code with scripts
today, `make check` is green at 25 fixtures, and the ZIP builds. Nothing in
this note has to land first. Go and log a real session.

**Phase 2. The natural key.** One change to how `rows.py` builds `write_key`,
one `replay.py --update` sweep across the 25 fixtures, one paragraph in
`docs/architecture.md`. Half a day.

This is the one phase with an ordering constraint, so here is the trade with
numbers rather than a recommendation. Landing it *before* the first install
costs half a day. Landing it *after* means every set logged in between carries
a sha256 key, and you get either a dual-format read path forever, or a one-off
backfill over every `Sets` row. If the live run is tonight, run it and take
the backfill. If it is this weekend, do phase 2 first.

**Phase 3. Two formula columns.** `week_index` becomes a Notion formula over
`Date`, the way `e1RM` already is. `high_rpe_streak` gets a column on
`Exercises`. Both are schema edits. Phase 3 has a prerequisite the others do
not: find Notion's week function on a vendor page, or find out it has none.
Do that first, because a negative answer changes the phase. Before install this is an hour. After
install it is one formula column added by hand in the Notion UI plus a
backfill of existing rows, which is small but not free.

**Phase 4. The prose lift.** Per skill, move the normative rules out of script
docstrings and `docs/build-plan.md` into `SKILL.md` and `references/`. Add the
"run the script if you can, otherwise follow this" preamble. Start with the
seven rules that live nowhere else: L1, L9, L11, L14, L15, L16, L18. No
behaviour changes on Claude Code, and the fixtures staying green is exactly
how you know the lift changed nothing.

**Phase 5. Reshape the data.** Cut the catalog index to the runtime fields and
shard it by first letter. Write `library/index.md`. Generate the field cards.
Cut the seed set to what the library names. This is the phase that makes the
ZIP usable on a web host, and it is the one that shrinks a 1.08 MB file to
about 55 KB.

**Phase 6. The eval harness.** `evals/`, the runner that exposes
`tools/mock-notion` as tools, the eight cases, `make eval`. This is what makes
phase 4 provable, so it should not lag phase 4 by much. The gap is bounded
though: phase 4 is provably behaviour-neutral on Claude Code, and the web
hosts have no users yet.

**Phase 7. The drift check.** `tools/scriptless/drift.py`, wired into
`make check`. Last, because it needs the phase 4 and phase 5 artifacts to
check against. Before anyone else edits a skill, because that is when drift
starts.

**Phase 8, conditional. The ChatGPT plugin wrapper.** `.codex-plugin/plugin.json`.
Blocked on the host matrix's open question 1, whether chatgpt.com is a real
target at all or whether Codex CLI is enough. If it is Codex, `.agents/skills`
already covers it and this phase does not exist. Do not build it on
speculation.

Note what is *not* in the list. Host matrix unknown 1, whether ChatGPT web
runs a skill's bundled `scripts/`, does not appear in any phase. That is the
point of the whole exercise: after phase 4 the answer no longer changes what
gets built. It only changes how fast the thing runs.

## Stubs

Contract sketch, no logic, in `tools/scriptless/`:

- `keys.py`, the natural key: build, parse, and check a key against its row.
- `cards.py`, generate a field card per database from the schema.
- `drift.py`, the three drift checks, exiting non-zero like
  `tools/intake/check_questions_docs.py`.
- `evalcase.py`, the eval case and result shapes and the runner signature.

## Open questions

Recorded here and in `.nikki-agents/decisions.tsv`, because this note has no
channel to ask.

1. **Is chatgpt.com a real target, or is Codex CLI enough?** Unchanged from
   the host matrix. It decides whether phase 8 exists. Everything else in this
   note is the same either way.

2. **Live run tonight, or phase 2 first?** The write key trade above. Half a
   day now against a backfill later. Your call, and either answer is fine.

3. **Does the mixed lb and kg history matter to you?** The design deletes unit
   conversion from the target path, which means a history with both units no
   longer ranks on one scale at read time. If you never mix units this costs
   nothing. If you train at two gyms with different plates it costs a "best
   ever" answer.

4. **How many catalog rows do you actually want seeded?** The note assumes
   85, being the 48 the ten templates name plus the 37 in `extra.json`.
   Seeding more is slower at intake and better on the first rare lift. There
   is no right answer without knowing what you lift.

5. **Who runs `make eval`, and how often?** It costs money, so it needs an
   owner and a cadence. Per release is the assumption. Weekly is also
   defensible.

6. **Should `write_key` carry a schema version?** Not designed in above,
   because it would make every existing key wrong for a second time on the
   next schema change. Worth deciding once, before there is live data, rather
   than twice.
