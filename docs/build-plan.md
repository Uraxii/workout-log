# Release 1 build plan, v2.1

Ref key: `(NN sX)` = `research/NN-*.md` section X, where `00 sS` =
`00-synthesis-system.md`, `00 sT` = `00-synthesis-trainer.md`, `00 sQ` =
`00-open-questions-resolution.md`. `(dec "...")` = `.nikki-agents/decisions.tsv`,
all rows 2026-09-01. `(lim R#)` / `(lim L-##)` = `docs/limitations.md`.

## TL;DR

1. v2 rewrote v1 against the 11 root shapes in `docs/limitations.md` and three new user orders: no deploy during the build, agent-is-trainer with one client, calisthenics and functional strength first-class (lim R1-R11), (dec "Build plan v2 commissioned"). **v2.1** closes the two PARTIALs and five new defects the closure audit found; see s13.
2. **Set shape unified**: one row, an exercise-declared `measure` kind, nullable magnitude columns for duration, distance, level, interval. No second schema (lim R1), (02 s9).
3. **Lifecycle is 18 numbered rules**, not a transcript. `attempt`, write identity, frozen date and timezone all defined (lim R5), (lim R11).
4. **Grammar gets a five-rung fallback ladder** and tokens for time, distance, side, composed spoken numbers (lim R2), (lim R3).
5. **One client, one install.** No client entity, no multi-client audit; jurisdiction is per install (dec "T2 superseded").
6. **No Notion template.** `intake` creates the databases through the API on first "set me up" (dec "Notion template replaced by intake").
7. **Every phase proof runs offline** from fixtures against a mock writer. The real Notion check happens once, at install, by the user (dec "No deployment during the build").
8. Library grows to 10 templates and gains the formats they need; the exercise catalog ships in the package as 92 authored defaults plus an authored alias table, and a name it lacks is logged as typed (dec "Release-1 library grows from 3 to 10"), (dec "Exercise catalog").
9. Codex demoted to instructions-only; two supported install flavours, A and B (lim R10), (13 s2).
10. Seven skills still, seven phases still. Cut list grew by four, shrank by two.

## 1. Core data shape

Four Notion databases plus program and config pages. Log data is properties
because it gets filtered; config is page bodies because the user hand-edits it
(00 sS conflict (d)). One workspace = one client, always (dec "T2 superseded").

### 1.1 The set shape, in three lines (closes R1)

1. **One row shape, not four.** The exercise's catalog entry declares a `measure` kind; the `Sets` row carries nullable magnitude columns and the kind says which are meaningful. Copied from FitNotes' `Kind` field (02 s9); nullable Notion columns cost nothing (02 s3), (lim R1).
2. **Every gap in R1 is a magnitude or a modifier, never a new entity.** Seconds, metres, a level index, a side, an interval. Four parallel schemas would be more code for less query power (lim R1), (lim L-01).
3. **`load_kind` replaces two proposals at once**: research/02's `is_added_load` boolean and the cut `band` column. Assistance is a signed load, so an assisted trend cannot read backwards (02 s3), (lim L-04), (lim L-05).

`measure` enum on the catalog row: `weight_reps | reps_only | hold_time |
distance_load | distance_time | level_reps | interval_reps` (02 s9), (16 "Format fit").

### 1.2 `Sets` database — one row per set

Carried unchanged from v1: `Session`, `Exercise`, `Set index`, `Set type`,
`is_amrap`, `to_failure`, `RPE`, `RIR`, `Timestamp`, `machine_setting`,
`Side`, `reps_left`, `reps_right`, `Notes` (02 s2), (02 s3), (04 s7.3).
New or changed in v2:

| Property | Notion type | Why | Ref |
|---|---|---|---|
| `Load` + `Unit` | number + select `lb \| kg` | Renamed from `Weight`. Raw number typed, never normalised at rest | (dec "S11 units"), (02 s8) |
| `load_kind` | select `absolute \| added \| assist` | `bw+25` vs `bw-25`; assistance subtracts | (02 s3), (lim L-04) |
| `Reps` | number | Nullable now: a hold has none | (02 s2) |
| `duration_s` | number | Timed holds, planks, carries, run intervals | (02 s2 `duration_seconds`), (lim L-01) |
| `distance` + `distance_unit` | number + select `m \| km \| mi` | Carries and cardio | (02 s2 `distance`), (lim L-01) |
| `level` | number | Stage index inside `variation_chain` | (16 "Format fit"), (lim L-19) |
| `interval_s` | number | EMOM and every-N-minutes work; one row per round | (16 "Format fit"), (lim L-02) |
| `attempt` | number | Write-order counter, rule L7 | (lim L-25) |
| `write_key` | text | Renamed from `client_key`; it is a hash, not a person | (lim L-32), (04 s7.3) |
| `source_message_id` | text | Primary idempotency key, rule L9 | (04 s7.4), (lim L-26) |
| `Pain flag` | select `none \| niggle \| stop` | Mapped from free text by rule S3 | (02 s2), (lim L-38) |
| `confirm_line` | text | The audit trail: what the agent told the user | (dec "Open point 3") |
| `stale` | checkbox | Set by rule L14 when a `fix` invalidates a written target | (lim L-23) |
| `e1RM` | Notion formula | Read-time layer, section 1.7 | (02 s9), (lim L-36) |

Not shipped: `tempo`, still UNVERIFIED (00 sS delta 11). `band` returns as
`load_kind = assist` plus a `Notes` string (lim L-05).

### 1.3 The five example rows

Exercise `measure` in brackets. One user line, one or many rows.

| User typed | measure | Load | load_kind | Reps | duration_s | distance | level | Side | interval_s | rows |
|---|---|---|---|---|---|---|---|---|---|---|
| `185x5` | weight_reps | 185 lb | absolute | 5 | — | — | — | both | — | 1 (04 s2.4 A) |
| `l-sit 20s` | hold_time | — | — | — | 20 | — | — | both | — | 1 (lim L-01) |
| `farmer carry 60m @70lb` | distance_load | 70 lb | absolute | — | — | 60 m | — | both | — | 1, `implements=2` on the catalog row (02 s3 multiplier) |
| `ring row step 3 x8` | level_reps | — | — | 8 | — | — | 3 | both | — | 1 (16 "Format fit"), (lim L-19) |
| `kb swing emom 10x10 @24kg` | interval_reps | 24 kg | absolute | 10 | — | — | — | both | 60 | 10, `set_index` 1..10 (lim L-03), (lim L-02) |

Per-implement load sits on the catalog row as `implements`, not on the set: it is
a property of the exercise, so it costs zero set columns (02 s3), (lim R1).

### 1.4 `Sessions` database

v1's properties stand, with four changes. `Status` becomes `open | closed | abandoned | halted`, so `pain-triage`'s halt is a recorded state and not a no-op (lim L-39), (00 sT "Safety envelope"). `Date` and `Timezone` freeze at open by rule L4 (lim L-28), (lim L-29). `Cursor` stays stored but is advisory only, per rule L8 (lim L-27), (04 s7.3). `Readiness` 1-5 gets its own turn, per rule L2 (dec "S28 readiness"), (lim L-49).

### 1.5 The exercise catalog — package data, not a database

**Superseded.** s1.5 declared an `Exercises` database seeded with 913 rows.
The athlete's Notion holds logs only, so there is no such database. The
catalog is `exercises/defaults.json`, 92 exercises shipped inside the
package, which the agent reads to pick exercises when it builds a program
and never writes anywhere. Identity is the exercise `name`: no slug, no id.
A `Sets` row names its exercise by name, and a name the defaults lack is
written as the athlete typed it (s3.2 rung 4). `exercises/README.md` says
how the 92 were chosen.

### 1.6 Per-exercise state (closes R4)

**Superseded in its home, not in its content.** These fields were properties
on an `Exercises` row. That row does not exist, and none of them is a log, so
they live under the `progression` key on `program/current`, JSON encoded as
`{exercise name: {field: value}}` (`program-design/scripts/program_page.py`
owns the round trip). v1 put resolved ambiguity in `Sessions.Overrides`,
which dies at close (lim L-11).

| Field | Written by | Read by | Ref |
|---|---|---|---|
| `fail_count`, `training_max`, `stage_index`, `variation_index`, `last_deload_at` | `load-adjust` | `load-adjust` | (00 sS delta 4) |
| `deload_declined_at` | `load-adjust` | checked before re-offering a deload | (lim L-22), (dec "S19 progression") |
| `next_target` | `load-adjust` at close | `session-runner` at open | (dec "S19 progression"), (lim L-23) |

Two fields from the v1 table are gone rather than moved. `grey_band_answer`
was never written by any code: rule G2's reading survives inside the chat's
own `last_greyband` state and the `fix` that reverses it, and a field nothing
writes is not state. `target_source_set` was never written either, and it
pointed at a `Sets` row by an identity the reader would have had to
reconstruct.

### 1.7 Read-time layer (closes R9)

Storage rules are untouched; three read-only helpers sit on top (dec "S11 units").

1. `e1RM` is a Notion formula column on `Sets`: `Load / (1.0278 - 0.0278 * Reps)`, null above 10 reps or on a non-`working` set. Sort plus `page_size=1` answers "best ever" in one request (02 s9), (lim L-36).
2. Display conversion is read-only, into the `config/preferences` unit. A mixed lb/kg history ranks correctly and no stored row changes (lim L-35).
3. Carry-forward moves `{value, unit}` as one pair, never two rules (lim L-34), (02 s7).

### 1.8 The gym, `Programs`, config

**Superseded for `Locations`.** v1 gave the gym's equipment its own database.
Plates and bars are the athlete's own settings, not a log, so they are keys
on `config/preferences`: `location`, `plate_pairs_lb`/`_kg`,
`bar_weight_lb`/`_kg`, `min_increment_lb`/`_kg`.
`program-design/scripts/loads.increment_for` reads the last pair and floors a
resolved load to the smallest pair the athlete says her gym racks, falling
back to 5 lb / 2.5 kg when she has not said. `fixtures/14-plate-rounding` is
the proof, through a cold start.

`Programs` headers add `progression_unit: session | week | block | level` and
`dose: sets | minutes`, the two units the 10-template library needs (lim L-19),
(16 "Format fit"). Config stays page bodies (00 sS delta 7); `config/limits` holds
limits entries, `progression: manual`, `policy_checked`, clearance state and the
PAR-Q+ date (07 s1.1), (dec "T24 store policy_checked date").

## 2. Lifecycle rules (closes R5 and R11)

Rules, not a sample transcript. A transcript cannot be contradicted by a decision
that adds a line; a rule can be checked (lim R11), (lim L-49).

**Session identity and clock**

- **L1.** A session opens on the first logged set or an explicit readiness answer, whichever is first (04 s2.5), (dec "S28 readiness").
- **L2.** At open: the day opener, then the readiness ask as a separate short turn. Neither has an asserted line count (lim L-49).
- **L3.** `Timezone` is the device IANA zone at open, written once (02 s8).
- **L4.** `Date` is the local date in that zone at open, written once, never rewritten. An 11:40pm set landing at 00:05 belongs to the open date (lim L-28).
- **L5.** Every day-boundary check — same-day, `week_index`, the 3h resume ask — reads the stored zone, never the live device zone (lim L-29), (00 sS delta 2).
- **L6.** Two sessions may share a `Date`. Identity is the page id (02 s8).

**Write identity**

- **L7.** `attempt` counts per `(session, exercise, set_index)`, first write 0. A `fix` on an occupied slot writes `attempt+1` and supersedes (lim L-25).
- **L8.** `write_key = hash(session_id, exercise_id, set_index, attempt)`, query-before-create inside one write path, so a drifting `Cursor` corrupts nothing (lim L-27), (04 s7.3).
- **L9.** Idempotency is `source_message_id` alone. Second guard for a human retype: identical content in the same slot within 120 s is a duplicate, confirmed not re-written (lim L-26), (04 s7.4).
- **L10.** The confirm line the agent sent is stored as `confirm_line`. That is the whole audit log (dec "Open point 3"), (dec "T2 superseded").

**Session state**

- **L11.** `open -> closed` on "done for today"; `open -> abandoned` on answering *advance* at the next open (dec "S21 partial session").
- **L12.** `open -> halted` only by `pain-triage`. A halted session takes no set writes and never auto-advances the cursor. The only exit is `halted -> closed`, authorized by `pain-triage` alone, after the user explicitly acknowledges the hand-off; the cursor stays on the node it stopped at, so the next open resumes there (lim L-39), (00 sT "Safety envelope").
- **L13.** No session times out and discards data (04 s5.3).
- **L14.** A `fix` to a set `load-adjust` already read sets `stale` on the row and on `next_target`, and re-runs `load-adjust` for that exercise (lim L-23).
- **L15.** `fix` may target a named `abandoned` session within 7 days. That is release 1's only backfill (lim L-24), (dec "S8 history import").
- **L16.** `undo` targets the most recently written row of any kind, verbatim notes included. "Current session" is the most recently touched one until a new one opens (lim L-12), (04 s2.6).
- **L17.** A rest node takes `done`, `rest`, `skip` or any bare acknowledgement and advances the cursor with no set written (lim L-14), (dec "S22 rest days scheduled").
- **L18.** `week_index` derives from `Date` in the stored zone (00 sS delta 2).

## 3. Grammar and the fallback ladder (closes R2, R3)

v1's productions stand (04 s2.3) with four token families added, then one ladder.

### 3.1 New tokens

| Family | Accepts | Writes | Ref |
|---|---|---|---|
| time | `20s`, `45sec`, `1m30`, `2min`, `20 seconds` | `duration_s` | (lim L-01), (16 "Format fit") |
| distance | `60m`, `400m`, `1.5km`, `0.5mi`, `60 metres` | `distance` + `distance_unit` | (lim L-01), (lim L-08) |
| side | `5l/6r`, `8 left 7 right`, `10 per side`, `each side` | `Side`, `reps_left`, `reps_right` | (lim L-06), (02 s3) |
| interval / rounds | `emom 10x10`, `10 on the minute`, `e2mom`, ladder `1,2,3x5` | N rows, `interval_s`, `set_index` 1..N | (lim L-02), (lim L-03) |
| level | `step 3`, `level 3`, `progression 3` | `level` | (lim L-19), (16 "Format fit") |
| composed spoken number | `one thirty five` -> 135, `two twenty five` -> 225, `a hundred and ten` -> 110 | `Load` or `Reps` | (lim L-07), (04 s5.4), (dec "S24 voice input is real") |

Normalisation runs before the grammar: spoken numbers collapse, `by`/`at`/`*`
become `x`/`@`, and adjacent bare numbers join into one magnitude (`1 85 x 5` ->
`185x5`) (lim L-09), (04 s5.4). Rule A gains a fourth branch: first <= 10, second
> 30, no unit = **rounds x reps**, so `8x40` is 8 rounds of 40 (lim L-08),
(04 s2.4 A). An unknown unit suffix refuses to guess rather than falling through
(lim L-08). Rule J with no day scope matches the whole library and prompts only on
N>1 (lim L-13), (04 s2.4 J). New rule G2, **no dialogue** (HYPOTHESIS): a grey-band
`20x8` with no carry-forward source resolves in a fixed order — the exercise's
`measure` kind, then the program target if one exists, else read as weight x reps —
and the reading goes in the confirm line: "read as 20 lb x 8, `fix` if reversed".
The reading is stored in `grey_band_answer`. dec S26 stands intact: nothing is asked
mid-set, and `undo` or `fix` carries the correction (lim L-10), (dec "S26
weight/reps order"), (04 s3).

### 3.2 The ladder, five rungs, in order

| # | Rung | Cost | Ref |
|---|---|---|---|
| 1 | Grammar parse against today's day scope | 0 round trips | (04 s2.3) |
| 2 | Alias table lookup, authored, shipped in-repo | 0 round trips | (dec "Aliases authored by us"), (lim L-16) |
| 3 | Whole-word match, the athlete's own logged names first then the shipped defaults; refuses on a tie rather than picking | 0 round trips | (04 s2.4 J), (lim L-13) |
| 4 | Log the typed name verbatim, `measure` inferred from the set shape, said in the confirm line | 0 extra writes | (dec "Exercise catalog"), (15 DECISION), (lim L-15) |
| 5 | Verbatim `Notes` row, never a rejection | 1 write | (04 s2.6) |

Rung 4 is the "no match" path R3 asked for, so a required `Exercise` value no
longer contradicts never-reject (lim R3), (lim L-15). It costs nothing now:
the exercise IS the name, so there is no row to create and no id to mint.
Rung 3's "own names first" scope is derived from her logged `Sets`, never
stored.

**Entry budget, restated as a measurable proxy.** No phase proof can time a real
write, because nothing deploys (dec "No deployment during the build"). The budget
is therefore **tool round-trips per user turn**: rungs 1, 2 and 3 add 0 (local
string work against shipped tables); rung 4 adds 1 create; rung 5 adds 0. Ceiling
for one logged set: **1 create, at most 1 read, and 0 questions on the happy path**;
only a rung-3 tie ever asks, once, then it is remembered (04 s2.4), (lim L-11).
Phase 2's proof asserts the round-trip count per fixture line (lim R2).

## 4. Core loop

Turn shape is one confirm line plus one next-target line, never more unless asked
(04 s5.1). Readiness has its own turn (rule L2).

```
User:  what do i have today
Agent: Day B (Lower) - 5 exercises, ~40 min.
       Squat 3x5 @ 185 (up 5 from last). Last time: 180 x5,5,5.
       Warm-up: bar x5, 95x5, 135x3, 165x2 (165 = bar + 45,15).
Agent: Readiness 1-5? (skip if you like)
User:  4
Agent: Noted.
User:  185x5
Agent: Squat set 1 logged, 185x5. Set 2 at 185.
User:  l-sit 20s
Agent: L-sit set 1 logged, 20s. Set 2, same target.
User:  farmer carry 60m @70
Agent: Farmer's Carry set 1, 60m @70lb per hand. Set 2 at 70.
User:  new one, zercher squat 135x5
Agent: Added Zercher Squat to your catalog. Set 1, 135x5.
```

Confirm-line shape, exactly: `<exercise> set <n>, <magnitudes>[ @rpe]. <next
target>.`, where `<magnitudes>` is the measure kind's non-null columns in
declaration order (s1.1). On exercise close, append the per-set summary and the
progression outcome in one clause (04 s5.5); small bumps apply automatically,
deloads and -10% drops ask first (dec "S19 progression"). PR hints only within one
increment (dec "S25 PR hints"). Rest target rides in the same line, no fake timer
(04 s5.2). The time-cap trim ladder is stated, not asked (04 s1.5).

## 5. Intake, including database creation (closes part of R6)

### 5.1 Database creation on first run

There is no template page to duplicate (dec "Notion template replaced by intake").

1. The user creates one blank Notion page and grants the connector or MCP server access to it (13 s6), (00 sS "Friend replicates it").
2. The user says "set me up". `intake` reads `schema/notion-schema.json` — the single source of truth phase 1 builds — and creates `Sets` and `Sessions` under that page through the API (dec "Notion template replaced by intake"). Those two are the whole schema: Notion holds logs only.
3. Nothing is seeded, and there is no rate-limit wait. The exercise catalog is package data (s1.5).
4. Creation is idempotent: a database of that name under that parent is adopted, not duplicated. Same query-before-create discipline as rule L8 (04 s7.3).

**Vetoable**: it trades a published template page for an API call the user cannot
inspect first. See open point 1.

### 5.2 Question set

v1's 22 groups stand unchanged and in the same order — safety, goal, history,
constraints, body, recovery, preferences, two to four per turn (07 s2) — every
question asked, nothing silently defaulted (dec "Intake asks every profile
question"). Four changes:

| Change | Why | Ref |
|---|---|---|
| Q3 jurisdiction is per install, not per client | install = client | (dec "T2 superseded") |
| Q13 writes `config/preferences.location` through the section 6 write path | one named path | (lim L-33) |
| New Q23: preferred measure kinds — do you do timed holds, carries, runs, level-graded work | drives `measure` defaults and library choice | (lim R1), (16 "Format fit") |
| `intake_cursor` on `config/athlete`, written after every turn | 22 groups is 7-8 turns; a dropped connection must not restart it | (lim L-48) |

**Out-of-order answers.** Any recognised field volunteered mid-flow is written on
mention, and its item is skipped when its turn comes, with a one-clause
acknowledgement (lim L-47). Age stays an ordinary profile fact: no gate, no
guardian consent flow, no DPIA (dec "T18 final"); under-18 turns on LTAD limits as
trainer guidance (09 s7). Never asked: birth name, anatomy, identity history
(11 s6.3). Body fat never reported (00 sT TL;DR 9). Baseline branch unchanged from
v1 (dec "Baseline flow"), (dec "Baseline session shape"), (02 s9).

## 6. Skills

Seven skills (00 sT "Skill catalog"). No user data in any skill file; the repo is
public (dec "S2 paid Claude plan / S31 final"). Every skill retrieves from
reference files and never free-generates (00 sT TL;DR 2).

**One named write path.** `config-write(page, key, value)` and
`row-create(db, payload)` are the only two write verbs any skill may use. Both
are query-before-create (rule L8). This is what closes the "only `intake` writes
config" half of R6 without adding a skill (lim R6), (lim L-33).

| Skill | Trigger | Writes | New in v2, by root shape |
|---|---|---|---|
| `trainer-core` | Every coaching turn, loaded unconditionally | nothing, it gates | Audit = the stored `confirm_line`, single client, no per-client jurisdiction (dec "T2 superseded"), (lim L-31). Never unattended (dec "S4 no unattended runs") |
| `intake` | First run, "set me up", life change | all config, and the two log databases | Creates databases via API (dec "Notion template replaced by intake"). `intake_cursor` (lim L-48). Out-of-order writes (lim L-47). Q23 measure kinds (lim R1) |
| `screen` | Inside `intake`; re-fires on any health change | clearance state and date | PAR-Q+ verbatim, follow-ups only on YES (dec "T3 PAR-Q+ asked verbatim"). Owns the re-screen that clears `progression: manual`, rule S5 (lim L-42) |
| `program-design` | "Make me a plan", block end, **any new `open` limits entry** | `program/current`, `program/history/<date>` | Trigger threshold now defined (lim L-21). Scripted refusal-with-options, section 7.2 (lim L-17). Swap-in-place for one exercise, replacing the cut `substitute-exercise` (lim L-21). Emits `progression_unit: level` and `dose: minutes` (lim L-19) |
| `session-runner` | "What am I doing today", "next", "done", any logged set | set rows, session page, cursor | Preconditions, rule S1 (lim L-37). Fallback ladder, section 3.2 (lim R2), (lim R3). Readiness as its own turn (lim L-49). A new gym is a `config/preferences` answer, not a row (lim L-33). Rest-node acknowledgement, rule L17 (lim L-14) |
| `load-adjust` | End of set, exercise, session, **and any performance question** | `next_target`, per-exercise state | Reads `progression: manual` first (00 sT "PEM hard stop"). `deload_declined_at` (lim L-22). `variation_index` and `level` stepping (lim L-20). Recompute on `stale`, rule L14 (lim L-23). Never reads `load_kind = assist` as a rising trend (lim L-05). HRT branch lives here, since `deload` and `plateau-review` are cut (lim L-44), (00 sT "HRT-aware branch") |
| `pain-triage` | Pain, numbness, tingling, a pop, swelling, **plus crash, wiped out, payback, flare** | `halted` status, dated limits entry | Fatigue and crash language added (lim L-43). Free-text-to-enum table, rule S3 (lim L-38). Multi-profession hand-off in one line (lim L-45). Under-18 referral threshold, rule S4 (lim L-40) |

`screen` stays its own skill: PAR-Q+ expires at 12 months, any health change
re-fires it, and the measured LLM failure is over-flagging clearance
(00 sT "Why `screen` is its own skill").

### 6.1 Safety rules (closes R8)

- **S1.** `session-runner` refuses to open a session unless clearance is `cleared` or `not_required` and `program/current` exists. The refusal names which precondition failed (lim L-37), (00 sQ T7).
- **S2.** No set writes while `Status = halted`, per rule L12 (lim L-39).
- **S3.** `ref/red-flags` carries a phrase-to-enum table: "twinge", "tight", "sore" -> `niggle`; "sharp", "pop", "gave way", "shooting" -> `stop`, which also opens a limits entry and fires rule L12 (lim L-38), (00 sT "Safety envelope").
- **S4.** Under 18, the Ottawa ankle and knee rule text applies unchanged from age 5 up: same two-timepoint weight-bearing test, same tenderness landmarks, pooled sensitivity 98.5% ankle and 99% knee (17 TL;DR), (17 DECISION). Below age 5, including 5, no rule arithmetic: any suspected ankle or knee fracture after acute injury refers for imaging, because the paediatric meta-analyses have no data there and the known miss is the Salter-Harris growth-plate fracture (17 s2), (lim L-40).
- **S5.** `progression: manual` clears only on 14 consecutive symptom-free logged days plus either a clinician clearance date or a `screen` re-run. A bare confirm never clears it (lim L-42), (00 sT "PEM hard stop"), (10 s5).
- **S6.** `ref/scope-and-refusals` gains a row for relaying programming to an unscreened third party: redirect to the person, never program through a proxy (lim L-41), (dec "T2 superseded").
- **S8.** An open `config/limits` entry has exactly two exits, and neither deletes it. `session-runner` writes `resolved` when the user says the problem is gone **and** 14 days have passed with no `stop`-level mention of that movement, and states the date in the confirm line. Only `screen` writes `cleared by clinician`, and only against a named clinician and a date the user supplies. `pain-triage` re-opens the entry on any new mention of that area and resets the 14-day window (lim L-38), (00 sS delta 8), (07 s1.1).
- **S7.** Override tiers, named: *hard refusal* (red flags and out-of-scope, no override), *logged pushback* (objection stated, user may proceed, objection stored in `confirm_line`), *silent preference* (the user's call, no comment) (lim L-46), (12 s8.4), (00 sT TL;DR 8).

Reference files are v1's twelve (00 sT "Reference material index"), with
`ref/red-flags` gaining the S3 table and the S4 branch, `ref/wording` gaining the
section 7.2 refusal script and the multi-profession hand-off (lim L-45), and
`ref/progression-rules` gaining `variation_index` and `level` stepping (lim L-20).

## 7. Library and catalog (closes R7)

### 7.1 Ten templates

BBR, GZCLP, r/bwf RR, PHUL, Metallicadpa PPL, nSuns 5/3/1 LP, r/kettlebell wiki,
Easy Strength, Couch to 5k, Otago (dec "Release-1 library grows from 3 to 10"),
(16 TL;DR). Templates known via mirrors ship as our own page written from the
structure, citing the original author (dec "Templates known via mirrors").

Format features each one needs, all now present:

| Feature | Needed by | Closed by | Ref |
|---|---|---|---|
| Time-based sets | Couch to 5k, Norwegian 4x4 | `duration_s`, `measure: distance_time` | (16 "Format fit"), (lim L-01) |
| Minutes-per-week dosing | NIA guide | `dose: minutes` header | (16 "Format fit") |
| Level progression | Otago | `progression_unit: level`, `level` column | (16 "Format fit"), (lim L-19) |
| EMOM and ladders | r/kettlebell wiki | `interval_s`, N-row expansion, deterministic index | (16 "Format fit"), (lim L-02), (lim L-03), (lim L-18) |
| Seconds per side | mobility drills, L-sit, carries | `duration_s` + `Side` | (16 "Format fit"), (lim L-06) |
| Variable exercise count per day | Easy Strength | rotation node lists its own exercises; already legal | (16 "Format fit") |

The r/kettlebell wiki contradiction resolves to SHIP: its EMOM content is now
expressible, so the "SHIP" grade and the "grammar cannot express it" note no
longer disagree (lim L-18), (16 "Format fit").

### 7.2 Refusal with options

Five categories still have no shippable template and stay uncovered in release 1:
**rings-specific calisthenics, dedicated loaded carries, named-restriction
mobility, sport-general in-season maintenance, full-body hypertrophy** (16 "Gaps").
`program-design` never invents (00 sT TL;DR 2), so it uses one scripted reply in
`ref/wording`, three options, no silence (lim L-17):

> "I don't have a template for X. Three things I can do: run the nearest one I do
> have, [named template], which shares [what it shares]; build X's movements into
> your current program as accessory work; or point you at [source] to bring
> numbers back. Which?"

Rings and carries take option 1 or 2: the RR carries ring progressions, Easy
Strength carries loaded carries, both now expressible (16 calisthenics table),
(16 functional-strength table). Named-restriction mobility and in-season
maintenance take option 3, since only reference material exists (16 "Gaps").
Full-body hypertrophy is built from ACSM sets-per-muscle numbers, not dressed up
as a template (16 hypertrophy table), (08 Goal 2).

### 7.3 Catalog

free-exercise-db, 876 rows, Unlicense, no live API call at runtime; plus
`exercises/extra.json`, 24 authored rows closing the probe list, including Zercher
squat, Pendlay row, Nordic curl, ring row, wall walk, dragon flag; plus an
authored alias table; plus rung-4 runtime rows (dec "Exercise catalog"),
(dec "Aliases authored by us"), (15 DECISION), (lim L-16). Yoga and mobility
drills are program content or one extras row per drill, never a catalog category
(dec "Category probe rows").

## 8. Repo layout and install paths (closes R10)

```
workout-log/
├── AGENTS.md, CLAUDE.md
├── schema/notion-schema.json   # the one schema, read by intake AND the mock writer
├── exercises/{defaults.json,aliases.json}
├── library/<10 templates>
├── fixtures/<transcript, expected>
├── tools/mock-notion/          # offline writer, section 9
├── .claude/skills/<7 skills>/SKILL.md   # CANONICAL, Agent Skills spec
├── .agents/skills/             # Codex discovery path, generated symlinks
├── .github/copilot-instructions.md
├── .claude-plugin/{plugin.json,marketplace.json}
├── .mcp.json
└── dist/workout-skills.zip   # 7 skill dirs, each with its own data/ copies
```

Layout from (13 s7). `make skills` generates the symlinks and the ZIP (13 s7).

`schema/`, `exercises/` and `library/` sit at the repo root and two skills read
them, which flavour A gets from the checkout and flavour B does not get at all.
So `tools/package/build_zip.py` copies the files a skill actually reads into
`<skill>/data/<same repo-root path>` inside the ZIP, and `library.py`, `rows.py`
and `catalog.py` resolve `<skill>/data` first, the repo root second. Neither
present is a `FileNotFoundError` naming the path, never a silent wrong dir
(workout-log-d2y).

### 8.1 Two supported flavours

| # | A: Claude Code plugin | B: claude.ai ZIP |
|---|---|---|
| 1 | Free Notion account (00 sS "Friend replicates it" 1) | Same |
| 2 | Create one blank Notion page (dec "Notion template replaced by intake") | Same |
| 3 | `/plugin marketplace add Uraxii/workout-log` (13 s1.4) | Connect the Notion connector, OAuth, no keys (13 s6) |
| 4 | `/plugin install workout@uraxii-plugins` (13 s1.4) | Enable code execution in Settings, Capabilities (13 s6) |
| 5 | Grant the Notion MCP access to that page (13 s7) | Customize > Skills > Upload `dist/workout-skills.zip` (13 s6) |
| 6 | Say "set me up"; `intake` creates the two log databases (dec "Notion template replaced by intake") | Same |

A needs a terminal, an always-on PC and Pro-or-better, phone leg via Remote
Control (dec "Phone path"), (13 s5), (dec "Open point 5"). B needs none of those
and runs on Free, but distribution is hand-them-the-ZIP (13 s6).

### 8.2 Codex: instructions only

Codex reads `.agents/skills` and `AGENTS.md`, so the coaching text loads (13 s2).
It has **no documented Notion MCP wiring**: 13 s2 shows only a
`dependencies.tools: type: mcp` hint in `agents/openai.yaml` and a `config.toml`
enable/disable block, neither a server configuration, and nothing deploys during
the build so none can be verified (dec "No deployment during the build"). Codex
therefore ships as instructions only: skills load and advise, no set is written.
**Cost of the standing decision:** (dec "Plugin targets release 1") named three
targets and one cannot complete a turn, which is what case 10 found (lim L-50),
(lim R10). The `.agents/skills` symlinks are generated **and committed** by `make
skills`, so a Codex user gets the seven skills straight from a clone with no build
step (13 s2), (13 s7). Release 1 records Codex as **explicitly untested**: no phase
runs it (lim L-50). Promotion needs one verified Codex-to-Notion session, open point 4.

## 9. Build order, offline proofs

Nothing deploys during the build. Every proof runs from the repo with no Notion
and no phone; the real Notion check happens once, at install, by the user
(dec "No deployment during the build").

**The harness, built in phase 1 and used by every later phase.** `tools/mock-notion`
reads `schema/notion-schema.json`, accepts the same create and update calls
`intake` and `session-runner` make, and appends rows to a TSV. `fixtures/` holds
transcript files and expected-row tables. A phase passes when replay output
equals the fixture, byte for byte.

| # | Phase | Builds | Offline proof |
|---|---|---|---|
| 1 | Set shape and the harness | `schema/notion-schema.json`, `measure` kinds, `tools/mock-notion`, replay runner (section 1.1), (02 s9) | Replay a 3-set transcript against the mock writer; rows match `fixtures/01-three-sets.expected` exactly, including `Unit`, `set_index` and `measure` (dec "No deployment during the build") |
| 2 | Grammar and ladder | Rules A-J plus rule A branch 4 and G2, the four token families, the five-rung ladder (section 3), (04 s2.4), (lim R2) | Replay the 24 worked examples (04 s2.5) plus the 5 rows of section 1.3 plus one unknown name and one gibberish line. Every row matches; the unknown name creates a catalog row; gibberish lands as a note (lim L-15). A first-ever grey-band `20x8` resolves with no question and the confirm line states the reading (dec "S26 weight/reps order"). The harness asserts round-trips per line against the s3.2 ceiling (lim R2) |
| 3 | Lifecycle and write identity | Rules L1-L18, `attempt`, `write_key`, `halted` (section 2), (lim R5) | Replay an out-of-order pair, a same-id resend, a 20 s human retype, a midnight-crossing session and a 7-day-old `fix`. One row per set, `Date` unchanged across midnight, `attempt` increments on the fix (lim L-25), (lim L-26), (lim L-28) |
| 4 | Programs and the today answer | Program pages with `progression_unit: level` and `dose: minutes`, rest nodes, the opener plus the readiness turn (section 4), (16 "Format fit") | Replay a full cycle of GZCLP, Otago and Couch to 5k from `library/` against fixture openers, rest node included. The readiness turn appears once per session and is skippable; no line count is asserted (lim L-49), (lim L-14) |
| 5 | Intake, schema creation, screen | `intake` including the API create calls, `intake_cursor`, out-of-order writes, `screen` (section 5), (07 s2) | Replay a cold-start transcript against the mock writer: four databases created once, re-run adopts rather than duplicates, all 7 PAR-Q+ questions verbatim, a mid-flow volunteered answer written and its item skipped (lim L-47), (lim L-48) |
| 6 | Progression, safety, read-time layer | `load-adjust`, rules S1-S7, `e1RM` formula, display conversion (sections 1.7, 6.1), (dec "S19 progression") | Replay: three top-of-range sessions bump automatically; a -10% branch asks first; a declined deload is not re-offered (lim L-22); "sharp pain, felt a pop" flips `halted` and writes a limits entry (lim L-39); a bare "I'm fine" does not clear `progression: manual` (lim L-42); a mixed lb/kg fixture ranks best-squat correctly (lim L-35) |
| 7 | Packaging | `AGENTS.md`, Copilot instructions, Codex symlinks, plugin manifests, `make skills`, ZIP (13 s7) | `skills-ref validate` on all seven skill dirs (13 s4), `claude plugin validate ./`, the committed `.agents/skills` symlinks resolve from a fresh clone, and a grep for user data returns zero hits. `tools/package/check_zip.py` unpacks the ZIP into a scratch dir outside the repo, imports every `<skill>/scripts/*.py` from it and logs one set through `log_set` there, so flavour B is proved on the artifact the user uploads rather than on the repo tree (workout-log-d2y) (dec "S2 paid Claude plan / S31 final"). No install is attempted, and Codex is recorded untested rather than checked (lim L-50), (13 s2) |

**Install check, once, by the user, after phase 7.** Flavour A or B steps 1-6,
then log one set and confirm the row (dec "No deployment during the build").

## 10. Cut from release 1

| Cut | Ref |
|---|---|
| Interchange exporter; monthly Notion CSV export is the insurance | (dec "S6/S7 lock-in") |
| History import, except the 7-day `fix` window of rule L15 | (dec "S8 history import deferred") |
| Unattended runs, reminders, push notifications | (dec "S4 no unattended runs"), (14 s1.1) |
| Streaks | (dec "S22 rest days scheduled; S23 no streaks") |
| Age gate, guardian consent record, DPIA | (dec "T18 final") |
| Video assessment, movement screening, body-fat percentage | (07 s7), (07 s4.5) |
| Apple Health and Health Connect | (05 s6) |
| Vendoring Liftosaur; own grammar instead | (05 s3), (04 s1.2) |
| Self-hosted wger; crib the schema only | (00 sS conflict (f)) |
| `tempo` column, still UNVERIFIED | (00 sS delta 11) |
| Periodization | (00 sS "Progression default") |
| ExRx and Symmetric Strength percentile tables | (07 s10) |
| Skills `deload`, `re-entry`, `plateau-review`, `weekly-review`, `adherence`, `technique-cues`, `lifestyle-prompts` | (00 sT "Skill catalog") |
| Expansion reference packs: goals, sports, seasons, conditions, HRT, masters, youth | (00 sT "The expansion set") |
| Skills as Notion child pages | (dec "S31 skills live in a git repo") |
| **New:** client entity, multi-client audit, per-client jurisdiction | (dec "T2 superseded") |
| **New:** the Notion template page, published or not | (dec "Notion template replaced by intake") |
| **New:** Codex as an install flavour; instructions only | (lim R10), (13 s2) |
| **New:** five uncovered program categories, handled by the section 7.2 script | (16 "Gaps"), (lim L-17) |

**Off the cut list.** `band` returns as `load_kind = assist` (lim L-05).
`substitute-exercise` returns as `program-design`'s swap-in-place (lim L-21).

## 11. Case coverage

Every case in `docs/use-cases.md`, its break hypothesis, and the section that now
answers it.

| NN | Break hypothesis, short | Root shapes | Closing section |
|---|---|---|---|
| 01 | Readiness has no slot in a three-line opener | R11 | s2 rule L2, s4 (lim L-49) |
| 02 | Dictated numbers past twenty do not parse | R2 | s3.1 composed spoken numbers (lim L-07) |
| 03 | `20x8` grey band, `8x40`, a typo'd name, undo scope | R2, R4, R11 | s3.1 rule G2 and rule A branch 4, s1.6, s2 rule L16 (lim L-08), (lim L-10) |
| 04 | Rings: no bw load semantics, no variation stepping, no template | R1, R7 | s1.2 `load_kind`, s1.3, s6 `load-adjust`, s7.2 (lim L-04), (lim L-20) |
| 05 | Mixed units, mid-session gym change, no best-lift answer | R6, R9 | s1.7, s6 write path, s6 `session-runner` (lim L-33), (lim L-34), (lim L-35) |
| 06 | Otago levels, C25k durations, rest nodes with no exercise | R1, R2, R7, R11 | s1.2 `level` and `duration_s`, s2 rule L17, s7.1 (lim L-19), (lim L-14) |
| 07 | A declined deload is re-offered forever | R4 | s1.6 `deload_declined_at` (lim L-22) |
| 08 | EMOM, ladders, a time cap, undefined set index | R1, R2, R7, R11 | s1.2 `interval_s`, s1.3 row 5, s3.1 interval family, s7.1 (lim L-02), (lim L-03) |
| 09 | Carries, a catalog miss, per-side reps, no aliases | R1, R2, R3, R7 | s1.3, s3.1 side and distance families, s3.2 rung 2 and 4, s7.3 (lim L-01), (lim L-15) |
| 10 | Codex cannot complete one turn | R10 | s8.2, cost stated (lim L-50) |
| 11 | Lost writes, resends, out-of-order arrival, drifting cursor | R5 | s2 rules L7-L9 (lim L-25), (lim L-26), (lim L-27) |
| 12 | Midnight, a second session, a flight to Tokyo | R5, R11 | s2 rules L3-L6 (lim L-28), (lim L-29) |
| 13 | An abandoned day's real training cannot be entered | R9 | s2 rule L15, 7-day window (lim L-24) |
| 14 | A fix does not recompute a target already written | R4, R11 | s2 rule L14 and s1.6 `stale` (lim L-23); s2 rule L16 for undo scope (lim L-12) |
| 15 | 3,400 rows, alias collision, e1RM scan | R3, R9 | s1.7 e1RM formula, s3.1 rule J no-scope mode, s7.3 (lim L-13), (lim L-36) |
| 16 | Cold start writes a program with no clearance check | R4, R6, R8 | s6.1 rule S1, s5.2 cursor and out-of-order (lim L-37), (lim L-47), (lim L-48) |
| 17 | A halt that is not a status; an open limits entry has no exit | R7, R8 | s1.4 `halted`, s2 rule L12, s6.1 rules S2, S3 and S8, s6 `program-design` trigger (lim L-38), (lim L-39) |
| 18 | A 16-year-old through adult Ottawa rules; two red flags at once | R8 | s6.1 rules S4 and S6, s6 `pain-triage` (lim L-40), (lim L-41), (lim L-45) |
| 19 | A PEM crash has no trigger; `progression: manual` self-clears | R8 | s6 `pain-triage` triggers, s6.1 rules S5 and S7 (lim L-42), (lim L-43), (lim L-46) |
| 20 | Two clients in one conversation | R5, R6, R7, R8 | Out of scope by decision: one client per install. The agent says so and points at a second install (dec "T2 superseded"), (lim L-30) |

## 12. Open points

Global instruction says ask when unclear; this is an unattended write, so the
asks are here (dec "Stop asking the user research-decidable questions").

1. **Database creation by API is assumed and vetoable.** s5.1 replaces the template page (dec "Notion template replaced by intake"). Faster to replicate, but the user cannot inspect the schema first. Veto restores a published blank template and drops step 2 of both flavours.
2. **Which of the 10 templates is the first-run default.** (dec "Open point 4") sends this to a phase-4 prototype against three days, double progression, commercial gym; GZCLP is the standing favourite (16 TL;DR).
3. **Otago and NIA both, or one.** They overlap and answer different questions (16 "Open questions" 1). The ten-template list carries Otago only (dec "Release-1 library grows from 3 to 10").
4. **Codex promotion needs one verified MCP session**, impossible during the build (dec "No deployment during the build"), (13 s2).
5. **Resolved in v2.1.** Rule S4 is now sourced to research/17-ottawa-paediatric.md (Dowling 2009, Vijayasankar 2009). Residual: whether age 5 exactly sits above or below the floor is ambiguous in both abstracts; shipped below (17 Open Questions).
6. **The 24 extras rows are not authored yet.** (15 "Open Questions" 1) leaves it to a follow-up; phase 1 needs the file to exist, even stubbed.

## 13. Changelog v1 -> v2

| Shape | v1 defect | v2 section that closes it |
|---|---|---|
| R1 | A set is `{weight, reps}` and nothing else | s1.1 measure kinds, s1.2 columns, s1.3 five rows (lim R1) |
| R2 | One production shape, no fallback ladder | s3.1 four token families, s3.2 five rungs (lim R2) |
| R3 | "No match" is indistinguishable from "reject" | s3.2 rung 4 create-on-demand, s7.3 catalog (lim R3) |
| R4 | Per-exercise state dies at session close | s1.6 per-exercise state properties (lim R4) |
| R5 | No session clock owner, no write identity | s2 rules L3-L10 (lim R5) |
| R6 | Config singular, only `intake` writes it | s5.1 API creation, s6 one named write path (client half dropped per dec "T2 superseded") (lim R6) |
| R7 | `program-design` may only select, and `library/` is short | s7.1 ten templates plus formats, s7.2 refusal script (lim R7) |
| R8 | Safety state advisory, no status, no precondition | s1.4 `halted`, s6.1 rules S1-S7 (lim R8) |
| R9 | History stored raw with no read-time layer | s1.7 e1RM formula and display conversion, s2 rule L15 (lim R9) |
| R10 | Three targets committed, one undocumented | s8.2 Codex demoted to instructions only, cost stated (lim R10) |
| R11 | Lifecycle specified by transcript, not by rule | s2 eighteen numbered rules (lim R11) |

### v2 -> v2.1

| S4 sourced | rule S4 rewritten from research/17-ottawa-paediatric.md; open point 5 closed | s6.1, s12 |

Closure audit: 47 CLOSED, 2 PARTIAL, 5 new defects. Each row is one patch.

| # | Defect | Patch |
|---|---|---|
| 1 | Rule G2 opened a mid-set dialogue, which dec S26 forbids | s3.1 G2 rewritten as a no-dialogue resolution order with the reading in the confirm line; S26 intact (dec "S26 weight/reps order"), (lim L-10) |
| 2 | L-38 PARTIAL: nothing cleared an open limits entry | s6.1 rule S8, two exits, who writes each, re-open on mention (lim L-38), (00 sS delta 8) |
| 3 | Rule L12 named halted entry but no exit | s2 rule L12: `halted -> closed` only, `pain-triage` authorizes, cursor never auto-advances (lim L-39) |
| 4 | Case-14 cited `s1.6 stale` for its undo-scope half | s11 case 14 now cites rule L16 for L-12 (lim L-12) |
| 5 | The five-second budget was unmeasurable under offline-only proofs | s3.2 restated as round-trips per turn, per rung, asserted in phase 2's fixture (lim R2), (dec "No deployment during the build") |
| 6 | L-50 PARTIAL: symlinks uncommitted, Codex untouched by phase 7 | s8.2 and phase 7: symlinks committed by `make skills`, Codex recorded explicitly untested (lim L-50), (13 s2) |

Also changed, not from a root shape: no deployment during the build, so section 9
proofs are fixture-driven against a mock writer (dec "No deployment during the
build"); one client per install, so section 11 case 20 is answered by refusal
(dec "T2 superseded"); library 3 -> 10 and catalog extras adopted into sections
7.1 and 7.3 (dec "Release-1 library grows from 3 to 10"), (dec "Exercise catalog").
