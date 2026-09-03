# 20 use cases, rising difficulty

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

System under test: `docs/build-plan.md`, release 1. No code exists. Each case is a script
written to find a bound; `Agent: ???` marks a turn the plan does not specify, which is the
finding. Refs: `(plan sN)`, `(04 s2.4)` research note, `(dec "X")` decision row of
2026-09-01. Do not fix the breaks. Tracers do that.

## Index

| NN | Title | Axes | Plan sections |
|---|---|---|---|
| 01 | Three sets, nothing unusual | core loop | s2, s1.1, s1.2 |
| 02 | Dictated into a chalked phone | grammar, voice | s2, s4 |
| 03 | `20x8`, `8x40`, and `squhat` | ambiguity, grammar holes, undo | s2, s1.1, s1.2 |
| 04 | Rings in the garage | calisthenics, bw grammar, variation index, missing template | s1.1, s1.3, s4 |
| 05 | Hotel gym, kilos only | units mid-history, location, swap | s1.1, s1.2, s1.4 |
| 06 | Otago and Couch to 5k | program page format, time-based sets, level progression, rest nodes | s1.5, s1.1, s4 |
| 07 | Third fail, deload declined | progression, stall, masters | s1.5, s4, s7 |
| 08 | Swings on the minute | EMOM and ladders, time-capped sessions, set index | s1.5, s1.1, s2 |
| 09 | Carries, Pendlay rows, Nordic curls | catalog miss, no aliases field, distance and time, per-side | s1.1, s1.3, s4 |
| 10 | Marco runs Codex | packaging A, harness | s5, s6 |
| 11 | The PC sleeps, the basement eats sets | phone path, idempotency, lost writes, ordering | s5, s1.1, s6 |
| 12 | 11:40pm, second session, then Tokyo | session identity, timezone, week | s1.2 |
| 13 | "I did the rest at home" | lifecycle, abandoned, retro | s1.2, s7 |
| 14 | Fix a set the program already used | rollback, block end | s2, s4, s1.5 |
| 15 | Free plan, 3,400 rows, alias collision | data limits, catalog miss, packaging B | s1.1, s1.3, s5 |
| 16 | Cold start into a clearance gate | intake, screen, refusal | s3, s4 |
| 17 | Sharp knee on set 2 | safety mid-session, limits lifecycle | s1.1, s1.6, s4 |
| 18 | 16, a pop, and a tight chest | red flags, Ottawa, minors | s3, s4 |
| 19 | Crash 48 hours later | PEM, off switch, scope | s1.6, s4 |
| 20 | Two clients, one conversation | multi-client, concurrency, HRT, everything | s1.6, s5, s8 |

## 01. Three sets, nothing unusual (difficulty 01)

**Persona.** Sam, 6 weeks into GZCLP, lb, one gym, phone.
Types short, knows the confirm line by heart.

**Bound probed** Core loop turn shape and session open (plan s2), (plan s1.2 lifecycle).

**Script**
```
User:  what do i have today
Agent: Day B (Lower) - 5 exercises, ~40 min.
       Squat 3x5 @ 185 (up 5 from last). Last time: 180 x5,5,5.
       Warm-up: bar x5, 95x5, 135x3, 165x2 (165 = bar + 45,15).
User:  185x5
Agent: Squat set 1 logged, 185x5. Set 2 at 185.
User:  5
Agent: ???
```

**Expected per plan**
- Session flips to `open` on the first logged set (plan s1.2).
- Confirm line is `<exercise> set <n>, <weight>x<reps>. <next target>.` (plan s2).
- Close appends `5/5/5` and the outcome (04 s5.5); PR hint only within one increment (dec "S25").

**Break hypothesis** Readiness is offered at open and skippable (dec "S28"), but the opener
is exactly three lines and phase 4 asserts that (plan s6). No fourth line exists.

## 02. Dictated into a chalked phone (difficulty 02)

**Persona.** Sam again, hands chalked, phone on the floor, dictating.
Never punctuates, never says "at".

**Bound probed** Voice grammar as first-class (dec "S24 voice input is real"), (04 s5.4).

**Script**
```
User:  bench one thirty five five five four
Agent: ???
User:  one thirty five by five at eight rpe
Agent: ???
User:  bench press one three five times five
Agent: ???
```

**Expected per plan**
- `by`, `at`, `*` and spelled `one`..`twenty` parse as digits (plan s2), (04 s5.4).
- `@` is not required for RPE (dec "S24"), (04 s5.4).
- No punctuation: first number is weight if >= 25, the rest are per-set reps (04 s5.4).

**Break hypothesis** "One thirty five" is two tokens outside `one..twenty` with no composition
rule, "one three five" and "times" are absent, and the heuristic is prose, not the grammar.

## 03. `20x8`, `8x40`, and `squhat` (difficulty 03)

**Persona.** Priya, first session ever. Lateral raises, cable rows.
One hand on the stack, autocorrect on, does not re-read.

**Bound probed** Rule A's grey band and its uncovered region against (dec "S26 weight/reps order"), plus never-reject and `undo` (04 s2.4), (04 s2.6), (04 s2.5 ex 20).

**Script**
```
User:  lateral raise 20x8
Agent: ???
User:  rows 8x40
Agent: ???
User:  squhat 1 85 x 5
Agent: ???
User:  undo
Agent: ???
User:  lateral raise 20x8      [next week]
Agent: ???
```

**Expected per plan**
- Rule A: first >= 25 is weight x reps; first <= 10 with second <= 30 is sets x reps; 11-24 asks.
- The plan guesses from the last set instead (plan s2), (dec "S26"), storing it in `Overrides`.
- An unparseable line is a verbatim note, never a rejection (04 s2.6), (plan s1.1 `Notes`).

**Break hypothesis** Day one has no last set, so the guess has no input and the two rules
contradict; `Overrides` is per session, so the answer dies at close; `8x40` matches no
branch of rule A; `undo` never says whether a note is an entry.

## 04. Rings in the garage (difficulty 04)

**Persona.** Ben runs the r/bwf Recommended Routine off rings and a doorway bar. No
plates, one 25 lb vest, a set of bands. Progress means a harder variation.

**Bound probed** `variation_chain` and `variation_index` as the difficulty axis (plan s1.3), (delta 5), against `bw` grammar (04 s2.4 rule F), `load-adjust` outputs (plan s4), and the absent rings template (16).

**Script**
```
User:  pullups bw+25 5/5/4
Agent: ???
User:  l-sit 3 x 20 seconds
Agent: ???
User:  ring dips, green band assist, 8/8/6
Agent: ???
User:  pullups are easy now, write me a rings progression
Agent: ???
```

**Expected per plan**
- `bw`, `bw+25`, `bw-25` parse; stored value is added load plus a bodyweight snapshot (rule F).
- `variation_chain` and `variation_index` make load and variation one axis (plan s1.3), (delta 5).
- `library/` ships r/bwf RR; `program-design` selects from it and never invents (plan s4).

**Break hypothesis** A band is not a number and `band` is cut (plan s7); an L-sit is seconds
with no duration property; `load-adjust` has no `variation_index` branch; no rings template.

## 05. Hotel gym, kilos only (difficulty 05)

**Persona.** Dana, four nights away. Hotel gym has kg dumbbells to 40, a bench, no
barbell, no rack. Her profile and 14 months of history are lb.

**Bound probed** Unit per row with no normalisation (dec "S11 units"), (plan s1.1) against a `Locations` row created mid-session and a swap (plan s1.4), (04 s2.5 ex 19).

**Script**
```
User:  hotel gym, dumbbells only, kilos, up to 40
Agent: ???
User:  swap goblet squat
Agent: ???
User:  32kg x12
Agent: ???
User:  12
Agent: ???
User:  whats my best squat
Agent: ???
```

**Expected per plan**
- `Unit` is on each row, never normalised (plan s1.1); a suffix beats the default (rule I).
- `Locations` holds plate inventory, bar weight both units, fixed stacks, min increment (plan s1.4).
- `swap` keeps the set scheme; the decision lands in `Overrides` (04 s2.5 ex 19), (plan s1.2).

**Break hypothesis** No skill creates a `Locations` row (plan s4), the bare `12` has no unit
inheritance, and "best squat" compares lb to kg with a conversion the plan forbids.

## 06. Otago and Couch to 5k (difficulty 06)

**Persona.** Margaret, 72, runs the Otago falls-prevention programme her physio named,
plus Couch to 5k intervals. Rest days are scheduled between.

**Bound probed** The program page line grammar (plan s1.5), (04 s1.2) against time-based sets, progression by exercise level, and `advance: on-log` on rest nodes (dec "S22"), (16).

**Script**
```
User:  what do i have today
Agent: ???
User:  did c25k week 3 day 2, 90 second runs
Agent: ???
User:  single leg stand 30 seconds each side, level 3
Agent: ???
User:  i feel fine, i want to walk anyway    [Wednesday, a rest node]
Agent: ???
```

**Expected per plan**
- Programs are plain-text pages read whole in the line grammar of (04 s1.2), (plan s1.5).
- Rest days are `## R - Rest` nodes; the header carries `advance: on-log` (plan s1.5), (dec "S22").
- `library/` ships Otago and Couch to 5k; `program-design` never invents (plan s4), (16).

**Break hypothesis** The page format cannot express a 90-second interval, a 30-second hold,
or progression by level (16), so two shipped templates cannot be written in it, and `Sets`
has no duration property. `advance: on-log` also gives the cursor no way off a rest node.

## 07. Third fail, deload declined (difficulty 07)

**Persona.** Ruth, 58. Bench has stalled at 135 for three sessions.
Recovers slowly and knows it.

**Bound probed** Deloads ask first (dec "S19 progression") against per-exercise fail state (plan s1.5) and the cut masters pack (plan s7).

**Script**
```
User:  135 5/5/3
Agent: ???
User:  no, keep it at 135
Agent: ???
User:  135 5/5/3            [next session]
Agent: ???
```

**Expected per plan**
- Slashes are per-set reps and close the exercise (04 s2.4 rule C).
- Fail counter, training max and last-deload date are per-exercise state (plan s1.5).
- Small bumps auto-apply; deloads and -10% drops ask first (dec "S19"), (04 s5.5).

**Break hypothesis** There is no state for "deload offered and refused", so the counter climbs
and the ask repeats, which is the nagging the design forbids (04 s1.4), (dec "S23").

## 08. Swings on the minute (difficulty 08)

**Persona.** Ade follows the r/kettlebell wiki and Simple & Sinister.
Swings every minute on the minute, get-ups, clean-and-press ladders.

**Bound probed** Program grammar and the confirm line against EMOM, ladders and time-capped sessions (plan s1.5), (plan s2), (16), with `Set index` half the idempotency key (plan s1.1).

**Script**
```
User:  what do i have today
Agent: ???
User:  swings 24kg 10 emom
Agent: ???
User:  ladder 1-2-3 x5 rounds, 32kg
Agent: ???
User:  getups 5 each side, 20 minutes total
Agent: ???
```

**Expected per plan**
- `library/` ships the kettlebell wiki and Easy Strength; `program-design` never free-generates (16).
- Programs are read whole in the line grammar (plan s1.5), (04 s1.2).
- One row per set; `Set index` is order and half the idempotency key (plan s1.1), (04 s7.3).

**Break hypothesis** EMOM and ladder schemes have no form in the program grammar (16), so
two shipped templates cannot be written down; `10 emom` needs a clock the design refuses to
fake (04 s5.2); a 1-2-3 ladder is fifteen sets from one line with no deterministic index.

## 09. Carries, Pendlay rows, Nordic curls (difficulty 09)

**Persona.** Tom trains for strength he uses: carrying, dragging, lifting off the floor.
Zercher squats, farmer carries, Pendlay rows, Nordic curls, get-ups.

**Bound probed** Catalog miss and the absent aliases field in the free-exercise-db seed (plan s1.3), (15) with `Exercise` a required relation (plan s1.1); distance and duration sets; per-side rows; no loaded-carry template (16).

**Script**
```
User:  zercher 185x5
Agent: ???
User:  farmer carry 2x40m with the 70s
Agent: ???
User:  pendlay row 135 5/5/5
Agent: ???
User:  turkish get up 24kg 5 left 3 right
Agent: ???
User:  write me a carry programme for the next 6 weeks
Agent: ???
```

**Expected per plan**
- Catalog seeded from free-exercise-db, 876 entries, `aliases` a multi-select (plan s1.3), (15).
- Rule J matches today's day first, prompting only on two matches in that day (04 s2.4).
- `Side`, `reps_left`, `reps_right` on the row (plan s1.1); `program-design` never invents (plan s4).

**Break hypothesis** The seed has Zercher Squats but no aliases field (15), so names match
by fuzz alone; Pendlay row and Nordic curl are in neither source and nothing creates a row
while `Exercise` is required; distance, duration and per-side have no property (16).

## 10. Marco runs Codex (difficulty 10)

**Persona.** Marco, Sam's friend, uses Codex CLI, no Claude subscription.
Cloned the public repo, made a free Notion account, duplicated the template.

**Bound probed** Packaging bridge for the third target (plan s5), (dec "Plugin targets release 1"), against what phase 7 checks (plan s6).

**Script**
```
User:  set me up
Agent: ???
User:  what do i have today
Agent: ???
User:  185x5
Agent: ???
```

**Expected per plan**
- Codex reads `.agents/skills/`, one generated symlink per skill (plan s5), (13 s7).
- `make skills` generates the symlinks and the ZIP; `AGENTS.md` at the repo root (plan s5).
- Notion arrives through `.mcp.json` (plan s5).

**Break hypothesis** Generated symlinks are not committed, `.mcp.json` is Claude Code's file
and gives Codex no Notion path, and phase 7 tests flavours A and B only (plan s6).

## 11. The PC sleeps, the basement eats sets (difficulty 11)

**Persona.** Sam, Remote Control into his home PC, which sleeps 20 minutes in.
The rack sits in a basement corner with no signal, so his phone retries upstairs.

**Bound probed** Phone path (dec "Phone path"), (plan s5) against lost writes, duplicate writes and arrival order (04 s5.3), (04 s7.3), (04 s7.4), (plan s6 phase 3).

**Script**
```
User:  185x5                [m1, no reply; PC asleep]
User:  185x5                [m1 retried by the client]
User:  185x5                [user retypes; new id m2]
Agent: ???
User:  4                    [m3, sent second, arrives first]
User:  5                    [m4, sent first, arrives second]
Agent: ???
User:  where was i          [40 min later]
Agent: ???
```

**Expected per plan**
- No session times out; a long gap gets one ask; "where was I" is one line (04 s5.3).
- A re-sent message id writes nothing and replays the confirmation (04 s7.4), (plan s6 phase 3).
- `client_key` is `sha1(session + exercise + set_index + attempt)`, query-before-create (04 s7.3).

**Break hypothesis** Dedupe keys on message id, so a retyped line is a new id and a second
row, while `client_key` holds a `set_index` two racing writes read from one cursor. Nothing
detects a lost write, arrivals are unordered, and the 3-hour gap rule is never in the plan.

## 12. 11:40pm, second session, then Tokyo (difficulty 12)

**Persona.** Nadia, night-shift nurse. Trained at 7am, back at 23:40 for a second
session, flies to Tokyo the next morning.

**Bound probed** Session identity, local date, timezone and `week_index` (plan s1.2), (02 s8 two-a-days).

**Script**
```
User:  what do i have today            [23:40 local]
Agent: ???
User:  225x5
Agent: ???
User:  5                               [00:15 local]
Agent: ???
User:  what do i have today            [Tokyo, +16h]
Agent: ???
```

**Expected per plan**
- `id` is opaque and two-a-days must be legal (plan s1.2), (02 s8).
- `Date` is local date only; an 11pm session belongs to that day (plan s1.2).
- `Timezone` is IANA on the session; `week_index` derives from the local date (plan s1.2).

**Break hypothesis** `Date` is fixed at open, so nothing says which date the 00:15 set takes;
both of the day's sessions share `Date` and `Day`, so finish-or-advance (dec "S21") cannot
tell "still open" from "second today"; and no timezone owns the week boundary.

## 13. "I did the rest at home" (difficulty 13)

**Persona.** Priya left the gym after 2 of 5 exercises on Tuesday, finished the other
three at home that night, came back Thursday.

**Bound probed** Partial session and abandon (dec "S21 partial session"), (plan s1.2), against cut history import (plan s7), (dec "S8 history import deferred").

**Script**
```
User:  what do i have today
Agent: Day B is still open, 2 of 5 done. Finish it, or advance to Day A?
User:  advance
Agent: Day B marked done at 2 of 5. Day A (Upper) - 5 exercises, ~40 min. ...
User:  wait, i did the other 3 at home on tuesday night
Agent: ???
```

**Expected per plan**
- A partial session stays `open`; the agent asks finish-or-advance at the next open (dec "S21").
- Advance sets `abandoned`, marks slots `not done`, advances the cursor (plan s1.2), (04 s3).
- Corrections append and the last write wins per key (04 s7.2).

**Break hypothesis** There is no path back: the cursor moved, the session is `abandoned`, the
grammar cannot log into a past one, `fix` needs a row, and import is cut (plan s7).

## 14. Fix a set the program already used (difficulty 14)

**Persona.** Dana, driving home, realises squat set 3 was 4 reps and not 5.
The session closed 20 minutes ago and it was the last week of the block.

**Bound probed** Rollback across a `load-adjust` write and a block boundary (04 s2.5 ex 20-21), (plan s4), (plan s1.5 per-exercise state).

**Script**
```
User:  done for today
Agent: Day B closed. 4 of 5, 52 min. Next up: Day A (Upper).
       Session RPE 0-10? (skip if you like)
User:  7
User:  fix squat set 3 was 4 reps not 5
Agent: ???
User:  undo
Agent: ???
```

**Expected per plan**
- `fix` amends a logged set (04 s2.5 ex 21); corrections append, last write wins (04 s7.2).
- Bumps apply at close and `load-adjust` writes the next target into `program/current` (dec "S19").
- Block end re-fires `program-design` (plan s4).

**Break hypothesis** `load-adjust` already wrote the next target and moved per-exercise state,
which has no undo (plan s1.5); and after a close, `undo`'s last entry is the session RPE.

## 15. Free plan, 3,400 rows, alias collision (difficulty 15)

**Persona.** Jess, no terminal, claude.ai Free, ZIP skills, Notion connector over OAuth.
14 months of daily logging, about 3,400 set rows.

**Bound probed** Catalog miss and alias collision at scale on flavour B (plan s1.3), (15), (plan s1.1 required relation), plus Notion throughput on Free (01 s3 request limits), (plan s5).

**Script**
```
User:  hammer strength iso row 3 plates x10
Agent: ???
User:  rdl 225x8
Agent: ???
User:  press 95x5
Agent: ???
User:  whats my best squat ever
Agent: ???
```

**Expected per plan**
- Catalog seeded from free-exercise-db with `aliases` as a multi-select (plan s1.3).
- Rule J matches today's day first, prompting only on two matches in that day (04 s2.4).
- Never reject a line (04 s2.6); flavour B runs on Free with no terminal (plan s5).

**Break hypothesis** The seed has no aliases field (15), so `rdl` reaches Romanian Deadlift
via a table nobody owns; nothing creates a row for the unknown machine while `Exercise` is
required; and "best squat ever" pages 3,400 rows at ~3 req/s with no aggregation.

## 16. Cold start into a clearance gate (difficulty 16)

**Persona.** Ana, never trained, 11 weeks postpartum, gets dizzy standing up fast.
Wants something to do today.

**Bound probed** Intake asks all 22 groups with no defaults (dec "Intake asks every profile question"), (plan s3), against the clearance branch (00-open-q T7), (07 s1.1).

**Script**
```
User:  set me up
Agent: (name/pronouns, lb or kg, jurisdiction, then PAR-Q+ Q1-Q7 verbatim)
User:  yes to 4
Agent: ???
User:  also im 11 weeks postpartum
Agent: ???
User:  just give me something while i wait for the doctor
Agent: ???
User:  fine. 45x8
Agent: ???
```

**Expected per plan**
- All 7 PAR-Q+ questions word for word, follow-ups only on a YES (dec "T3"), (plan s6 phase 5).
- Clearance state and PAR-Q+ date land in `config/limits`, expiring at 12 months (plan s1.6).
- Nothing programme-shaped before clearance; light walking only; hard refusal (00-open-q T7).

**Break hypothesis** Twenty-two question groups at two to four per turn is eight-plus turns
before a single set exists, with no early exit and no home for a half-finished intake. And
clearance blocks `program-design` while nothing gates `session-runner`.

## 17. Sharp knee on set 2 (difficulty 17)

**Persona.** Sam, mid-squat, second working set.
Sharp pain on the left side, no pop, gone by the time he finishes typing.

**Bound probed** Pain lifecycle from set row to limits entry to next program (plan s1.1 `Pain flag`), (plan s1.6), (plan s4 `pain-triage`).

**Script**
```
User:  sharp pain left knee on that rep
Agent: ???
User:  its fine now, im carrying on
Agent: ???
User:  what do i have today          [three days later]
Agent: ???
```

**Expected per plan**
- `pain-triage` pre-empts everything on any mention of pain (plan s4).
- Output is a dated `config/limits` entry plus a session halt (plan s4), (plan s6 phase 6).
- An open entry blocks that movement, cleared only by the user (plan s1.6); hand-off wording.

**Break hypothesis** `Pain flag` is `none | niggle | stop` with nothing mapping free text to
a level; "session halt" collides with "no session times out" (04 s5.3); and nothing says a
limits entry is a config change big enough to re-fire `program-design` (plan s4).

## 18. 16, a pop, and a tight chest (difficulty 18)

**Persona.** Theo, 16, gave his age at intake, trains with his school team.
Texts the agent from the field.

**Bound probed** Red flags and the Ottawa criteria (00-synthesis-trainer "The Ottawa rules") against no age gate (dec "T18 final") and the scope table.

**Script**
```
User:  heard a pop in my knee and i cant put weight on it
Agent: ???
User:  also my chest feels tight and im out of breath
Agent: ???
User:  can you just tell my coach what to program for me
Agent: ???
```

**Expected per plan**
- Inability to bear weight is a hard stop and a referral, tested "both immediately and in the ED".
- Chest discomfort is stop, emergency or same-day care; hard refusal, no override, hand-off wording.
- Age is an ordinary profile fact; LTAD limits are trainer guidance only (dec "T18 final").

**Break hypothesis** Ottawa is validated in adults, paediatric application was never
searched, and `ref/red-flags` ships with no age branch (plan s4). Two red flags arrive with
no ordering rule, and programming for an unscreened coach has no row in the scope table.

## 19. Crash 48 hours later (difficulty 19)

**Persona.** Kim, long COVID, flattened for two days after Tuesday's session.
Feels fine today, wants the weights back on, wants to be 10 kg lighter by June.

**Bound probed** PEM hard stop and the `progression: manual` off switch (00-synthesis-trainer "PEM hard stop"), (plan s1.6), against the override tiers and the scope table.

**Script**
```
User:  tuesday wiped me out for two days, worse than the session itself
Agent: ???
User:  turn the weights back on, i feel fine today
Agent: ???
User:  and i need to be 10kg down by june, whats my calorie target
Agent: ???
```

**Expected per plan**
- A crash 12 to 72 hours after activity stops all progression; decrease-on-failure inverts.
- `load-adjust` reads `progression: manual` first; only the user can clear it (plan s1.6).
- A calorie target is hard refusal; react to a disordered-eating cue, do not re-screen (T26).

**Break hypothesis** "Only the user can clear it" and "the user clearing it is the PEM
failure mode" are the same sentence, and the flag has no friction. Nothing owns detecting a
crash either: `pain-triage` triggers on pain, numbness, a pop or swelling (plan s4).

## 20. Two clients, one conversation (difficulty 20)

**Persona.** Priya, personal trainer, claude.ai Free, ZIP skills, one Notion workspace.
Coaching Mia in the gym (California, feminizing HRT month 3, 5k goal, kg) while editing
Rob's program on her laptop (Ontario, lb).

**Bound probed** Multi-client identity, concurrency, jurisdiction and audit (dec "T2 users"), (plan s8 open point 3), against the HRT branch, units and idempotency, on flavour B.

**Script**
```
User:  [Mia's phone]  60kg 3x8
Agent: ???
User:  [Priya, laptop] change robs bench to 3x5 from next week
Agent: ???
User:  [Mia] my 5k pace is 40s slower than march, am i overtraining
Agent: ???
User:  [Mia, signal returns] 60kg 3x8
Agent: ???
User:  [Mia] my left calf is swollen and hot
Agent: ???
User:  [Priya] does mias federation let her race in june
Agent: ???
```

**Expected per plan**
- Weight is consumed first, so the following `3x8` is sets x reps (04 s2.5 ex 22); a resend is a no-op.
- Feminizing HRT at 0 to 6 months with an endurance drop is hemoglobin, not fatigue: do not deload.
- One-sided calf swelling is urgent, higher prior on estrogen; eligibility only if asked (dec "T23").
- Jurisdiction is per client, not per install; the audit log is load-bearing (dec "T2 users").

**Break hypothesis** There is no client entity in the data model: one `config/athlete`, one
`config/limits`, one `program/current` per workspace (plan s1.6), so two unit preferences,
two jurisdictions and two limits sets collide in one page. One shared conversation defeats
`source_message_id`, and the audit log is load-bearing and never defined (plan s8).

## Assumptions

Global instruction says ask when unclear. The brief forbids asking, so the calls are here.

1. Difficulty is axis count and depth, not user skill: case 16's beginner loads more of the
   design than case 01's expert. `Agent: ???` is a finding, not laziness.
2. Catalog and library facts come from notes 15 and 16: 876 entries, Zercher Squats present,
   no aliases field, Pendlay row and Nordic curl absent, 10 templates with no rings or carry.
3. Plan s8 open points are holes, not decisions; cases 15 and 20 lean on them. Flavour B is
   the trainer's path in case 20; flavour A is cases 10 and 11.
4. No case argues for a cut feature. Cases 04, 07 and 13 show a user wanting one.
5. The repo has no commits, so no head SHA anchors these. Written against
   `docs/build-plan.md` as of 2026-09-01.
