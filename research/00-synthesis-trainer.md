# Synthesis: what the trainer agent should be

Covers research notes 06 to 12, plus note 03 for the load rules the skills call.
The system half (storage, data model, logging UX) is synthesized separately in
`00-synthesis-system.md`, which covers notes 01 to 06. Written 2026-08-31.

Every claim points at the note and section it came from. Where two notes
disagreed, the disagreement is named and settled in the tensions section.
UNVERIFIED tags are carried over exactly as the source notes wrote them.

---

## TL;DR

1. **Ship seven skills.** `trainer-core`, `intake`, `screen`, `program-design`, `session-runner`, `load-adjust`, `pain-triage`. The sibling ships six; `screen` is carved out of `intake` (07 section 1).
2. **Retrieve and apply, never generate.** Every measured LLM failure here is a failure of free generation (06 "Evidence on LLM and AI coaching"). Programs from a library, loads from 03's rules, refusals from a fixed list.
3. **No test day by default.** Screen, start conservative, read weeks 1 to 3 of the log as the baseline (07 open q2). Four branches override, listed in the flow table.
4. **Eleven global red flags stop the session and refer**, no judgement call (10 TL;DR). Clearance runs the ACSM 2015 algorithm once, not a banner on every message (06 "Disclaimers").
5. **PEM hard stop.** Symptoms worsening 12 to 72 hours after activity switch every automatic progression rule off (10 ME/CFS card, NICE NG206). 03's engine needs a real off switch built.
6. **HRT-aware branch.** An endurance drop 0 to 6 months into feminizing HRT is hemoglobin, not overtraining. Check HRT status before deloading anyone (11 section 4.5).
7. **Disclose once**, at first contact and in exported documents. Never per message (12 section 8.2, 06 "Disclaimers").
8. **The agent may say no**, including to the owner. Hard refusal on red flags and out-of-scope; logged pushback with an override elsewhere (12 section 8.4).
9. **Body composition off for everyone.** Body fat percentage never reported at all (07 section 4.5, 11 section 6.4).
10. **ACSM 2026 re-anchors the numbers.** ~80% 1RM and 2 to 3 sets for strength, ~10 sets per muscle per week for hypertrophy, 30 to 70% 1RM for power, every muscle twice a week. Failure and complex periodization not required.
11. **28 open questions** at the end, each with a default so silence is still an answer. Two have no safe default.

---

## Skill catalog

Shaped for a Claude Code skill file: name, trigger, what it reads, what it
writes, which reference it loads. "R1" is release 1, meaning what one lifter
running preset routines actually needs.

The sibling synthesis ships six skills (00-synthesis-system "Skill list for the
first release"). This file adds a seventh, `screen`, and explains why below the
table.

| Skill | Trigger | Reads | Writes | Loads | R1 |
|---|---|---|---|---|---|
| `trainer-core` | Every coaching turn. Loaded unconditionally by all others | `config/athlete`, `config/limits`, last 7 days of sessions (06 section 1) | Nothing. It gates | `ref/scope-and-refusals`, `ref/red-flags`, `ref/wording` (12 section 1, 10 section 2, 11 section 6.5) | Yes |
| `intake` | First run, "set me up", life change | Conversation. On re-intake, existing config (06 section 2) | `config/athlete`, `config/limits`, `config/preferences` | `ref/intake-script` (07 section 2 blocks A-G, 11 section 6.3 additions, 09 section 9 athlete prompts) | Yes |
| `screen` | Inside `intake`, before any program. Re-fires on any health change | PAR-Q+ answers, current activity, known disease, planned intensity | Clearance state and date into `config/limits` | `ref/screening` (07 sections 1.1 to 1.4, 10 section 1 clearance rule) | Yes |
| `program-design` | "Make me a plan", block end, config change big enough to invalidate the plan | `config/*`, `library/`, last block adherence (06 section 3) | `program/current`, `program/history/<date>` | `ref/programming-numbers` (08 all goals, 06 section 3, ACSM 2026), `library/` | Yes |
| `session-runner` | "What am I doing today", "next", "done", a logged set | `program/current`, today's partial log, recent history (06 section 5) | The session log: load, reps, RIR, notes | `ref/warmup` (06 section 4 RAMP + plate maths, folded in for R1) | Yes |
| `load-adjust` | End of set, end of exercise, end of session | Today's sets, that lift's last 3 sessions, `config` increments (06 section 7) | Next session's target load in `program/current` | `ref/progression-rules` (03 consolidated decision table) | Yes |
| `pain-triage` | Any mention of pain, numbness, tingling, a pop, swelling. Pre-empts everything | What the user said, `config/limits` (06 section 9) | Dated entry in `config/limits`, session halt | `ref/red-flags` (10 TL;DR, 06 "Red flags"), `ref/referral-targets` (12 section 9) | Yes |
| `substitute-exercise` | "No rack", "that hurts", "gym is packed" | Exercise to replace, equipment list, `config/limits` (06 section 6) | The swap, in today's log | `ref/movement-patterns` (06 section 6, taxonomy UNVERIFIED, book-sourced only) | No |
| `deload` | Block boundary, or fatigue markers | Last 3 weeks of logs, adherence (06 section 10) | A deload week into `program/current` | `ref/progression-rules` deload block (03 "Deload"), `ref/hrt-adjustments` (11 section 4.5) | No |
| `re-entry` | A gap in the log | Gap length, last completed session (06 section 11) | Adjusted loads, a re-entry note | `ref/progression-rules` time-off table (03 "Time off", DERIVED) | No |
| `plateau-review` | Two consecutive load reductions on one lift | That lift's full history, weekly volume (06 section 12) | Dated plateau note with the cause chosen | `ref/progression-rules` plateau block (03 "Plateau detection", DERIVED) | No |
| `weekly-review` | End of the training week | The week's sessions vs plan (06 section 13) | `reviews/<date>` | `ref/realistic-rates` (12 section 7.2) | No |
| `adherence` | A missed session, "I can't get started" | Adherence trend, stated reasons (06 section 14) | If-then plan into `config/athlete` | `ref/adherence` (12 sections 4.1 to 4.9) | No |
| `technique-cues` | "Am I doing this right" | The exercise, what the user described (06 section 8) | A note on the exercise if a cue sticks | `ref/cue-library` (12 section 6.1 external focus; craft consensus, unsourced) | No |
| `lifestyle-prompts` | Visibly bad session with no programming explanation | Recent session quality (06 section 15) | A one-line session note | `ref/scope-and-refusals` nutrition block (12 section 1.4) | No |

### Why `screen` is its own skill, not part of `intake`

Three reasons, all from the notes. The PAR-Q+ expires at 12 months and is
invalidated by any new diagnosis or medication, so it re-fires on its own
schedule (07 section 6). Any health change triggers immediate re-screening
outside the intake flow (12 section 7.1). And the measured LLM failure mode is
over-flagging clearance, 53% of errors in the Zaleski study, which is fixed by
running one deterministic algorithm rather than by nervous improvisation (06
"Evidence on LLM and AI coaching"). Screening deserves a file the user can read
and audit.

### The expansion set: friend with a different goal or body

These are not skills, they are reference packs that existing skills load when a
flag is set. `program-design` stays one skill. Each pack is a file it reads.

| Pack | Fires when | Contents | Source |
|---|---|---|---|
| `ref/goals/<goal>` | Primary goal is not general strength | The nine goal sections: dose, variables, progression model, weekly template, common mistakes | 08 goals 1 to 9 |
| `ref/sports/<sport>` | Client names a sport | 24 sport profiles, plus the 8-step needs analysis that generalizes to any sport not on the list | 09 section 6 (20 sports), 09 Appendix B (baseball/softball, rowing, triathlon, team handball), 09 section 1 |
| `ref/seasons` | Client competes | Off/pre/in/post-season doses, competition week, taper, in-season maintenance floors | 09 section 2 |
| `ref/conditions/<card>` | A condition flag in `config/limits` | 26 cards, template Adjust / Avoid / Monitor / Stop signs / Refer when / Evidence | 10 section 3 |
| `ref/hrt-adjustments` | HRT direction and start date recorded | Feminizing and masculinizing timelines, adjustments table, the hemoglobin misread, refer triggers, wording | 11 sections 1 to 4, 6.5 |
| `ref/masters` | Age flag, or masters athlete | Power before strength, longer recovery spacing, higher maintenance dose | 09 section 7 masters, 10 "Older adults" |
| `ref/youth` | Under-18 flag | LTAD constraints. Blocked until the under-18 question is answered (09 open q6) | 09 section 7 youth, 10 "Children and adolescents" |

Release 2 order, by how often the flag actually fires for this user and her
friends: `ref/goals`, `ref/hrt-adjustments`, `ref/conditions` (5 cards, not 26,
per 10 open q4), then `ref/sports`.

---

## Client flow

The order is ACE's competency order and it is not negotiable: rapport, intake,
screen, assess, program, coach, reassess (12 section 3.2). Steps 3 and 7 are the
two most often skipped and the two that protect the client.

```
  1 RAPPORT  ->  2 INTAKE  ->  3 SCREEN  ->  4 BASELINE  ->  5 PROGRAM
                                  |                              |
                            red flag / clearance             6 RUN (sessions)
                                  |                              |
                            stop, refer, hold                7 REVIEW
                                                                 |
                                                        back to 4 or 5
```

### Default per branch

| Step | Healthy lifter, has routines | Friend with a goal from 08 | Athlete from 09 | Client with a 10 card | Client on HRT from 11 |
|---|---|---|---|---|---|
| Intake | Blocks A to G, short form (07 section 2) | Same, plus rank the goals. Two priorities is zero priorities (08 TL;DR) | Same, plus the 6 questions athletes never volunteer (09 section 9) | Same, plus condition, medications, clearance state (10 section 1) | Same, plus name, pronouns, HRT direction and start, surgery restrictions, binding, no-go body areas (11 section 6.3) |
| Screen | PAR-Q+, ACSM algorithm. Most clear with no clearance (07 sections 1.1, 1.2) | Same | Same, plus weight class and growth spurt check (09 sections 8, 7) | Clearance letter must name diagnosis, intensity ceiling, movements to avoid, monitoring, date, clinician (10 section 1) | Same as healthy. HRT is not a clearance trigger. VTE, post-surgical, and binding items go to `config/limits` (11 sections 4.1 to 4.4) |
| Baseline | **No test day.** Conservative starting loads, then weeks 1 to 3 of the log are the baseline (07 open q2) | No test day, except a cardio goal, which gets one field test, Cooper or Rockport (07 section 4.2) | **Test.** 2 or 3 field tests mapped to the qualities and injuries the needs analysis found (09 section 1 step 7) | No test day. Card's monitoring list instead. Never maximal testing on anyone the algorithm routed to clearance (07 section 7 "Must skip") | **Test, and bank it before HRT starts if there is still time.** Baseline is the only reference for what HRT cost (11 section 3.2 row 1) |
| Program | Library template. Cite the author, link the original (06 section 3, "Program library") | Template from the goal's weekly-template table, secondary goals stated out loud as maintenance (08 "Weekly templates") | Season phase sets volume. Test gaps set exercise selection (09 section 1 step 8) | Card's FITT-VP edits applied to a library template. Never train inside a diagnosis the agent invented | Ordinary programming plus the adjustments table. Hold or raise volume, do not deload for hormones (11 section 3.2) |
| Run | `session-runner` plus `load-adjust`. RPE logged, not read, below 1 year training age (03 rule 20, Zourdos 2016) | Same. Progression unit changes per goal: minutes, sets, rungs, not always load (08 TL;DR) | Same, plus session RPE after every session, or 09 section 4's load formulas are decoration (09 open q2) | Same, plus the card's stop signs checked every session | Same. Re-test endurance every 8 to 12 weeks and rewrite targets rather than chasing old PBs (11 section 3.2) |
| Review | Weekly adherence. 4 to 6 weeks progression. 8 to 12 weeks full reassessment (12 section 7.1, UNVERIFIED craft) | Same, plus an observable success test the client agreed to at intake (08 "Goals not on this list") | Same, on block and season boundaries. Never mid-block (07 section 6) | Same, plus re-screen on any medication or health change, immediately, not on the cadence (12 section 7.1) | Same. Never frame a hormonal change as a training failure or a training success (11 section 6.4) |

### Why no test day is the default

07 asks the question and does not answer it (07 open q2). The answer is that a
test battery costs a session, adds fatigue, and is exactly the kind of session an
ADHD client will not show up for. 07 section 6 already says the rule out loud:
"If the answer will not change the program, do not run the test." For a novice
it will not change anything, because a novice's every session is a PR (07 section
5, Rippetoe's definition). The first three weeks of logs give a better number
than one nervous test day, and they cost nothing.

Two branches genuinely need the test. An athlete's plan is written from the gaps
the tests found, so skipping them leaves nothing to write from (09 section 1
step 7). And a pre-HRT baseline is unrepeatable. Roberts 2020 could quantify what
HRT cost only because pre-hormone fitness tests existed (11 section 3.2).

---

## Safety envelope

### Red flags and what happens

The global list is not optional and the agent reads it every session (10 "How to
use this file"). Action is the same for all of them: stop the session now, do
not resume, name a profession, hold the programme where it is.

| Red flag | Action | Source |
|---|---|---|
| Chest pain, pressure or discomfort, at rest or on exertion | Stop. Emergency or same-day care | 10 TL;DR 1 |
| Sudden breathlessness out of proportion to the work | Stop. Same-day care | 10 TL;DR 2 |
| Fainting, near-fainting, unexplained dizziness, new palpitations | Stop. Possible cardiac outflow obstruction or exercise-induced arrhythmia | 10 TL;DR 3, 06 "Red flags" |
| New one-sided weakness, facial droop, slurred speech, sudden severe headache | Stop. Emergency | 10 TL;DR 4 |
| Resting BP 180/110 or higher, measured and repeated | Stop. Clinician before any programme. Do not blur this with the 200/110 testing threshold; use the lower one | 10 TL;DR 5, 10 section 1 |
| Calf pain or swelling on one side, or a new hot swollen joint | Stop. Urgent. Higher prior in a client on estrogen | 10 TL;DR 6, 11 section 4.6 |
| Saddle numbness, bladder or bowel change, progressive leg weakness | Stop. Surgical emergency, decompression is time-critical | 10 TL;DR 7, 06 "Red flags" (cauda equina) |
| Vaginal bleeding, fluid leak, or reduced fetal movement in pregnancy | Stop. Same-day obstetric care | 10 TL;DR 8 |
| Blood glucose at or below 70 mg/dL (3.9 mmol/L), or confusion and sweating in a diabetic client | Stop. Treat per their own plan, then clinician | 10 TL;DR 9 |
| Symptoms crashing 12 to 72 hours after activity | Stop all progression. See PEM hard stop below | 10 TL;DR 10, ME/CFS card |
| Dark urine plus severe muscle pain or swelling 24 to 48h after unaccustomed work | Stop. Exertional rhabdomyolysis, 10 to 30% develop acute kidney injury | 06 "Red flags" |
| Back pain with cancer history, unexplained weight loss, or unrelieved night pain | Stop. Clinician | 06 "Red flags" |
| Pain during any screening movement (an FMS score of 0) | Not a diagnosis, a referral | 07 section 8 item 11 |
| Rising volume plus falling performance plus falling intake | Refer for RED-S. Do not manage it | 12 section 8.4, IOC 2018 |
| Self-harm or suicidality disclosed in any context | Immediate handoff to a human | 11 section 4.6, 12 section 9 |
| Inability to bear weight after acute injury | Fracture screening. **Sourced 2026-09-01** to the Ottawa ankle and knee rules, Stiell et al. See "The Ottawa rules" below for the exact wording | 06 "Red flags", Stiell 1992/1993/1995/1996 |

Hand-off, not decline. A decline leaves the person stuck. Use 12 section 8.5's
template: "That one's outside what I can do. [Specific reason.] The person for
this is a [profession]. In the meantime I can still help with [in-scope thing],
if you want."

### The Ottawa rules

Sourced 2026-09-01, retiring the UNVERIFIED tag on the "cannot bear weight"
red flag. All four papers are Stiell et al. out of the University of Ottawa and
all four are captured in `.kb` (`llmwiki search "Ottawa ankle rules"`).

| Paper | What it is | Cite |
|---|---|---|
| *Ann Emerg Med* 1992;21(4):384-90 | Ankle rule, derivation. 905 adults | [PMID 1554175](https://pubmed.ncbi.nlm.nih.gov/1554175/) |
| *JAMA* 1993;269(9):1127-32 | Ankle rule, refinement and prospective validation. 1,485 adults | [PMID 8433468](https://pubmed.ncbi.nlm.nih.gov/8433468/) |
| *Ann Emerg Med* 1995;26(4):405-13 | Knee rule, derivation. 1,047 adults | [PMID 7574120](https://pubmed.ncbi.nlm.nih.gov/7574120/) |
| *JAMA* 1996;275(8):611-5 | Knee rule, prospective validation | [PMID 8594242](https://pubmed.ncbi.nlm.nih.gov/8594242/) |

**The weight-bearing criterion, in the authors' own words.** The 1992 ankle
derivation identified all 70 malleolar fractures among patients who were "age 55
years or more, had localized bone tenderness of the posterior edge or tip of
either malleolus, or were unable to bear weight both immediately after the
injury and in the ED." The 1995 knee derivation lists five variables, the fifth
being "inability to bear weight both immediately and in the ED (four steps)".

Three details the trainer agent must not lose:

1. **"Both immediately and in the ED" is the actual test.** Not "it hurts to
   walk", not "cannot bear weight now". Someone who limped off the field and is
   still limping meets it. Someone who walked fine at the time does not.
   **Four steps** is the operationalisation the knee rule gives; the ankle
   papers use the same two-timepoint phrasing.
2. **Both rules validated at sensitivity 1.0**, with the estimated probability
   of fracture on a negative rule at 0% (95% CI 0 to 0.8% for the ankle series,
   0 to 0.4% for the knee). That is why this is a hard stop and not a judgement
   call: the rule is built to have no false negatives, at the cost of
   specificity around 0.40 to 0.54. It will send people for imaging who turn out
   fine. That is the design, and for a fitness agent it is the right side to err
   on.
3. **These are triage rules for ordering an X-ray, not a trainer's tool.** The
   agent's use is one-directional: the criterion is met, so stop the session and
   refer. The agent never runs the rest of the rule, never palpates a malleolus,
   and never concludes "negative, carry on". A negative Ottawa rule is a
   clinician's finding, not the agent's.

The rules are derived and validated in **adults**. Paediatric application is a
separate literature and was not searched.

### Scope table

| The agent may | The agent may not | Refer to |
|---|---|---|
| Design and modify exercise programmes | Diagnose anything, including "that's probably just DOMS" | Physician |
| Cue technique, adjust load, schedule sessions | Prescribe rehab for an acute injury, a post-surgical client, or anyone under a physio's active care without that clinician's written plan | Physiotherapist |
| Give general healthy-eating information | Give meal plans, macro targets, calorie targets, or supplement recommendations | Registered dietitian |
| Explain what a clearance letter's limits mean for the plan | Override a clearance letter, or argue a client out of needing one | The clinician who wrote it |
| Say what the research says about a condition and exercise | Tell anyone to take, skip, split, or retime a medication, including insulin, beta blockers, GLP-1 agonists, and hormone therapy | Prescriber |
| Encourage generally | Counsel on mental health, relationships, or substance use | Clinical psychologist |
| Note that a goal looks unsafe, once, kindly | Validate an unsafe goal weight or help design a fast | Eating-disorder specialist |
| Read a federation rule aloud with a link and a date | Have an opinion on whether that rule is fair | Nobody. Stay out |

Sources: 12 sections 1.2 and 9, 10 section 2, 11 sections 4.6 and 6.5. ACE's
nutrition position and NASM's Code of Professional Conduct are the primary
anchors. The NSCA and NASM PDFs are tagged UNVERIFIED in both 06 and 10 because
neither fetched directly.

An AI agent has less standing than a certified trainer, not more. It cannot
observe the lift, cannot palpate, cannot see the person go pale. Every scope
limit that binds a human trainer binds it harder (06 "Scope of practice").

### Disclosure rule

Tension (d) resolved. Both notes are right about different things.

- **At first contact, once**: I am an AI, here is what I cannot do, here is the
  screening that decides whether you see a doctor first. This satisfies EU AI
  Act Article 50, which requires the notice be one a person actually notices
  (12 section 8.2, applies from 2 August 2026 under Article 113).
- **In any exported artifact**: the program document, a shared plan, a review a
  friend might read without having met the agent. A human might reasonably
  forget there (12 section 8.2).
- **On any red flag, every time**: stop, seek care. This is not a disclaimer, it
  is an instruction, and it fires on a specific trigger (06 "Disclaimers").
- **Never per message.** 53% of GPT-4's errors in the Zaleski study were
  over-flagging medical clearance in cases ACSM says need none. A banner the
  user learns to skip is worse than no banner (06 "Disclaimers", 06 "Evidence on
  LLM and AI coaching").

The reconciliation: 12's rule is about *identity*, disclosed once and durably.
06's finding is about *medical hedging*, which is a different thing and should be
replaced by running the screening algorithm properly. Nothing in Article 50
requires repetition.

### May the agent say no

Default: yes, including to the owner. Two tiers.

- **Hard refusal, no override.** Any global red flag. Any request in the "may
  not" column. Programming for a client the screening routed to clearance,
  before that clearance exists. A calorie target. A fast. IDEA's line is that
  the client's safety is the primary responsibility and is never compromised for
  self-interest (12 section 8.4).
- **Logged pushback, override available.** Everything else. The agent states the
  objection once, in one sentence, offers the safer version, and does what the
  user says if the user repeats the request. The disagreement goes in the log
  with a date.

The argument for tier 2 rather than hard refusal everywhere: an agent that
agrees with every request is not being kind (12 section 8.4), but ACSM's Code of
Ethics requires recognising autonomy and the right to make informed decisions
(12 TL;DR rule 8), and autonomy support predicts adherence (Teixeira 2012, same
note). Refusing twice is paternalism. Objecting once and logging it is a trainer.

### PEM hard stop

Tension (e) resolved, and it needs code, not prose.

If a client reports symptoms worsening 12 to 72 hours after activity, every
automatic progression rule switches off and the agent says so out loud (10
ME/CFS card, "Agent rule"). NICE NG206 is unambiguous: a programme "based on
fixed incremental increases in physical activity or exercise, for example,
graded exercise therapy (GET), should not be offered as a treatment for ME/CFS".

What that means for note 03's engine, concretely:

| 03 rule | Behaviour under a PEM flag |
|---|---|
| Rule 2, increase on top of range | Disabled. The planning unit is an energy budget, not a training load |
| Rule 3, hold and add a rep | Disabled |
| Rule 5, decrease on repeat failure | Inverted. Any post-exertional crash means the previous dose was too big. Reduce, do not hold (10 ME/CFS card) |
| Rule 6, deload on stall | Not applicable. There is no stall to detect |
| Plateau detection | Disabled. A good day is not evidence of new capacity |
| Session monitoring | Moves from during-session to 24, 48, and 72 hours after. Heart rate and step count become ceilings, not targets |

10 open q6 asks whether 03's progression engine has an off switch. It does not.
This is the one piece of new machinery this synthesis asks for: a
`progression: manual` state that `load-adjust` reads before anything else, and
that only the user can clear.

The evidence disagreement is narrower than it looks. Nobody credible defends
fixed increments for a client with PEM. The argument is over whether carefully
titrated activity helps or merely does not harm (10 ME/CFS card, both sides
cited).

### HRT-aware branch

Tension (c) resolved. This goes in `load-adjust`, `deload`, and `plateau-review`,
before any fatigue attribution.

```
IF endurance performance has dropped
   AND HRT direction = feminizing
   AND time-on-HRT is between 0 and 6 months
THEN this is hemoglobin, not fatigue.
     Do not deload. Do not count it against the failure counter.
     Recalibrate pace and heart-rate zones by feel.
     Say what is happening and why.
```

The numbers behind it: hemoglobin reaches cis-female range by about 4 months
(153 to 135 g/L in Harper 2025's cohort), while strength is preserved. Measured
running times were about 15% slower, swim times about 5% (11 TL;DR 1 to 3,
section 4.5). Her easy pace is genuinely slower and her heart rate at a given
pace is genuinely higher. An agent that has not accounted for this will read
overtraining, under-recovery, illness, or poor adherence, and will deload a
client who does not need deloading (11 section 4.5).

Three more branches from the same note:

- **Do not cut resistance volume for hormones.** Wiik 2020 showed knee extension
  and flexion strength maintained across 12 months while thigh muscle volume
  fell 5%. Strength is the cheapest thing to defend (11 TL;DR 3, section 3.2).
- **Raise sport volume if she still competes.** The runners who raised training
  volume lost the least performance, r=0.719, p=0.008. Caveat carried over
  unchanged: n=10, mixed retrospective and prospective, self-selected athletes.
  Encouraging, not proven (11 section 3.1).
- **Judge relative and absolute work separately.** Bodyweight-relative work gets
  harder faster than absolute work. Program both, do not compare them (11
  section 3.2, Hamilton 2024).

Mirror case for masculinizing HRT: months 0 to 12 are the best window for
strength progression, so progress load aggressively and volume conservatively,
because tendon lags muscle (11 section 3.2, Wiik 2020). Rising hematocrit means
endurance targets move upward and should be re-tested more often. Do not panic
at a "high" hematocrit read against the wrong reference range (11 section 4.5).

And the thing the agent must say out loud rather than imply: the body does the
feminizing. Fat moves to hips and legs on its own, +42% leg fat, +34% gynoid,
hip +3.2 cm at 12 months (Klaver 2018). Nothing in the training programme causes
or prevents that. Glute hypertrophy is real and adds shape. Spot fat reduction is
not (11 TL;DR 5, 6).

### Data the agent holds

Ask before storing anything health-related, say where it is stored, make
deletion actually delete, and never send it to a third party without per-use
consent (12 section 8.3). For HRT specifically, store direction and start date
only. That is all the programming table needs, and storing less is safer for a
population with real safety risks around data (11 open q7, defaulted below).

---

## ACSM 2026 re-anchor

The main thread verified the new stand: ACSM resistance-training position stand,
MSSE 2026-03-17, the first since 2009. Strength ~80% 1RM at 2 to 3 sets.
Hypertrophy ~10 sets per muscle per week. Power 30 to 70% 1RM. All muscles at
least twice a week. Failure, equipment type, and complex periodization are "not
strictly necessary".

Notes 03 and 08 cite ACSM 2009 in places. Here is what actually moves.

### What changes in note 03

| 03 element | Was | Now | Why |
|---|---|---|---|
| Rule 4, RPE cap | Hold if last-set RPE >= 9.5 two sessions running | Default target is 1 to 2 reps in reserve. Failure is not the goal, so the grinder cap is a backstop rather than the operating point | Failure "not strictly necessary" (ACSM 2026). Matches 03's own conflict resolution, "0-3 RIR", and 08's Refalo 2023 reading |
| Section 8, RP volume landmarks | MEV/MAV/MRV numbers per muscle | Keep the vocabulary for planning. Anchor the target at ~10 sets per muscle per week and progress up from there | ACSM 2026 gives a number where 03 had a coaching heuristic. 03 already warns the landmarks are a heuristic on top of the volume literature |
| Sections 5, 6, 9, 10 (5/3/1, GZCLP, nSuns, Madcow) | Presented as peers | Still usable, now opt-in rather than recommended. The wave and percentage schemes are complexity the stand says is not required | "Complex periodization not strictly necessary" (ACSM 2026) |
| Frequency | Not a rule in 03 | New hard check: every major muscle group twice a week, verified by `program-design` before a block is written | ACSM 2026 says this matters more than a perfect plan (06 section 3.2) |
| Rules 1, 2, 3, 5, 6, 7, 8 | Double progression, decrease, deload, time-off, pain flag | **Unchanged.** The 2026 stand sets dose targets, not the session-to-session decision rule | Nothing in the stand addresses within-block progression logic |

The engine itself stands: double progression in a rep range, capped by effort,
with failure-triggered deloads (03 TL;DR). The sibling synthesis reaches the same
conclusion from the system side (00-synthesis-system "Progression default").

### What changes in note 08

| 08 section | Was (ACSM 2009) | Now (ACSM 2026) |
|---|---|---|
| Goal 2, maximal strength | The 2009 novice/intermediate/advanced ladder: 8-12RM, 1-3 sets, 2-3 d/wk novice, up to 4-5 d/wk advanced | ~80% 1RM, 2 to 3 sets per exercise, for everyone. The ladder survives as a scaffold, still tagged UNVERIFIED in 06 section 3.4 because those figures came from search excerpts |
| Goal 3, hypertrophy | 10-20 sets per muscle per week as the working band | Start at ~10 and progress up. 08's own resolution already said "start low, progress, do not claim an optimum". The stand puts a number on the floor |
| Goal 3, proximity to failure | 0-3 RIR from Refalo 2023 | Unchanged, now backed by a position stand rather than one meta-analysis |
| Goal 8, power | Intent over load, velocity-based framing | 30 to 70% 1RM, fast concentric. A number where 08 had a principle |
| Goal 2, periodization | Williams 2017, small adjusted effect, LP vs DUP no difference | Unchanged in substance and now stronger. Have a plan and a progression rule. Do not sell a model |
| Shared vocabulary, exercise order | 2009: large before small, multi-joint before single-joint, higher before lower intensity | Unchanged. The 2026 stand does not address ordering, and 08's own resolution rule keeps the position stand for framing |
| Goals 1, 4, 5, 6, 7, 9 | Guideline dose, zone models, stretch dose, skill ladders, energy balance, interference | **Unchanged.** The 2026 stand is a resistance-training document. It says nothing about cardio, mobility, skill, or fat loss |
| Currency warning, 08 preamble | "Numbers UNVERIFIED, could not open either abstract" | Resolved. The main thread verified the stand this session. 08's open q1 is answered |

One thing the re-anchor does not fix: the 2009 numbers quoted in 06 section 3.4
remain UNVERIFIED search excerpts. That is not softened here.

**08 open q2 is now answered.** Pelland et al. 2026 was read on 2026-09-01
([PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/), captured in `.kb`,
full working in `03-progression-heuristics.md` "Volume evidence base"). **It does
not move the 10 to 20 band.** 67 studies, 2,058 participants. The posterior
probability that more weekly volume means more hypertrophy *and* more strength
is 100% for both, with diminishing returns and no identified ceiling. So:

- **The ~10 floor stands**, now agreeing with ACSM 2026 from a second direction.
- **The 20 is a recovery ceiling, not an optimum.** The curve is still rising
  where the studies stop. Never present 20 as the evidence-based dose; present
  it as where individual recovery usually gives out, which is what RP's MRV
  vocabulary already meant.
- **Frequency belongs to strength, not hypertrophy.** Pelland finds a clear
  frequency effect on strength (100% posterior) and one compatible with nothing
  at all on hypertrophy. The "every muscle twice a week" line from ACSM 2026
  survives as a way to fit the sets in, not as a hypertrophy lever.
- Only the abstract was read; *Sports Med* is paywalled.

---

## Tension resolutions

Eight cross-note tensions, named in the brief. Verdict only. The detail lives in
the sections above.

**(a) Test at baseline, or read the first three weeks of logs?** Read the logs.
07's own rule settles it: if the answer will not change the program, do not run
the test (07 section 6). Four overrides, listed in the flow table.

**(b) In-season maintenance frequency.** One session a week for young trained
athletes (Rønnestad, 09 section 2). Two for masters, who need a higher dose to
hold hypertrophy (Bickel 2011, 09 section 7). Age is read before season phase.

**(c) HRT-driven endurance loss misread as overtraining.** Feminizing, 0 to 6
months, endurance down means hemoglobin, not fatigue (11 section 4.5). The branch
fires before fatigue attribution in `load-adjust`, `deload`, `plateau-review`.

**(d) Disclose at first contact vs disclaimers hurt.** They were never the same
rule. Identity is disclosed once and durably (12 section 8.2). Medical hedging is
replaced by running the screening algorithm once (06 "Disclaimers").

**(e) ME/CFS vs generic progression.** A `progression: manual` state only the
user can clear, set by any report of symptoms worsening 12 to 72 hours after
activity (10 ME/CFS card, NICE NG206). The one new mechanism this file asks for.

**(f) May the agent say no to the user?** Yes. Hard refusal on red flags and
out-of-scope, no override. Everywhere else: object once, offer the safer version,
comply if the user repeats, log the disagreement (12 section 8.4, 12 TL;DR 8).

**(g) What can the `adherence` skill honestly claim?** The barriers and
facilitators clients report, and the delay-discounting finding. Not that any
tactic works. Detail below.

**(h) Body-composition tracking.** Off for everyone, opt-in once, never raised
again if declined. Body fat percentage is never reported from any method, and
that part is not opt-inable (07 section 4.5, 11 section 6.4).

### What `adherence` may claim, expanded

This is (g)'s detail, because it has no other home in this file.

**May claim.** Adults with ADHD name executive dysfunction, poor self-esteem and
low motivation as the barriers, and enjoyment and company as the facilitators,
from 30 semi-structured interviews (12 section 4.9). Delay discounting is steeper
in ADHD, so a twelve-week body-composition goal is a weak motivator by
construction, not by weakness of will (Marx 2021). Time-management stress broke
adherence in one pilot where 67% of completers reported it.

**May not claim.** That any of the eight derived tactics work. That mapping is
one researcher's inference, tagged UNVERIFIED by its own author, and no
randomised trial of ADHD exercise adherence exists at all (06 "Gaps"). Nor that
chat forms habits: chatbot effects on exercise-habit outcomes were not
statistically significant (06 "Evidence on LLM and AI coaching").

**Must anticipate.** The week 6 to 8 cliff. The meta-analytic effect falls from
SMD 0.29 at eight weeks or under to a non-significant 0.06 beyond, which the
authors call intervention fatigue (06 "Evidence on LLM and AI coaching").

Honest phrasing: "this is what people with ADHD say helps, and here is what we
will try". Never "research shows this works".

---

## Reference material index

Which note section becomes which file. The rule: a skill file holds procedure
and guardrails, a reference file holds numbers and tables. Skills stay short.
References get long and get cited.

| Reference file | Built from | Loaded by |
|---|---|---|
| `ref/scope-and-refusals` | 12 sections 1.2, 1.4, 9; 10 section 2 | `trainer-core`, `lifestyle-prompts` |
| `ref/red-flags` | 10 TL;DR 1-10; 06 "Red flags" | `trainer-core`, `pain-triage`, every session |
| `ref/referral-targets` | 12 section 9 (trigger to profession); 11 section 4.6 | `pain-triage`, `trainer-core` |
| `ref/screening` | 07 sections 1.1 to 1.4 (PAR-Q+ 2025, ACSM algorithm, BP thresholds, contraindications); 10 section 1 (clearance rule, letter contents) | `screen` |
| `ref/intake-script` | 07 section 2 blocks A-G; 11 section 6.3 (ask always / ask because / never ask); 09 section 9 | `intake` |
| `ref/programming-numbers` | 06 section 3; 08 "Shared vocabulary" and all nine goal sections; ACSM 2026 | `program-design` |
| `ref/progression-rules` | 03 "Consolidated decision table", "Deload", "Time off", "Plateau detection", "Increment sizing" | `load-adjust`, `deload`, `re-entry`, `plateau-review` |
| `ref/goals/<1-9>` | 08 goal sections plus their weekly templates | `program-design` |
| `ref/sports/<name>` | 09 section 6 (20 profiles), Appendix B (4 more) | `program-design` |
| `ref/needs-analysis` | 09 section 1 (8 steps), section 9 | `intake`, `program-design` |
| `ref/seasons` | 09 section 2 (phases, in-season doses, competition week, taper) | `program-design` |
| `ref/load-management` | 09 section 4 (session RPE, ACWR and its critique, weekly caps, overtraining monitoring) | `weekly-review`, `deload` |
| `ref/conditions/<card>` | 10 section 3, one file per card | `program-design`, `session-runner` |
| `ref/hrt-adjustments` | 11 sections 1, 2, 3.2, 3.3, 4 | `program-design`, `load-adjust`, `deload` |
| `ref/wording` | 11 section 6.5 (say / not); 12 section 4.10 (phrases to use and avoid) | `trainer-core` |
| `ref/adherence` | 12 sections 4.1 to 4.9 (MI, TTM, SDT, self-efficacy, implementation intentions, lapse handling, ADHD) | `adherence` |
| `ref/scaling` | 12 sections 5.1 to 5.4 (five dials, regression ladders, difficult client types, minimum viable session) | `session-runner`, `substitute-exercise` |
| `ref/cue-library` | 12 section 6.1 external focus, 6.2 when to correct, 6.3 what an agent can coach | `technique-cues` |
| `ref/realistic-rates` | 12 section 7.2; 07 section 5 (training age classification) | `intake`, `weekly-review` |
| `ref/warmup` | 06 section 4 (RAMP, ramp-up sets, plate maths) | `session-runner` |
| `library/<template>` | 06 "Program library to seed". Ship only the free ones: r/Fitness BBR, GZCLP, r/bwf Recommended Routine. Pointer only for 5/3/1, StrongLifts, Starting Strength | `program-design` |

Licensing note carried forward: do not reproduce paid book content. Ship a
pointer and let the user enter their own numbers (06 "Program library").

---

## Open questions for the user

Deduplicated across notes 07 to 12. Forty raw questions. Six are answered
elsewhere in this file or by the sibling synthesis. The remaining 34 collapse to
28 rows. Notes 03 and 06 were deduplicated by the sibling synthesis and are not
re-asked here.

**Already answered, so not re-asked.** Units are lb (system q11). Intake output
lives in Notion child pages (system q31, answering 07 q6). Streaks are out
(system q23, answering 12 q7). The ACSM 2026 full text was verified this session
(answering 08 q1). The PEM off switch is settled in tension (e) (answering 10
q6). The Yun 2023 DOI is a research gap, not a user decision, and sits in the
unverified list (11 q1).

| # | Question | Proposed default | From |
|---|---|---|---|
| T1 | Which country's rules govern this? | **Cannot default.** Fallback if silent: the stricter US line (ACE scope, HIPAA-standard handling), which is what notes 10 and 12 already assume | 10 q1, 12 q1 |
| T2 | Just you, or friends with their own clients? | You plus friends running their own logs. Not trainers with clients. Multi-client use makes the audit log load-bearing | 10 q2, 12 q2 |
| T3 | PAR-Q+ verbatim in chat, or a form you fill in yourself? | Verbatim, but split: 7 questions at first run, follow-ups only on a YES. It is one heavy interaction once a year | 07 q1 |
| T4 | Test at baseline, or read the first 3 weeks of logs? | Read the logs. Test only for the four overrides in tension (a) | 07 q2 |
| T5 | Is video in scope at all? | No for release 1. Everything in 07 section 3 that needs video is deferred, and 07 section 7 already assumes this | 07 q3 |
| T6 | Body composition: excluded, or opt-in? | Off for everyone, opt-in once. Body fat percentage never, from any method | 07 q4, 11 q3 |
| T7 | When screening says "see a clinician", what does the agent do? | Write nothing programme-shaped. Offer light-intensity walking only, which ACSM's own permissive position supports for most adults. Gate everything else behind a user-confirmed clearance flag with a date | 07 q5 |
| T8 | Store the ExRx and Symmetric Strength percentile tables locally, or look them up? | Neither in release 1. They only matter for advanced classification, which release 1 does not need | 07 q7 |
| T9 | Program mobility only against a named restriction, or as a general habit? | Against a named restriction. The evidence is much weaker than the volume of content suggests, and general mobility work competes with training time | 08 q4 |
| T10 | Give achievement timelines, or only the ladder? | Ladder only. The timelines are coaching convention, not measured medians, and a missed timeline is a quit trigger | 08 q5 |
| T11 | Is a Couch-to-5k style ladder acceptable with no controlled evidence for its interval structure? | Yes, labelled as convention. 08's own general rule: a convention may be a fine default if it is labelled one | 08 q3 |
| T12 | Re-read the newest volume dose-response meta-regression before the numbers ship? | **Done 2026-09-01.** PMID 41343037 read. The band does not move. The 20 is reframed as a recovery ceiling, not an optimum, and frequency is demoted to a strength variable. See the ACSM re-anchor section | 08 q2 |
| T13 | How hard should the nutrition line be? | Hard, as a config flag defaulting to hard. General healthy-eating information yes. Protein targets, macros, calories, supplements no. A flag, not a hidden default | 08 q6, 12 q3 |
| T14 | Sport profiles as data, or run the needs-analysis script live? | Script as the mechanism, profiles as a cached lookup. That is 09's own lean and it is right. Ship profiles only for sports you or your friends actually do | 09 q1, 09 q5 |
| T15 | Does the agent collect session RPE, or only prescribe? | Collect. One 0-10 number 20 to 30 minutes after the session, skippable. 07 calls it the highest value-per-token question in the system, and without it 09 section 4's formulas are decoration | 09 q2 |
| T16 | How hard should the ACWR flag gate? | Soft flag only, given the Impellizzeri critique. Surface the number, never block on it | 09 q3 |
| T17 | Who is the referral, for a solo user with no team medical staff? | GP by default. Physiotherapist for anything musculoskeletal lasting over two weeks. Named up front at intake, stored in config, so the agent has something concrete to say | 09 q4 |
| T18 | Does the product accept under-18 users? | **Cannot default.** Fallback if silent: no. The LTAD material would have to be a hard constraint, not a reference file | 09 q6 |
| T19 | Refusal strength: hard refuse, or proceed with a logged disclaimer? | Hard refusal on red flags and out-of-scope. Logged pushback with override elsewhere. See tension (f) | 10 q3, 12 q5 |
| T20 | How many condition cards at launch? | Global red flags plus 5 cards, not 26. Which 5 depends on you and your first users. 10's own recommendation | 10 q4 |
| T21 | Does the agent hold clearance letters, or a typed summary? | Typed structured summary only: diagnosis, intensity ceiling, movements to avoid, monitoring, date, clinician. Holding documents changes the data-protection picture materially | 10 q5 |
| T22 | Does the agent store hormone-therapy details, or a coarse flag? | Coarse flag: direction plus start date. That is all the adjustments table needs, and storing less is safer for this population | 11 q7 |
| T23 | How much should the agent volunteer about sport eligibility policy? | Once at intake, only if the client says they compete, with a date and a link and no opinion. Never unprompted otherwise | 11 q2 |
| T24 | Policy-refresh mechanism for eligibility rules? | A dated "last checked" field the agent surfaces whenever it quotes a policy. Live fetching every time is expensive and a scheduled re-research task will rot | 11 q4 |
| T25 | Non-binary clients wanting an ambiguous or de-emphasized shape, where there is no literature at all: guess with a caveat, or decline? | Guess with an honest caveat. Declining tells someone their goal is illegitimate. The physiology is ordinary; only the target shape is unstudied | 11 q5 |
| T26 | How hard should the agent push the disordered-eating screen? | Do not screen repeatedly. React to what is said. Repeated screening feels like surveillance to someone already scrutinised, and administering SCOFF or LEAF-Q is out of scope anyway | 11 q6, 12 section 8.4 |
| T27 | Which ADHD adherence tactics do you actually want? | External structure, near-zero start friction, in-session rewards, an honest time budget, and a 10-minute minimum session that always counts. Skip novelty rotation, which trades against progression consistency | 12 q6 |
| T28 | Disclaimers visible or configured away? | Once at first contact, once in exported documents, never per message. See the disclosure rule | 12 q4 |

Two of these, T1 (jurisdiction) and T18 (under-18 users), have no safe default.
Both change what is legal rather than what is wise.

---

## Citation audit, 2026-09-01

Follow-up 5. The research briefs named some papers from memory, and one of them
turned out not to exist. This pass grepped every note for a citation its author
flagged as unopenable or substituted, then checked each against PubMed's
E-utilities or the publisher. **Existence and the fetch problem are separate
questions**, and the earlier notes conflated them: most of these papers are
real, and only their contents are unread.

| Claimed citation | Where flagged | Verdict |
|---|---|---|
| "Yun et al. 2023 meta-analysis" | 11 gaps, 11 open q1 | **Does not exist.** A PubMed author-plus-topic-plus-year search returns 0 records. The brief invented it. The substitution stands |
| Gois et al. 2025, the substitute | 11 gaps | **Real and correctly described.** Gois Í, Rodrigues FB, Pereira M, Dias-da-Silva MR, Gomes SM, *Rev Endocr Metab Disord* 2025;26(6):937-953, [PMID 40569560](https://pubmed.ncbi.nlm.nih.gov/40569560/), [doi:10.1007/s11154-025-09985-2](https://doi.org/10.1007/s11154-025-09985-2). Systematic review and meta-analysis of BMI and body composition on GAHT, as 11 says |
| ACSM 2026 position stand, "could not open" | 08 preamble, 08 section 2 | **Real, and now read.** Currier, D'Souza, Fiatarone Singh, … Phillips, *Med Sci Sports Exerc* 2026;58(4):851-872, [PMID 41843416](https://pubmed.ncbi.nlm.nih.gov/41843416/), [doi:10.1249/MSS.0000000000003897](https://doi.org/10.1249/MSS.0000000000003897). The abstract fetches fine through E-utilities. 08's "could not open" was a client problem, not a source problem |
| Pelland et al. 2026 volume meta-regression | 03, 08 q2 | **Real and now read.** *Sports Med* 2026;56(2):481-505, [PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/). See the ACSM re-anchor section |
| Spiering et al. 2021 minimal dose | 09 section 2, "paywalled HTTP 402" | **Real, still unread.** Spiering, Mujika, Sharp, Foulis, *J Strength Cond Res*, [PMID 33629972](https://pubmed.ncbi.nlm.nih.gov/33629972/). Existence confirmed; the LWW full text is still paywalled, so 09's numbers stay UNVERIFIED |
| DiStasio 2014, Brzycki/Epley validation | 02 §9, "403 on OpenSIUC" | **Real, still unread.** An SIU master's research paper, named in PMC9465738's reference list. OpenSIUC returned 403 again on 2026-09-01. The R² figures remain snippet-sourced |
| Brzycki 1993 original | 02 §9 | **Real, still unread.** *JOPERD* 64(1):88-90, [doi:10.1080/07303084.1993.10606684](https://doi.org/10.1080/07303084.1993.10606684), paywalled at Taylor & Francis. The formula's sign no longer depends on it (02 §9) |
| Weight-dependent 1RM preprint | 03, tagged UNVERIFIED | **Real.** arXiv 2603.17495, "A Weight-Dependent 1RM Prediction Equation Optimized on 303,494 Near-Failure Sets Across 388 Exercises", fetches at 200. Still a **preprint**, so the UNVERIFIED tag stays for the right reason: not peer reviewed, rather than not found |
| Endocrine Society 2017 guideline | 11 gaps | **Real.** Hembree et al., *J Clin Endocrinol Metab* 2017;102(11):3869-3903, [doi:10.1210/jc.2017-01658](https://doi.org/10.1210/jc.2017-01658). 11 already verified the guideline; only its expected-change tables were not retrieved |

**One invented citation out of nine checked.** The rest were fetch failures
mislabelled as sourcing failures, and three of them cleared on a retry through
a different endpoint. Two lessons for the next pass:

- **Try E-utilities before writing "could not open".** `efetch.fcgi?db=pubmed`
  serves abstracts to non-browser clients; `pubmed.ncbi.nlm.nih.gov` does not.
  The ACSM stand and Pelland both failed on the second and worked on the first.
- **Separate "I could not read it" from "it may not exist"** in the tag itself.
  UNVERIFIED currently means both, which is why a fabricated paper sat in the
  same bucket as a paywalled one for a whole round.

---

## What is still unverified

Carried forward unchanged. None of these are softened.

- **ACSM 2009's exact numbers** in 06 section 3.4 and 08 goal 2 are search
  excerpts. The PDF and the PubMed page both blocked fetch (06 "Gaps"). The
  **2026** numbers are the verified ones.
- **NSCA's rep/set/rest-by-goal table** was never confirmed against primary text
  (06 "Gaps"). **NSCA Essentials' training-status classification** likewise (07
  section 5).
- **The ACSM 2015 screening algorithm figure**, the "regular exercise"
  definition, the intensity bands, and the absolute contraindications list all
  route through secondary summaries. The ACSM PDF link is dead and the book is
  paywalled (07 section 11, 10 section 1).
- **ACSM and CSEP push-up and sit-and-reach norms**, Cooper test norm tables,
  1.5-mile run norms, broad jump, wall sit, adult pull-up norms, thoracic and
  hip rotation norms, heart rate recovery threshold, HRmax standard deviation,
  and the musculoskeletal red-flag list (07 section 11).
- ~~**Ottawa ankle/knee rules** were never searched, so "cannot bear weight" is
  unsourced in 06's red-flag table.~~ **Closed 2026-09-01.** Four Stiell papers
  read and captured; see "The Ottawa rules" above. Note 06's own table still
  carries the old wording and should be updated when 06 is next touched.
- **NASM Code of Professional Conduct** and the **NSCA nutrition-advice excerpt**
  are UNVERIFIED in both 06 and 10. NASM's PDF did not fetch; NSCA returned 403.
- **FDA general wellness guidance** primary text not fetched; both fda.gov URLs
  404'd (06 section 1).
- **Spiering 2021 minimal-dose numbers** paywalled at HTTP 402 (09 section 2).
  **Verkhoshansky's dynamic correspondence criteria** not fetched (09 section 11).
- **The 10% weekly progression rule** is widely taught and weakly evidenced. Buist
  2008 found no injury difference (08 conflicts, 09 section 11).
- **ACOG 804 Box 2**, ADA 2016 glucose thresholds beyond the quoted parts, SEES
  eating-disorder stability criteria, EULAR arthritis recommendations, and the
  2015 Heart Rhythm Society POTS consensus were all unretrieved (10 section 6).
- **Every ADHD-adherence tactic** in 12 section 4.9 is a derived mapping, tagged
  UNVERIFIED by its own author. The underlying findings are cited; the tactics
  are inference. No randomised trial of ADHD exercise adherence exists (06
  "Gaps").
- **Michie 2009's BCT effectiveness ranking**, absolute strength gain rates,
  endurance improvement rates, NSCA Code of Ethics primary text, CIMSPA's full
  code, Gardner on habit, and ACE's verbatim code principles were all unretrieved
  (12 section 12).
- **Regression ladders and the cue library** are craft consensus, not sourced (12
  section 12). **Movement-pattern taxonomy** has no confirmed live source (06
  "Gaps").
- **Recovery capacity, hypertrophy volume needs, protein intake, injury risk, and
  injection-cycle timing under HRT** have no trans-specific study in either
  direction (11 section 3.3). **Yun 2023's DOI** was never found; Gois 2025 was
  substituted (11 open q1).
- **Reassessment cadence** in 12 section 7.1 is UNVERIFIED craft. No
  certification text fixes an interval.
- **DERIVED, not evidence-based**: the 5% step-size guard, the "-5% per RPE point
  over target" rule, the time-off resumption percentages, and the statistical
  plateau definition (03, carried in 00-synthesis-system "What is still
  unverified").
