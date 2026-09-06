# Progression by guidance

In plain words: today the app decides whether to add weight to a lift by
running Python arithmetic, and that arithmetic forgets everything the moment a
chat ends. This note says how to replace it with written instructions the
coach follows, what the instructions actually say word for word, what gets
deleted, and the one automated check that should survive so a wrong weight
cannot be written in silence.

Design note. Explanation mode: it argues a shape and prices it. No code
changes with it. `docs/build-plan.md` stays the authority for content and
`docs/architecture.md` for structure until an increment below actually lands.

Written against `master` at `9dc5ed8`. `make check` was not run: two other
agents were live in this checkout. Every claim below comes from reading the
files and from greps, both cited inline.

The order this answers, verbatim: "Keep in mind we should rely on agentic
reasoning where we can." and "No need to program an algorithm for when to
increase weight. Guidence to the agent should be enough."

---

## The answer in one paragraph

Yes, and the repo already argued for it: `docs/scriptless-design.md` classes
"Progression bump, hold, deload" as **prose + data** and says the parameters
"are already in `library/*.json`". So this is not a new direction, it is the
direction that note picked and never finished. The shape: delete the turn
grammar and the arithmetic in `.claude/skills/load-adjust/scripts/`, keep the
program's own `progression` object as the data the coach reads, and put a
five-row decision table in `SKILL.md` that names every `advance_when.kind` the
library actually uses. One deterministic check survives, rewritten in place at
`tools/replay/check_replay.py`: it never decides anything, it only asserts
that a written `next_target` has the right shape, the right unit, and moved by
the size the program itself declared.

**The one thing that is not free.** Deleting the Python deletes the two
fixtures that prove progression (`fixtures/06-progression`,
`fixtures/08-progression-refusal`), because `tools/mock-notion/seams.py:43`
routes `@skill load-adjust` straight into `load_adjust.adjust_turn`. Nothing
else replays a transcript. So the deletion is blocked on the eval harness that
`docs/scriptless-design.md` already scoped and priced. The prose can land
first and land alone; the deletion cannot.

---

## What this note is NOT deciding

- It does not touch the Python in the other six skills. A prior session
  investigated that and recommended against it, and the reason still holds:
  `tools/mock-notion/seams.py:17-34` imports six seam modules by name, so
  deleting them breaks 26 fixtures at import time.
- It does not redesign `agent/progression-state`'s field list, the storage
  split in `AGENTS.md`, or the two write verbs.
- It does not decide whether `session-runner` should call `load-adjust` or
  merge with it. That is ticket `workout-log-rb0` and it stays open either
  way.
- It does not build the eval harness. It states that the deletion depends on
  one, and points at `docs/scriptless-design.md` "Proving it when the
  authority is prose" for the shape.
- It writes no implementation code. The drafted `SKILL.md` prose below is the
  deliverable; the stub signatures in "The check that survives" are
  signatures, not a module.

---

## What the coach reads at the moment it decides

Four reads, all existing verbs, in this order. "The agent looks at the
history" is not an answer, so here is the whole input.

**1. `config_read("config/limits")`, key `progression`.** If the value is
`manual`, stop. Log the line, say progression is manual, evaluate nothing.
This is rule S5's hard stop and it comes first because every other read is
wasted if it fires. Today `load_adjust.py:131-133` reads exactly this.

**2. `config_read("program/current")`, key `body`.** Parse the JSON. Find
today's node through the cursor, then the block for this exercise. Read from
that block:

| Read | Where it lives | What it decides |
|---|---|---|
| `progression.axis` | block | which field a decision writes: `weight` writes `next_target`, `level` writes `stage_index`, `variation` writes `variation_index`, `reps` writes the prescription |
| `progression.advance_when` | block | the one condition that earns an advance |
| `progression.increment`, `increment_unit` | block | the exact size of one step |
| `progression.on_miss`, `after_misses` | block | what a miss does, and after how many |
| `progression.deload_pct` | block | how far a deload drops |
| `progression.reset` | block | where a stage ladder restarts when it runs out |
| `rep_range` or `reps` | block, or the active `stages[stage_index]` entry | the window the sets are judged against |
| `load_pct` | block or `sequence` step | the fraction of `training_max` this set loads to |

A block with no `progression` object never advances by itself. Say so and
write nothing. `docs/program-format.md` "Block" already states this; the
guidance restates it because the guidance has to be complete.

**3. `config_read("agent/progression-state")`, key `progression`.** JSON,
`{exercise name: {field: value}}`. Read this exercise's record:
`next_target`, `training_max`, `fail_count`, `stage_index`,
`variation_index`, `last_deload_at`, `deload_declined_at`. This is where the
counters that cannot be re-derived live, and it is the page that survives a
chat boundary.

**4. `row_query("Sets", {"Exercise": <name>})`.** Keep **today's session's
rows for this exercise, plus the one previous session's rows for this
exercise**, ordered by `Timestamp`. Per row, read `Reps`, `Load`, `Unit`,
`load_kind`, `RPE`, `is_amrap`, `level`, `Session`.

Two sessions, not three, not the whole history. The reason is worth stating
because it is what makes prose viable at all: **every rule in this repo that
needs history longer than one session reads a stored counter instead.**
`fail_count`, `stage_index` and `deload_declined_at` are on the page. The only
rule that genuinely needs a second session is the RPE cap, and it needs
exactly two. `.nikki-agents/replay-engine-scope.md` puts the same fear plainly:
"A model can walk five rows carrying four numbers. A model cannot walk two
hundred, and it must never be asked to." Two sessions is inside that bound by
a wide margin.

One rule needs a longer look and gets it for free from the log rather than
from a counter. `sessions_at_stage` (Otago at 6, `bwf-rr` at 6,
`kettlebell-wiki` at 4) is answered by counting the distinct `Session` values
in `Sets` for this exercise whose `level` equals the current level.
`schema/notion-schema.json` declares `Sets.level` as a number, so the count is
a filter, not a fold. No new field, no ordering, no accumulator.

---

## Where the guidance lives

**One place: `.claude/skills/load-adjust/SKILL.md`.** No new JSON file, no
`references/progression-rules.json`, no second table.

The owner offered a `.json` reference file, and I am declining it. Here is the
reason rather than a preference. The parameters are already data and already
in the coach's hands: `library/*.json` carries every `progression` object, and
`program-design` copies the chosen template verbatim into
`program/current.body`. A second file restating `advance_when.kind` would be a
second enumeration of a closed set that `schema/program-schema.json` already
defines, and `principle-redesign-from-first-principles` names that exactly:
"Second registry, manifest, or config holding the same kind of thing as the
first." The stale copy always wins arguments it should lose.

What is left after the parameters are excluded is a five-row decision table
and about four short paragraphs. That is smaller than the file it would live
in, and it belongs in the file the coach is already reading when it decides.

Two supporting edits, both deletions of wrong text rather than new text:

- `docs/program-format.md` "Progression rule" stays as it is. It is
  reference-mode description of a data shape, the coach reads the data not the
  doc, and it is already correct.
- `.claude/skills/load-adjust/SKILL.md` "Turn 1, from cold" and
  `.claude/skills/program-design/SKILL.md` both tell the coach the
  `progression` key rides on `config-read("program/current")`. The code writes
  it to `agent/progression-state` (`program_page.py:31`). Both lines are wrong
  today and both must be corrected in the first increment, before anything is
  deleted. A model that follows the current docs reads an empty key and says
  "Noted."

---

## The guidance, drafted

Paste-ready. This replaces the sections "Small bumps are automatic, deloads
and -10% drops ask first", "Weight, level, or variation: one engine, three
targets", and "Turn 1, from cold" in
`.claude/skills/load-adjust/SKILL.md`. Everything else in that file stays: the
off switch, the assist-direction rule, the read-time layer, the HRT branch,
and the Never list are all still right and none of them are arithmetic.

### Deciding the next load

Read four things before you decide anything.

1. `config-read("config/limits")`. If `progression` is `manual`, stop here.
   Log the line, say progression is manual, and decide nothing.
2. `config-read("program/current")`. Parse `body`. Find this exercise's block
   in today's node. Its `progression` object is the rule. If the block has no
   `progression` object, this exercise never advances by itself: say so and
   write nothing.
3. `config-read("agent/progression-state")`. Parse `progression`. This
   exercise's record holds `next_target`, `training_max`, `fail_count`,
   `stage_index`, `variation_index`, `last_deload_at` and
   `deload_declined_at`.
4. `row-query("Sets", {"Exercise": <name>})`. Use today's session's rows for
   this exercise and the previous session's rows for this exercise. Ignore
   everything older. The counters in step 3 already carry it.

Then apply the one style the rule names. The `advance_when.kind` field picks
the style and there are five kinds. A block whose `kind` you do not recognise
is a program you must not guess at: say the rule is one you cannot apply, and
write nothing.

#### Style A: fixed increment (`all_prescribed_reps`, `top_of_rep_range`)

Used by `bbr`, `gzclp`, `nsuns-lp`, `phul`, `ppl-metallicadpa`.

The set window is `rep_range` if the block has one, otherwise the fixed
`reps`. For `all_prescribed_reps` the window's top and bottom are both `reps`.

Judge today's sets for this exercise against the window:

- **Every set at or above the top of the window.** Advance one step. The new
  target is `next_target` plus `increment`, in `increment_unit`. Write it to
  the field `axis` names, and set `fail_count` to 0.
- **At least one set inside the window, none of them below the bottom.**
  Hold. Say the current target again. Write nothing.
- **Every set below the bottom of the window.** A miss. Add 1 to
  `fail_count` and write it. Then read `after_misses` (1 if the block does not
  say). If `fail_count` is below it, hold and say so, and stop here.
  Otherwise apply `on_miss` from the next section.

Never advance off a session with no sets in it. An empty session is neither a
success nor a miss: say there is nothing to adjust and write nothing.

Worked example, `gzclp` T1 squat, `increment: 10`, `increment_unit: lb`,
`reps: 5`, `next_target: "185 lb"`. Today's sets are `185x5, 185x5, 185x5`.
Every set hit 5. New target is 195 lb. Write
`{"Squat (Barbell)": {"next_target": "195 lb", "fail_count": 0}}` and say
"Squat: all five sets, bumping to 195 lb next session."

#### Style B: training-max percentage wave (`amrap_at_least`)

Used by `nsuns-lp`, and by `gzclp`'s T3 blocks at 25 reps.

Every set in this block is prescribed as `load_pct` of `training_max`, not as
an absolute weight. The last set carries `amrap_last` and is the only set that
decides anything.

- **The AMRAP set hit at least `advance_when.reps`.** Advance the training
  max, not the target: new `training_max` is the old one plus `increment`, in
  `increment_unit`. Write `training_max` and set `fail_count` to 0. Do not
  write `next_target`; every set's load is recomputed from `training_max`
  times `load_pct` at the next session.
- **The AMRAP set fell short.** Apply `on_miss`. `nsuns-lp` says `hold`
  everywhere, so hold and say the training max is unchanged.

The per-set load you speak to the athlete is `training_max` times `load_pct`,
rounded down to a weight her gym can load, in the unit she logs in. Say the
number out loud before she lifts it. Never round in kilograms and report in
pounds; convert first, round second.

Worked example, `nsuns-lp` bench T1, `training_max: 200 lb`, today's AMRAP set
`170x5`, `advance_when: {"kind": "amrap_at_least", "reps": 3}`,
`increment: 5`. Five is at least three. New training max is 205 lb. Write
`{"Bench Press (Barbell)": {"training_max": 205, "fail_count": 0}}` and say
"Bench: 5 reps on the AMRAP, training max up to 205 lb."

#### Style C: the two remaining kinds, in short

- **`sessions_at_stage`** (`otago` at 6, `bwf-rr` at 6, `kettlebell-wiki` at
  4). Count the distinct sessions in `Sets` for this exercise whose `level`
  equals the current `stage_index`. When that count reaches
  `advance_when.count`, add 1 to `stage_index` and write it. The load never
  moves on this kind; `axis` is `level`.
- **`user_says_easy`** (`easy-strength`). Ask "did that feel easy?" after the
  block, and only for a block carrying this kind. On yes, advance by
  `increment` on the `axis` the block names, which for `easy-strength` is
  `reps`. On no, or on no answer, hold. Never ask this question for a block
  carrying any other kind.

#### What a miss does (`on_miss`)

Read after `fail_count` has reached `after_misses`.

- **`hold`.** Stay put. Say the target is unchanged. Write only `fail_count`.
- **`next_stage`.** Add 1 to `stage_index` and write it, set `fail_count` to
  0, and leave the load alone. This is GZCLP's cheap intermediate step: the
  set and rep scheme changes, the bar does not. If the block has no stage left
  after this one, apply `reset` instead: `retest_pct` means the target becomes
  `pct` of a fresh tested max at `test`, and `load_delta` means the target
  drops by `value` in `unit`. Either way `stage_index` goes back to
  `reset.stage`. Ask the athlete for the retest before writing a
  `retest_pct` result; you cannot invent a tested max.
- **`deload`.** Ask first, always. Say the exact drop and the exact resulting
  number, and wait for a plain yes or no on the very next turn. On yes, write
  the new target, write `last_deload_at` as today's date, and set `fail_count`
  to 0. On no, write `deload_declined_at` as today's date and hold. Do not ask
  again until misses have piled up a fresh full `after_misses` streak past the
  one that was declined.

Never write a deload without an explicit yes on the very next turn. A deload
that lands on a "maybe" or on silence is a load the athlete did not choose.

#### The hold clause every style shares: RPE

RPE is accepted when the athlete types it and never prompted for. If she
reported RPE 9.5 or higher for this exercise in **both** today's session and
the one before it, hold even at the top of the window, and say why. One hard
session never blocks an advance. A session that reports no RPE at all breaks
the run, because RPE is optional and this cap is a backstop rather than the
operating point.

Read this off the two sessions you already have in hand. There is no stored
streak counter and you must not invent one: `agent/progression-state` carries
no field for it, so a number you write there will be rejected.

#### Assistance moves the other way

`load_kind` is `assist` when the number is help subtracted from bodyweight. An
advance there *lowers* the stored number, because less assistance is a harder
set, and a deload *raises* it. Never describe a falling assist number as a
decline or a rising one as progress. Say "less assist", not "up".

#### What you write, and nothing else

One `config-write` to `agent/progression-state`, key `progression`, carrying
the whole `{exercise name: {field: value}}` map with your change merged in.
Never drop the other exercises' records; read the map, change one record,
write the map back.

Only these seven field names may appear inside a record: `training_max`,
`next_target`, `stage_index`, `variation_index`, `fail_count`,
`last_deload_at`, `deload_declined_at`. A field name outside that list is a
field the page does not carry, and writing one loses the value silently.

`next_target` is text and always carries its unit: `"195 lb"`, never `195`.
`training_max`, `stage_index`, `variation_index` and `fail_count` are plain
numbers. `last_deload_at` and `deload_declined_at` are dates.

#### Say the decision, never write it silently

Every decision gets one spoken line naming the exercise, what happened, and
the resulting number with its unit. A decision you cannot make is spoken too:
if the block has no rule, or `next_target` is missing, or `fail_count` is
missing, say which one is missing and what you did about it. Writing nothing
and saying "Noted." is the worst outcome available, because the athlete walks
away believing the set landed.

If `fail_count` is missing from the record, do not assume zero. Count the
sessions for this exercise where every set fell below the bottom of the window
since the last advance, deload, or stage change, say that you recounted it,
and write the number you counted.

---

That is the whole draft. It is roughly 90 lines against the 200 lines of
`load_adjust.py` plus 125 of `rules.py` plus 101 of `parse.py` plus 64 of
`say.py` that it replaces, and unlike those it works on a host that runs no
scripts.

---

## The six known defects, verdict each

| # | Defect | Verdict |
|---|---|---|
| 1 | The rule dies at a chat boundary: `program-design` writes `agent/progression-state`, `load_adjust.py:142` reads `state["rules_by_exercise"]`, `hydrate.py:72-73` fills `state["progression"]`, nothing bridges them | **DISSOLVES.** `rules_by_exercise` exists only because `load_adjust.py`'s docstring admits no caller hands it a rule, so it invented a `setup` line. Delete the grammar and the rule is read from the program page, which is where it already is. |
| 2 | `session-runner` never calls `load-adjust` (`load_adjust.py:8`, ticket `workout-log-rb0`, P1) | **STILL NEEDS FIXING.** This is a trigger-wiring defect, not an arithmetic one. Guidance changes who does the arithmetic, not who is asked. The fix shrinks: the trigger becomes a sentence in `session-runner/SKILL.md` telling the coach to decide the next load when a session closes, instead of a function call. It still has to be written. |
| 3 | `next_target` type mismatch: `program_page.py` writes `"145 lb"`, `rules.py:30` multiplies it | **DISSOLVES**, and it was never live: nothing today reads `next_target` back into `cfg["current"]`, so the mismatch is latent and would have fired the day defect 1 was fixed. Under guidance the unit-carrying string is read by a reader that understands units. The check in the next section binds the shape so it cannot drift back. |
| 4 | `high_rpe_streak`, `declined_streak`, `pending_deload` are computed but absent from `program_page.PROGRESSION_FIELDS`, so `merge_progression` raises on them and the RPE cap can never fire across chats | **DISSOLVES.** All three are accumulator state that only exists because the fold exists. The drafted RPE clause reads two sessions off `Sets` instead of carrying a streak, `pending_deload` becomes a question asked and answered in the same conversation, and `declined_streak` collapses into `deload_declined_at`, which the page does carry. |
| 5 | `load-adjust/SKILL.md` "Turn 1, from cold" and `program-design/SKILL.md` both say the `progression` key is on `config-read("program/current")`; the code writes `agent/progression-state` | **STILL NEEDS FIXING, and it is now the highest-stakes line in the repo.** When prose is the authority, a wrong page name in prose is a wrong page name in production. Fix it in increment 1, before any deletion. |
| 6 | No fixture combines `@skill load-adjust` with `@cold`, which is why 26 green fixtures caught none of this (verified: `grep -l "@cold" fixtures/*/transcript.txt` returns eight fixtures, none of which mention `load-adjust`) | **STILL NEEDS FIXING, and the design makes it harder, not easier.** A fixture cannot prove prose: there is no model in the loop to be wrong. The replacement is a model eval case, which is the dependency the deletion is blocked on. |

Three dissolve, three survive. Two of the three survivors (5 and 6) are the
ones that decide whether this design is safe to ship, so the honest summary is
that replacing the arithmetic fixes the arithmetic-shaped defects and leaves
the wiring-shaped and proof-shaped ones exactly where they were.

### A seventh defect, not on the list, found while reading

`deload_pct` means three different things in three files.

- `schema/program-schema.json:340-344` declares `number`, `exclusiveMinimum:
  0`, `maximum: 1`. A fraction.
- `library/bbr.json` uses `0.9` six times. Read against the schema that is
  "deload to 90%", a 10% drop.
- `.claude/skills/load-adjust/scripts/rules.py:30` computes
  `current * (deload_pct / 100)` as the size of the drop. Read that way `0.9`
  is a 0.9% drop, and `say.py:38` would print "0.9% deload".

The fixtures pass because `fixtures/06-progression/transcript.txt:32` seeds
`deload_pct=10` by hand, which is neither of the other two readings.

Prose cannot fix this. Any wording I write is read against a number whose
meaning the file does not state, and a model will pick a reading and be
confidently wrong. **Rename the field to carry its own operation:
`deload_to_pct`, a fraction, meaning "the new target is this fraction of the
current one".** Then `0.9` can only mean one thing, in the schema, in the
library, and in the guidance. This is `principle-encode-lessons-in-structure`'s
strongest available rung: the bad value stops being representable instead of
being warned against.

Six files touch `deload_pct`: `schema/program-schema.json`, `library/bbr.json`,
`docs/program-format.md:79`, and the three load-adjust files that are being
deleted anyway.

---

## Does a deterministic proof survive? Yes, one.

The tension is real and I am not going to wave at it. `intake/scripts/ddl.py`'s
docstring records four tickets (`workout-log-29l`, `-3lw`, `-6zr`, `-8ms`)
that were "four symptoms of that one cause": a model hand-building a payload
from prose and drifting from the schema. The fix that stuck was "the schema is
read by code instead". Progression is a payload too, and a wrong weight is
written silently with no error anywhere.

But look at what those four tickets actually were. They were **payload shape**
failures, not **decision** failures. Nothing in that history says a model
chose wrongly between bump and hold; it says a model wrote a field name or a
type the schema did not carry. That distinction is the whole design of the
check.

**Keep one check. Bind the written value, never the decision.**

Rewrite `tools/replay/check_replay.py` in place, same path, same Makefile
line, new job. It exists today only to prove `rules.replay()`, which is being
deleted, so the file is free.

```python
# tools/replay/check_replay.py, after the rewrite. Signatures only.

def progression_writes(expected_tsv: Path) -> list[dict[str, Any]]:
    """Every `config-write agent/progression-state progression` payload in
    one expectation file, in write order. Already implemented today as
    `_progression_rows`; keep it verbatim."""

def declared_fields(schema_path: Path) -> frozenset[str]:
    """The seven field names, read from
    `schema/notion-schema.json` `config_pages['agent/progression-state']`.
    Read, never restated: this is the ddl.py lesson applied."""

def declared_increment(program_body: dict, exercise: str) -> tuple[float, str] | None:
    """The `increment` and `increment_unit` the program itself states for
    one exercise, or None if the block declares no progression rule."""

def check_shape(payload: dict, fields: frozenset[str]) -> list[str]:
    """One failure line per violation: a field name outside `fields`, a
    `next_target` not matching `^\\d+(\\.\\d+)? (lb|kg)$`, a `fail_count`
    that is not a non-negative integer."""

def check_step(previous: dict, current: dict,
               increment: tuple[float, str] | None) -> list[str]:
    """One failure line per illegal move between two consecutive writes for
    one exercise:
      - the unit changed
      - `next_target` rose by anything other than exactly one `increment`
      - `next_target` fell without `last_deload_at` or `stage_index`
        changing in the same payload
    This never decides whether a bump was correct. It asserts only that a
    bump which happened is the size the program declared."""
```

Three things it binds, and only three: the **shape** of the written value, the
**unit** it carries, and the **size of one step** against a number the program
itself states. It never reads a set, never judges a rep range, never decides.
Adding one number from a data file to another number is not an algorithm for
when to increase weight; it is a receipt that the increase matches the receipt
the program wrote.

Keep the current file's failure-on-zero behaviour: `check_replay.py:169-171`
prints FAIL when it checked no windows. A check that cannot fail is worse than
no check, and that line is what stops this one going quiet after the fixtures
move.

What it does not catch, said out loud: a bump at the wrong time. If the coach
bumps after a missed session, the write is exactly one increment, correctly
shaped, correctly united, and the check passes. That failure is caught only by
a model eval with a judged assertion, or by the athlete noticing. I am
accepting that, because binding "was this the right moment" means
re-implementing `rules.evaluate`, which is the thing the owner is deleting.

---

## Ticket `workout-log-8j6`: yes, mooted. Do not build it.

Plainly: **yes.** Close it, and close `workout-log-vi3` with it. Do not build
phase 2 or phase 3 of `.nikki-agents/replay-engine-scope.md`.

The reason, not just the verdict. That note's own "do-nothing case" says the
strong argument for the replay engine is repairability: "Today a missed or
duplicated `config-write` corrupts `fail_count` permanently; nothing
recomputes it." Under guidance, something does recompute it, and it is the
coach, in one sentence of prose that already exists in the draft above ("If
`fail_count` is missing from the record, do not assume zero. Count the
sessions..."). The prize the ticket was chasing arrives for free, as a
sentence, from a decision-maker that can also say out loud that it recounted.

The note's second strong argument, chat-boundary survival of
`high_rpe_streak`, is answered the same way and better: the drafted RPE clause
reads two sessions instead of carrying a streak, so there is no counter to
lose.

The note's third argument it already calls "weak, and honestly negative": the
field count does not go down.

Phase 1 of that note shipped and is what `check_replay.py` is today. It gets
rewritten, not deleted, so its machinery survives with a different job. Say
that in the ticket close so the work does not read as wasted.

---

## What gets deleted

Every path below was confirmed present with `ls` and `wc -l` at `9dc5ed8`.
Importer counts come from a repo-wide grep including `tools/` and `fixtures/`.

### Deleted outright

| Path | Lines | Who imports it today | Count |
|---|---|---|---|
| `.claude/skills/load-adjust/scripts/rules.py` | 125 | `load_adjust.py:51`, `tools/replay/check_replay.py:29` | 2 |
| `.claude/skills/load-adjust/scripts/parse.py` | 101 | `load_adjust.py:49`, `say.py:16`, `tools/replay/check_replay.py:28` | 3 |
| `.claude/skills/load-adjust/scripts/say.py` | 64 | `load_adjust.py:52` | 1 |
| `.claude/skills/load-adjust/scripts/load_adjust.py` | 200 | `tools/mock-notion/seams.py:34`, `tools/replay/check_replay.py:27`, plus `tools/package/check_zip.py:41-50` by glob | 2 named |

490 lines of Python, and with them: the `setup` turn grammar, `_YES`/`_NO`/
`_REASSURANCE`, `evaluate`, `replay`, `_miss`, `rpe_capped`, `bumped_value`,
`deload_target`, `TARGET_FIELD`, `HIGH_RPE`, the whole `OUTCOME` say table,
`Unreadable`, and the `cfg` keys `high_rpe_streak`, `declined_streak` and
`pending_deload` that no page ever carried.

### Edited, not deleted

| Path | Change | Consequence |
|---|---|---|
| `tools/mock-notion/seams.py:33-34, 43` | drop the `sys.path` insert, the `import load_adjust`, and the `"load-adjust"` row | `@skill load-adjust` in a transcript has no seam and `replay.py` fails on it |
| `tools/replay/check_replay.py` | rewritten in place per the section above | `Makefile:30` unchanged |
| `.claude/skills/load-adjust/SKILL.md` | three sections replaced with the draft above | the file becomes the authority |
| `.claude/skills/program-design/SKILL.md` | correct the page name for the `progression` key | |
| `schema/notion-schema.json` | move the seven field names out of `program_page.PROGRESSION_FIELDS` into `config_pages['agent/progression-state']` as a declared list | gives the check and the prose one source |

### Deleted only after the eval harness exists

| Path | Why it must wait |
|---|---|
| `fixtures/06-progression/` | its `transcript.txt` is 60 lines of `@skill load-adjust` turns with no seam left to run them |
| `fixtures/08-progression-refusal/` | same, and its whole subject is the parser being deleted |

26 fixtures become 24. That is the price, and it is bounded: `check_e1rm.py`,
`notion_ddl.py`, `catalog/check.py`, `library/check.py`,
`check_questions_docs.py`, `check_frontmatter.py`, `check_zip.py` and the
other 24 fixtures are untouched. Compare with the prior session's finding that
deleting all skill Python breaks six of nine proofs simultaneously; this
deletion touches one proof and two fixtures.

### Explicitly NOT deleted

- `.claude/skills/load-adjust/scripts/read_layer.py`, 93 lines. Imported by
  `tools/schema/check_e1rm.py:43`, which is a `make check` proof. It is the
  read-time layer (e1RM, unit conversion, ranking), not progression
  arithmetic, and `docs/architecture.md:109` and
  `docs/storage-section-design.md:34` both point at it as the one place that
  converts units. It stays, and `load-adjust` keeps a `scripts/` directory,
  which also keeps `check_zip.py:42-44` from tripping its "no `<skill>/scripts`
  dir in the ZIP" guard.
- `.claude/skills/program-design/scripts/program_page.py`. Four importers:
  `load_adjust.py:50`, `tools/mock-notion/hydrate.py:29`,
  `starting_loads.py:20`, `design.py:36`. Three survive the deletion. It owns
  the `program/current` round trip and the `agent/progression-state` write
  shape, and `progression_write` is still the one function that renders that
  payload for every caller that runs scripts at all.

---

## Sequencing, and the smallest first increment

Deletion-first is usually right and it is wrong here, for one reason: the
prose has to be correct before the code that currently does the job goes away,
or there is a window where nothing decides.

**Increment 1, and this is the whole ask.**

> Rewrite the three decision sections of
> `.claude/skills/load-adjust/SKILL.md` with the drafted "Deciding the next
> load" text above, and correct the two lines that name the wrong page for the
> `progression` key: `.claude/skills/load-adjust/SKILL.md` "Turn 1, from
> cold" and `.claude/skills/program-design/SKILL.md` "Turn 1, from cold".
> Delete no code. Touch no fixture. Then log one set in a fresh chat against a
> real program and read what the coach says and writes.

That is one file-and-a-half of prose and it is enough to get a correct,
spoken, non-silent decision in a fresh chat today, because the coach stops
looking for `state["rules_by_exercise"]` (which nothing ever fills) and starts
reading `agent/progression-state` (which `hydrate.py:72-73` already fills).
`make check` stays green throughout: the Python is still there, still
imported, still passing its fixtures. Nothing is at risk.

The increments after it, named but not argued here:

2. Rename `deload_pct` to `deload_to_pct` across the schema, `library/bbr.json`
   and `docs/program-format.md`. Independent of everything else, and it is a
   silently-wrong-number defect sitting in the library right now.
3. Build one eval case per `docs/scriptless-design.md` "What a case looks
   like": a cold chat, one top-of-range session, exact assertion on the
   `config-write`. This is the gate on increment 4.
4. Delete the four modules, edit `seams.py`, rewrite `check_replay.py`,
   retire the two fixtures.

Increments 1 and 2 are free and reversible. Increment 4 is not, and it is
correctly last.

---

## Where I think the order should not be followed literally

Three places. The owner asked for judgement rather than a menu, so these are
positions, not options.

**1. "No need to program an algorithm" is right about the decision and wrong
about the payload.** The four tickets in `ddl.py`'s docstring are the evidence,
and they are payload-drift tickets. Deleting the decision arithmetic while
also deleting every assertion about the written value would remove the only
thing standing between a hand-composed payload and the exact failure that
history already produced four times. The check in "Does a deterministic proof
survive" is small, it decides nothing, and it should be kept.

**2. Four of the six known defects are not arithmetic defects, and prose does
not fix them.** Defects 2, 5 and 6 are wiring and proof problems. Defect 5 in
particular gets *worse* under this design: today a doc that names the wrong
page is a stale comment beside working code, and after the change it is the
instruction production follows. If increment 1 lands the new decision table
and leaves those two "Turn 1, from cold" sections pointing at
`program/current`, the coach will read an empty key and answer "Noted." in
fluent prose, and the athlete will still lose the set. Fixing those two lines
is not a nice-to-have bundled with the rewrite; it is the rewrite's
precondition.

**3. The deletion is not free, and anyone who says the fixtures can just be
regenerated is wrong.** `tools/mock-notion/replay.py` replays a transcript
through a Python seam. With `load_adjust.adjust_turn` gone there is no seam,
so `--update` cannot regenerate anything and the two progression fixtures
cannot be repaired, only replaced. The replacement costs a model eval harness
that does not exist. My recommendation is to land increments 1 and 2 now, run
the prose against real training for a block, and only spend the eval money if
it survives that. If it does not survive, the Python is still there and
nothing was lost.

---

## Open, and honestly unresolved

- **How the coach knows which session is "the previous session" for one
  exercise.** `Sets.Session` is `rich_text`, not a relation
  (`schema/notion-schema.json`), and `row_query` has no ordering
  (`docs/architecture.md` "Mock reader contract"). Grouping rows by `Session`
  and ordering by `Timestamp` works, and I believe it is right, but I have not
  seen a fixture prove it and `.nikki-agents/replay-engine-scope.md` flags the
  same read-order gap for backfilled rows under rule L15's 7-day window.
- **Whether `next_target` should stay a unit-carrying string.** It is the
  right shape for a reader that speaks units and the wrong shape for anything
  that computes. Under this design nothing computes on it, so it stays. If a
  later Notion formula ever needs it, this decision is what will have to be
  revisited.
- **`workout-log-rb0`.** The trigger question stays open and this note does
  not close it. It shrinks from "wire a function call" to "write a sentence in
  `session-runner/SKILL.md`", but somebody still has to write the sentence and
  decide whether the decision fires per set, per exercise, or per session.
