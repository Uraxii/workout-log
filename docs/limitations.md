# Release-1 limitations

Merged from four tracer reports over docs/use-cases.md cases 01-20, traced
against docs/build-plan.md, research/, and .nikki-agents/decisions.tsv.
Inputs: /tmp/swarm-usecases/worker-1.md, worker-2.md, worker-3.md, worker-4.md.
Decisions are fixed. A decision shown to cost something is reported, not reopened.

## TL;DR

60 raw findings across 4 tracers (W1 15, W2 16, W3 12, W4 17). 50 after dedupe.

| severity | count |
|---|---|
| blocks-core-loop | 15 |
| safety | 8 |
| wrong-data | 17 |
| friction | 9 |
| cosmetic | 1 |

Five limitations hitting the most cases:

1. **L-01** (4 cases: 04, 06, 08, 09) a set is weight and reps only. No duration, no distance. Timed holds, C25k runs, EMOM, and loaded carries cannot be logged at all.
2. **L-49** (4 cases: 01, 06, 08, 12) dec S28 offers a readiness number at session open; phase 4's runnable check asserts the opener is exactly three lines with no slot for it.
3. **L-06** (3 cases: 06, 08, 09) `Side`/`reps_left`/`reps_right` ship in the schema, the grammar has no `left`/`right` token, so those columns can never be filled.
4. **L-15** (2 cases: 09, 15) `Exercise` is a required relation with no create-on-demand path, which directly contradicts the grammar's "never reject a line" promise.
5. **L-17** (2 cases: 04, 09) `library/` has no template for 5 categories and `program-design` never invents, with no scripted refusal, so the request dies silently.

L-21, L-33, and L-50 also hit 2 cases each at blocks-core-loop severity.

## Master table

Sorted by severity, then cases-hit descending.

| id | severity | design element (plan section) | defect | cases | source findings | decision or note exposed | minimal fix (HYPOTHESIS) |
|---|---|---|---|---|---|---|---|
| L-01 | blocks-core-loop | `Sets` db, docs/build-plan.md s1.1 (:23-45) | no `duration_seconds` and no `distance` column, and no matching `reps_expr` form | 04, 06, 08, 09 | W1-F9, W2-F1, W2-F10 | s7 cut list names `tempo` and `band`, never these two: silent drop, not a decision | add both columns plus a `NUM "s"` reps form and a distance unit token |
| L-15 | blocks-core-loop | `Exercise` relation, docs/build-plan.md s1.1 (:28) | required relation with no runtime create-on-demand path, so a catalog miss blocks the write | 09, 15 | W2-F8, W3-F9 | contradicts "never reject a line", research/04-routines-and-logging-ux.md:432-433 | adopt research/15's runtime user-added-row escape hatch (:189-202) into s1.3 |
| L-17 | blocks-core-loop | `program-design`, docs/build-plan.md s4 (:259) | "selects from library/, never invents" with no scripted reply when no template matches | 04, 09 | W1-F12, W2-F12 | research/16-program-library.md Gaps: 5 GAP categories incl. rings and carries (:100-104) | one refusal/nearest-template wording rule in `ref/wording` |
| L-21 | blocks-core-loop | `program-design` triggers, docs/build-plan.md s4 (:259) | "config change big enough to invalidate the plan" is undefined; no skill owns a targeted single-exercise edit | 17, 20 | W4-F6 | s7 cut list (:364) removes `substitute-exercise` and `re-entry` | define the threshold ("any new `open` limits entry") and give `program-design` a swap-in-place fallback |
| L-33 | blocks-core-loop | the gym's equipment, docs/build-plan.md s1.8 + intake q13 (:215) | no skill in the s4 table (:254-262) writes `config/preferences.location` outside one-time intake (it was a `Locations` database row when this was found) | 05, 20 | W1-F13 | mid-session gym change has no path into the data model | give `session-runner` a "new location described" trigger mirroring intake q13 |
| L-50 | blocks-core-loop | repo layout and friend replication, docs/build-plan.md s5 (:288-332) | Codex has no replication flavour, no documented MCP/Notion path, no committed skill symlinks, no phase-7 run | 10 | W2-F13, W2-F14, W2-F15, W2-F16 | dec "Plugin targets release 1" (decisions.tsv:81) commits to Codex CLI | write flavour C, document Codex MCP wiring or declare it unsupported, add a phase-7 run |
| L-02 | blocks-core-loop | grammar, research/04-routines-and-logging-ux.md s2.3 | no clock or interval concept; EMOM and a 20-minute time cap are unrepresentable | 08 | W2-F5 | 04 s5.2 "Do not fake it" bars a faked timer | real capability gap, not a grammar patch |
| L-03 | blocks-core-loop | `reps_expr`, research/04-routines-and-logging-ux.md s2.3 + s7.3 | no production expands one ladder line into N sets, and no deterministic `set_index` for the expansion | 08 | W2-F6 | shares the undefined-index problem with L-25 | new grammar production plus an index assignment rule |
| L-07 | blocks-core-loop | voice vocabulary, research/04-routines-and-logging-ux.md s5.4 (:579-596) | spelled numbers stop at twenty, nothing composes multi-digit words, `times` is not a multiplier (:315-332) | 02 | W1-F2 | dec S24 "voice input is real, first-class" (decisions.tsv:76) | normalize dictated numbers before the grammar runs |
| L-14 | blocks-core-loop | rest node, docs/build-plan.md s1.5 | rest node has no exercise, free text matches no command, `advance: on-log` never fires | 06 | W2-F3 | dec S22 puts rest nodes in every rotation (decisions.tsv:72) | a rest-day acknowledgment command that advances the cursor without a set |
| L-18 | blocks-core-loop | `library/` kettlebell wiki, research/16-program-library.md | :117 grades it "Fits s1.5: Yes / SHIP"; :184-186 says its EMOM/ladder content the grammar cannot express | 08 | W2-F7 | self-contradiction inside one file | downgrade to POINTER or scope SHIP to the non-EMOM subset |
| L-19 | blocks-core-loop | `progression_unit`, docs/build-plan.md s1.5 | enum is `session\|week\|block`; Otago progresses by level | 06 | W2-F2 | research/16-program-library.md:180-183 | add `progression_unit: level` with a stage-index-only rule |
| L-20 | blocks-core-loop | `load-adjust`, docs/build-plan.md s4 (:261) | behaviour list has no `variation_index` branch, so the s1.3 variation axis is driven by nothing | 04 | W1-F11 | s1.3 delta 5 exists to unify that axis | add a `variation_index` step rule to `ref/progression-rules` |
| L-25 | blocks-core-loop | `client_key`, research/04-routines-and-logging-ux.md:807 | the idempotency formula references `attempt`, a term defined nowhere | 11 | W3-F1 | phase-3's runnable check (docs/build-plan.md:341) claims to prove this mechanism | define `attempt` as a per-(session, exercise, set_index) write-order counter |
| L-30 | blocks-core-loop | config and program pages, docs/build-plan.md s1.6 (:104-113) | one `config/athlete`, one `config/limits`, one `program/current` per workspace: no client dimension | 20 | W4-F13 | dec "T2 users" requires jurisdiction and audit per client (decisions.tsv:87) | add a client relation or page-per-client before trainer support ships |
| L-37 | safety | `session-runner` trigger, docs/build-plan.md s4 (:260) | trigger row has no clearance-state and no program-exists precondition | 16 | W4-F2 | T7 gates activity behind confirmed clearance (00-open-questions-resolution.md:31) | add both preconditions to the trigger row |
| L-38 | safety | `Pain flag`, docs/build-plan.md s1.1 (:36) | enum `none\|niggle\|stop` has no free-text mapping rule, and no rule says what clears a limits entry | 17 | W4-F4 | s1.6 says an entry is "cleared only by the user" without defining the phrase | explicit phrase-to-level table in `ref/red-flags` |
| L-39 | safety | `pain-triage`, docs/build-plan.md s4 (:262) | output "session halt" has no matching `Sessions.Status` value, so the halt is a no-op | 17 | W4-F5 | :63-64 lists only `open\|closed\|abandoned` and "no session times out" | add a `halted` status requiring explicit user action to leave |
| L-40 | safety | `ref/red-flags`, docs/build-plan.md s4 (:273) | Ottawa rules carried with no age branch | 18 | W4-F7 | source states paediatric application "was not searched" (00-synthesis-trainer.md:204-206); dec T18 final removes the age gate (decisions.tsv:97) | state a lower referral threshold for under-18, sourced separately |
| L-41 | safety | scope table, research/12-trainer-practice-and-ethics.md:107-114 | no row for relaying programming to an unscreened third-party coach | 18 | W4-F9 | dec "T2 users" enumerates self, friends, trainers-with-clients only (decisions.tsv:87) | add a scope-table row: redirect to the client, do not program through a coach |
| L-42 | safety | `progression: manual`, research/00-synthesis-trainer.md:291,297 | cleared by a bare user say-so, which is exactly the failure mode the switch disabled | 19 | W4-F10 | 10-medical-and-special-populations.md:517-519 lists this as a thing to avoid | require a symptom-free window or a re-screen, not a bare confirm |
| L-43 | safety | skill triggers, docs/build-plan.md s4 (:260-262) | no trigger list includes fatigue or crash language; a conversational PEM report has nowhere to land | 19 | W4-F11 | `pain-triage` triggers on pain, numbness, tingling, a pop, swelling only | add crash/fatigue language to `pain-triage`'s trigger list |
| L-44 | safety | HRT-aware branch, research/00-synthesis-trainer.md:304-317 | the branch's home skills `deload` and `plateau-review` are cut; `load-adjust` triggers only on set/exercise/session end | 20 | W4-F15 | s7 cut list, docs/build-plan.md:364 | extend `load-adjust`'s trigger to performance questions, or move the branch to `trainer-core` |
| L-08 | wrong-data | Rule A, research/04-routines-and-logging-ux.md:336-349 | `8x40` matches none of the three magnitude branches; `2x40m` falls silently into sets-by-reps | 03, 09 | W1-F4, W2-F10 (misparse half) | the fall-through loses distance instead of asking | add a fourth branch for first<=10, second>30, and refuse on an unknown unit |
| L-10 | wrong-data | dec S26, .nikki-agents/decisions.tsv:70 | "guess from last logged set" has no input on a user's first-ever set of that exercise, and does not fall back to Rule A's ask | 03, 16 | W1-F3 | dec S26 replaced Rule A's ask-once (research/04:343-345); its own justification was miscited (decisions.tsv:85) | fall back to ask-once when no carry-forward source exists |
| L-16 | wrong-data | `aliases`, docs/build-plan.md s1.3 (:79) | column is specced as populated from free-exercise-db, which has no aliases field; empty at seed | 09, 15 | W2-F9, W3-F10 | research/15-exercise-catalog-coverage.md:153,164-172; Rule J degrades to exact-name match | cite research/15's extras.json + hand-authored alias table in s1.3 |
| L-26 | wrong-data | idempotency, research/04-routines-and-logging-ux.md:816-827 | two competing schemes ("content + position, or the platform message id") with no rule for which; a human retype gets a fresh id and is not caught | 11, 20 | W3-F2, W4-F17 | phase-3's proof only replays a same-id resend (docs/build-plan.md:341) | pick the platform message id, drop the other, and add a content match inside a short window |
| L-04 | wrong-data | `Sets` db, docs/build-plan.md s1.1 (:23-45) | no field distinguishes load added on top of bodyweight from an absolute weight, though Rule F promises both | 04 | W1-F8 | research/02-data-model.md:82-108 recommends the flag | add an `is_added_load` boolean per research/02 s3 |
| L-05 | wrong-data | s7 cut list, docs/build-plan.md:347-361 (delta 11) | `band` is cut, so assistance context the user typed is dropped and an assisted trend reads backwards | 04 | W1-F10 | research/02-data-model.md:93-95 warns of exactly this | keep it in `Notes` and tell `load-adjust` never to read that as a trend signal |
| L-11 | wrong-data | `Overrides`, docs/build-plan.md s1.2 (:60) | Rule A promises the grey-band answer is "remembered for that exercise", but `Overrides` is session-scoped and inert at close | 03 | W1-F7 | research/04:343-345 vs :746-754 | store the resolution on the Exercise row, not the session page |
| L-22 | wrong-data | per-exercise state, research/00-synthesis-system.md delta 4 (:198-201) | no "deload offered and declined" flag, so a repeat 3rd fail is indistinguishable from a fresh one | 07 | W2-F4 | dec S19 "deloads ask first" is silent on a decline (decisions.tsv:68) | add `deload_declined_at`, checked before re-asking |
| L-23 | wrong-data | `load-adjust` write-back, docs/build-plan.md s4 (:259) + s1.6 (:98-100) | a `fix` to a set `load-adjust` already read never recomputes the written next target; per-exercise state has no rollback | 14 | W3-F8 | dec S19 writes the next target at close (decisions.tsv:68) | flag the target and state stale on `fix`, re-run `load-adjust` |
| L-24 | wrong-data | `fix`, research/04-routines-and-logging-ux.md:465-473 | nothing writes real data into an abandoned session's "not done" slots: `fix` needs an existing row, no reopen or backdate command exists | 13 | W3-F6 | dec S8 history import deferred (decisions.tsv:80); dec S21 (decisions.tsv:73) | let `fix` target a named prior abandoned session within a short window |
| L-27 | wrong-data | `Cursor`, research/04-routines-and-logging-ux.md:811-814 | stored, race-prone field the design admits can drift mid-session, with no lock and repair only at next open | 11 | W3-F3 | phase-3's proof never replays an out-of-order pair (docs/build-plan.md:341) | query-before-create against the cursor inside one lock |
| L-28 | wrong-data | `Sessions.Date`, docs/build-plan.md s1.2 (:54, 68-73) | no lifecycle rule says whether `Date` freezes at open or re-evaluates as sets log past local midnight | 12 | W3-F4 | feeds week_index (research/00-synthesis-system.md delta 2) and roll-ups | state that `Date` is set once at open and never rewritten |
| L-29 | wrong-data | timezone ownership, docs/build-plan.md s1.2 (:55) | no rule says which clock, the session's stored zone or the live device zone, frames the same-day check for S21 and the s5.3 gap ask | 12 | W3-F5 | research/00-synthesis-system.md:186-191 anchors week_index but not this | anchor every day-boundary check to the session's stored IANA zone |
| L-31 | wrong-data | open point 3, docs/build-plan.md s8 (:379-381) | audit log shape is unresolved and deferred to phase 3 design, but T2 makes it load-bearing from turn 2 | 20 | W4-F16 | dec "T2 users" (decisions.tsv:87) | settle open point 3 before any trainer-facing phase |
| L-34 | wrong-data | carry-forward, research/02-data-model.md:199-217 | `weight` and `unit` carry forward by two decoupled rules, so a bare number can inherit the wrong unit | 05 | W1-F14 | dec S11 stores a unit per row (decisions.tsv:69) but never pairs the carry | carry `{value, unit}` as one pair from the previous set |
| L-35 | wrong-data | `Weight` "never normalised", docs/build-plan.md s1.1 (:30) | no read-time carve-out, so a cross-unit "best lift" query is unanswerable or must break the rule | 05 | W1-F15 | dec S11 units (decisions.tsv:69) | read-time-only conversion for ranking and display, never touching stored rows |
| L-47 | wrong-data | intake flow, docs/build-plan.md s3 (:198-224) | no rule for a user volunteering the answer to a later intake item mid-flow | 16 | W4-F1 | grep of research/04 and research/07 for out-of-order handling returns nothing | write any recognized field on mention, skip that item when its turn comes |
| L-49 | friction | phase 4 check, docs/build-plan.md s6 (:342) | opener is asserted to be "exactly three lines"; dec S28's readiness number has no slot in it or in the first-set confirm | 01, 06, 08, 12 | W1-F1 | dec S28 (decisions.tsv:71) vs docs/build-plan.md:61,193 | ask readiness as its own short turn after the opener |
| L-06 | friction | grammar, research/04-routines-and-logging-ux.md s2.3-s2.4 | no `left`/`right` token anywhere, so the shipped `Side`/`reps_left`/`reps_right` columns can never be populated by a parsed line | 06, 08, 09 | W2-F11 | schema is ready (docs/build-plan.md s1.1), grammar is not | add a `NUM "left" NUM "right"` production |
| L-12 | friction | `undo` and `fix` scope, research/04-routines-and-logging-ux.md:470-477 | undefined whether a verbatim Note counts as "the last entry", and whether a closed session is still "current" | 03, 14 | W1-F6, W3-F7 | 04 s2.6's fallback creates rows nothing claims | Notes are entries; "current session" is the most recently touched one until a new one opens |
| L-09 | friction | tokenizer, research/04-routines-and-logging-ux.md:315-332, 386-389 | entries split on `;` only; a mangled numeric stream like `1 85 x 5` has no defined tokenization | 03 | W1-F5 | likely to co-occur with dictation (case 02) | tolerant pre-pass joining adjacent bare numbers into one weight |
| L-13 | friction | Rule J, research/04-routines-and-logging-ux.md:386-389 | "prompt only on two matches in today's day" is undefined when free-logging with no active day scope | 15 | W3-F12 | 876-entry library, where "press" has many candidates | with no day scope, match the whole library and prompt on N>1 |
| L-36 | friction | PR queries, research/02-data-model.md:246-248, 306-312 | no stored or formula e1RM field, so an e1RM "best ever" needs an unscoped client-side scan | 15 | W3-F11 | Notion ~3 req/s, per-workspace cap unpublished (research/01-storage-options.md:61) | add a formula e1RM column so sort + `page_size=1` answers it |
| L-45 | friction | hand-off template, research/00-synthesis-trainer.md:141-163 | no rule for naming two professions in one confirm-shaped line when two red flags fire | 18 | W4-F8 | actions already union to "stop", so this is wording only | let the template take a list of professions and stay one line |
| L-46 | friction | override tiers | referenced as a structure by docs/use-cases.md:531 but never defined | 19 | W4-F12 | research/12-trainer-practice-and-ethics.md:925-935 and 00-synthesis-trainer.md:22 gesture at one | name the tiers in `ref/scope-and-refusals` |
| L-48 | friction | `intake`, docs/build-plan.md s4 (:257) | no resume marker for a half-finished intake, unlike Sessions' `Cursor` | 16 | W4-F3 | intake is 22 items at 2-4 per turn, so 7-8+ turns (docs/build-plan.md:198-224) | store an `intake_cursor` on `config/athlete` |
| L-32 | cosmetic | `client_key`, research/04-routines-and-logging-ux.md:806-810 | the name means an idempotency hash, not a coaching client, which misleads given L-30 | 20 | W4-F14 | reinforces that no client-scoping field exists | rename to `write_key` |

## Root shapes

Eleven shapes explain all 50. The build-plan revision should be driven from
these, not from the rows.

**R1. A set is `{weight, reps}` and nothing else.** The `Sets` row carries one
magnitude and one count. Every other physical dimension a lifter produces
(seconds under tension, metres carried, load relative to bodyweight, assistance
applied) has no column. research/02-data-model.md recommended `duration_seconds`,
`distance`, and an `isAssisting` flag; s1.1 ships none of them and s7's cut list
records only `tempo` and `band`, so two of the four were dropped with no
decision behind them. Explains L-01, L-04, L-05.

**R2. The grammar has one production shape and no fallback ladder.** Everything
is `weight? reps_expr rpe?` split on `;`. Anything else falls straight through
to the verbatim-note escape, which never rejects but also never parses. So a
number the vocabulary cannot spell, a multiplier it does not list, a per-side
split, a rounds count, a clock, a mangled token stream, and a turn with no
exercise at all are one gap, not seven. Explains L-02, L-03, L-06, L-07, L-08,
L-09, L-14.

**R3. Nothing distinguishes "no match" from "reject".** `Exercise` is a required
relation, `aliases` is empty at seed, and Rule J has no mode for matching
without a day scope. The grammar promises never to reject a line; the schema
makes an unmatched name unwritable. research/15 decided a runtime escape hatch
and build-plan never cites it. Explains L-13, L-15, L-16.

**R4. Resolved ambiguity and progression state have no per-exercise home that
outlives one session.** A grey-band answer, a declined deload, and a corrected
set all need to be remembered against an exercise. The only durable per-exercise
state is delta 4's five-field list, and per-session `Overrides` dies at close.
So a promise to "remember" is unkeepable and a correction cannot roll anything
back. Explains L-10, L-11, L-22, L-23.

**R5. A session has no clock owner and no write identity.** `Date` has no freeze
rule, no rule names the governing timezone, `Cursor` is a stored field with no
lock, the `client_key` formula names an undefined `attempt`, and idempotency has
two competing schemes at once. Five symptoms of one missing thing: a defined
session identity with a defined write order. Explains L-25, L-26, L-27, L-28,
L-29.

**R6. Config pages are singular and only `intake` writes them.** One
`config/athlete`, one `config/limits`, one `program/current`, one gym-equipment
write path, no intake cursor, no rule for an answer arriving early, no client
dimension, no audit shape. Everything that must be per-client or written
mid-session collides with this. Explains L-30, L-31, L-32, L-33, L-47, L-48.

**R7. `program-design` may only select from `library/`, and `library/` is
short.** Five GAP categories, no `level` progression unit, no `variation_index`
stepping, no targeted single-exercise edit, no scripted refusal, and one
template graded SHIP and unrunnable in the same file. Explains L-17, L-18, L-19,
L-20, L-21.

**R8. Safety state is advisory, with no status, no enum mapping, and no
precondition.** `pain-triage` can output a halt that no `Sessions.Status`
records, `Pain flag` has no rule connecting free text to its enum,
`session-runner` checks no clearance, `progression: manual` clears on a bare
confirm, no trigger owns a crash report, `ref/red-flags` has no age branch, and
the skills the HRT branch lives in are cut. This is the largest cluster and the
only one where the failure mode is harm rather than data loss. Explains L-37,
L-38, L-39, L-40, L-41, L-42, L-43, L-44, L-45, L-46.

**R9. History is stored raw with no read-time layer.** Units never normalise,
weight and unit carry forward separately, e1RM is computed nowhere, and an
abandoned session's slots are permanently wrong. Every "best ever" or
cross-session question runs against rows that were never prepared to answer one.
Explains L-24, L-34, L-35, L-36.

**R10. Three plugin targets are committed and one is documented.** Flavours A
and B exist; Codex has no replication steps, no MCP path, no committed symlinks,
and no phase-7 coverage. Explains L-50.

**R11. Turn lifecycle is specified by sample transcript, not by rule.** The
opener's shape is asserted as a line count, so a decision that adds a line
contradicts a runnable check. `undo` and `fix` are described against an example,
so their scope after a fallback note or after close is undefined. Explains L-12,
L-49.

## Refuted or downgraded

Break hypotheses the tracers did not sustain as written. These claims should not
be counted against the design.

| case | claim | verdict | citation |
|---|---|---|---|
| 09 | "distance, duration and per-side have no property" | PARTIAL: per-side overstated. `Side`, `reps_left`, `reps_right` exist; the gap is grammar only | docs/build-plan.md s1.1; worker-2.md:55 |
| 11 | "nothing detects a lost write" | REFUTED at the transport layer: Remote Control queues and delivers on reconnect | research/13-plugin-packaging.md:376; worker-3.md:18-22 |
| 12 | "no timezone owns the week boundary" | REFUTED as stated: delta 2 ties week_index to the session's own local date. The narrower gap (which clock frames the live day check) stands as L-29 | research/00-synthesis-system.md:186-191; worker-3.md:35-39 |
| 14 | "undo's last entry is the session RPE" | REFUTED on input order: `fix` is typed after the RPE, so by recency `undo` targets the fix | research/04-routines-and-logging-ux.md:470-477; worker-3.md:65-70 |
| 15 | "pages 3,400 rows with no aggregation" | REFUTED for a weight-only "best": Notion filter + sort + `page_size=1` avoids the scan. CONFIRMED only for the e1RM reading, kept as L-36 | research/02-data-model.md:246-248; worker-3.md:83-88 |
| 15 | "3 plates x10 is unparseable" | Downgraded: it degrades gracefully to a verbatim note as designed. The catalog block is the real defect | research/04-routines-and-logging-ux.md s2.6; worker-3.md:78 |
| 18 | "two red flags collide" | PARTIAL: both rows union to "stop the session now", so the mechanical action does not collide. Only the wording is unhandled, kept as L-45 | research/00-synthesis-trainer.md:137-139; worker-4.md:46 |
| 05 | `32kg x12` shape not in the worked examples | Downgraded: the outcome is unambiguous, not scored | research/04-routines-and-logging-ux.md s2.5; worker-1.md:66 |
| 11 | "where was i" at 40 minutes should ask | Downgraded: 40 min is under the 3h threshold, so no ask fires. Correct behaviour | research/04-routines-and-logging-ux.md:565-577; worker-3.md:16 |

Case 03's hypothesis was broader than the author stated, not narrower: it also
surfaced L-11 beyond the four named breaks (worker-1.md:107).

## Contradictions in the research

Both citations given. Each of these is a place the corpus disagrees with itself.

1. **Kettlebell wiki graded both ways.** research/16-program-library.md:117 grades it "Fits s1.5: Yes / SHIP"; :184-186 lists its EMOM and ladder content as something the grammar cannot express. (W2-F7, L-18)
2. **Opener line count vs readiness.** docs/build-plan.md:342 asserts the opener is "exactly three lines"; .nikki-agents/decisions.tsv:71 (S28) offers a readiness number at session open. (W1-F1, L-49)
3. **Grey-band guess vs ask.** .nikki-agents/decisions.tsv:70 (S26) overrides research/04-routines-and-logging-ux.md:343-345's ask-once with a guess, and leaves no fallback when there is nothing to guess from. decisions.tsv:85 separately records that S26's own justification cited the wrong section. (W1-F3, L-10)
4. **One Notion path for every harness.** docs/build-plan.md s2 says "Notion arrives through `.mcp.json`"; research/13-plugin-packaging.md s1.2 shows that mechanism is Claude-Code-plugin-specific and s2 documents no MCP path for Codex. (W2-F14, L-50)
5. **Required relation vs never reject.** docs/build-plan.md:28 and research/02-data-model.md:73 make `Exercise` required; research/04-routines-and-logging-ux.md:432-433 promises never to reject a line. research/15-exercise-catalog-coverage.md:189-202 decided the escape hatch, and build-plan cites it nowhere. (W2-F8, W3-F9, L-15)
6. **A halt that is not a status.** docs/build-plan.md:262 gives `pain-triage` a "session halt" output; :63-64 lists only `open|closed|abandoned` and states no session times out. (W4-F5, L-39)
7. **HRT branch homed in cut skills.** research/00-synthesis-trainer.md:306 places the branch in `load-adjust`, `deload`, and `plateau-review`; docs/build-plan.md:364 cuts the last two. (W4-F15, L-44)
8. **Remembered per exercise, stored per session.** research/04-routines-and-logging-ux.md:343-345 promises the grey-band answer is remembered for that exercise; docs/build-plan.md:60 and research/04:746-754 make `Overrides` session-scoped. (W1-F7, L-11)
9. **Silent drops vs recorded cuts.** docs/build-plan.md s7 records `tempo` and `band` as cut; `duration_seconds` and `distance` are recommended by research/02-data-model.md s2, absent from s1.1, and absent from the cut list. (W1-F9, W2-F10, L-01)

## Decisions with a cost

Stated neutrally. The decision stands; the case shows what it costs.

| decision | source | case | cost |
|---|---|---|---|
| S24 voice input is real, first-class | decisions.tsv:76 | 02 | every turn of the dictation persona falls to the verbatim-note fallback, which answers by abandoning parsing (W1-F2) |
| S26 guess from the last logged set, never open a dialogue mid-set | decisions.tsv:70 | 03, 16 | a first-ever set of an exercise has nothing to guess from, and the ask-rule it replaced is not available as a fallback (W1-F3) |
| S11 units, every row stores its unit, never normalised | decisions.tsv:69 | 05, 15 | "what is my best squat" over a mixed lb/kg history has no answer that does not break the rule (W1-F15) |
| S28 readiness offered at session open | decisions.tsv:71 | 01 | phase 4's runnable check asserts a three-line opener, so the readiness ask has no place to live (W1-F1) |
| S19 progression, deloads ask first | decisions.tsv:68 | 07, 14 | nothing records a decline, so the ask repeats; and the next target is written at close with no recompute after a correction (W2-F4, W3-F8) |
| S21 partial session, finish-or-advance at next open | decisions.tsv:73 | 13 | "advance" records real training as "not done" with no way back (W3-F6) |
| S8 history import deferred | decisions.tsv:80 | 13 | the only mechanism that could have repaired an abandoned session's slots is out of release 1 (W3-F6) |
| S22 rest days scheduled in the rotation | decisions.tsv:72 | 06 | a rest node has no exercise, so a free-text turn at one has nowhere to land (W2-F3) |
| Plugin targets release 1: Claude Code, Codex CLI, GitHub Copilot | decisions.tsv:81 | 10 | two of the three targets have documented flows; the Codex user cannot complete a single turn (W2-F13 to F16) |
| T2 users includes trainers with clients, jurisdiction per client | decisions.tsv:87 | 20 | s1.6's config and program pages are singular per workspace, with no client dimension and no settled audit shape (W4-F13, W4-F16) |
| T18 final, no age gate | decisions.tsv:97 | 18 | a 16-year-old is routed through Ottawa rules validated on adult cohorts only, with the source's own paediatric caveat not carried into `ref/red-flags` (W4-F7) |
| Release-1 cut list (`substitute-exercise`, `re-entry`, `deload`, `plateau-review`, `band`, `tempo`) | docs/build-plan.md:347-364 | 04, 17, 20 | an open limits entry can block a movement nothing can swap; the HRT branch loses two of its three homes; assisted trends read backwards (W1-F10, W4-F6, W4-F15) |

## Synthesizer notes

Three observations from the merge itself, not findings from the tracers.

1. worker-4.md's own severity tally is stated three times and disagrees with
   itself (lines 105, 107, 109). I used its corrected line 109: safety 8,
   blocks-core-loop 2, wrong-data 3, friction 3, cosmetic 1.
2. worker-2.md's case-06 trace points at "W2-F1/F2" for the per-side gap; the
   per-side finding is actually W2-F11. The finding is real, the cross-reference
   is wrong.
3. I kept every tracer's severity grade rather than re-grading. L-06 (per-side)
   is the one I would argue with: it is graded friction, but W2-F11's own note
   says the schema columns can never be populated, so a unilateral set is
   recorded as a total with the split lost. That reads closer to wrong-data.
