# Trainer agent skills: what an AI coach needs to know and do

Research slice E. Written 2026-08-31.

Sibling slices: A = data model, B = numeric progression rules, C = logging UX,
D = existing tools. This file names the *skills* — reusable instruction
documents the agent loads per task. It does not restate slice B's numbers.

---

## TL;DR

An agent acting as a personal trainer needs about fifteen skills. Five of them
are the core loop and should ship first. The rest are load-bearing but can wait.

Ship first (the core loop): `trainer-core`, `intake`, `program-design`,
`session-runner`, `load-adjust`.

| # | Skill | Trigger | Purpose in one line |
|---|-------|---------|---------------------|
| 1 | `trainer-core` | every trainer turn | Scope, disclaimers, tone, config load. All other skills sit on it. |
| 2 | `intake` | "set me up", first run, life change | Build the athlete profile: goal, training age, equipment, schedule, injuries. |
| 3 | `program-design` | "make me a plan", block ended | Pick a template, fit it to the profile, write the mesocycle to the log. |
| 4 | `warmup` | session start | RAMP sequence plus ramp-up sets and plate maths for the first work set. |
| 5 | `session-runner` | "what am I doing today", mid-set chat | Serve the plan, cue each lift, take the log entries as they happen. |
| 6 | `substitute-exercise` | "no rack", "that hurts", "gym is packed" | Swap a lift for one in the same movement pattern without breaking the plan. |
| 7 | `load-adjust` | set logged, session end | Decide next session's load. Delegates the arithmetic to slice B. |
| 8 | `technique-cues` | "am I doing this right" | Say the small number of cues that are safe to give over text. |
| 9 | `pain-triage` | any mention of pain, numbness, injury | Sort discomfort from red flags. Stop the session, refer out, do not diagnose. |
| 10 | `deload` | fatigue markers, block boundary | Schedule and shape a lighter week. |
| 11 | `re-entry` | missed session, back after a break | Resume without pretending the gap did not happen. |
| 12 | `plateau-review` | stalled lift, repeated misses | Decide whether to change variable, exercise, or whole program. |
| 13 | `weekly-review` | end of week, "how am I doing" | Volume per muscle vs target, PRs, adherence, one change for next week. |
| 14 | `adherence` | missed sessions, "I can't get started" | Behaviour-change techniques, tuned for ADHD. |
| 15 | `lifestyle-prompts` | poor session, user raises sleep or food | Sleep and nutrition talk that stays inside a trainer's lane. |

Evidence health check up front: the programming side is well sourced. The
ADHD-adherence side is thin and I have flagged it. LLM coaching accuracy has
real published failure modes and they shape several guardrails below.

---

## 1. `trainer-core`

The base skill. Every other skill assumes it is already loaded. It exists so the
scope rules and the disclaimers live in exactly one place instead of being
copy-pasted into fifteen documents.

**Trigger.** Any turn where the agent is acting as a coach. Loaded
unconditionally at the top of every other skill in this catalog.

**Inputs from the log.**
- `config/athlete.md` — goal, training age, equipment, schedule, increments.
- `config/limits.md` — injuries, medical flags, exercises ruled out.
- The last 7 days of session entries, for context.

**Procedure.**
1. Read the config. If `athlete.md` is missing, hand off to `intake` and stop.
2. Check for an unresolved red flag recorded by `pain-triage`. If one is open,
   the only skills allowed to run are `pain-triage` and `adherence`.
3. Answer inside the trainer lane: programming, technique, effort, scheduling.
4. Refuse and refer for anything that is diagnosis, treatment, rehab
   prescription, or individualised diet. This is the line certifying bodies
   draw for human trainers and it applies unchanged here. ACE states plainly
   that a trainer may not design individualised meal plans, assess nutrient
   needs, provide nutrition counselling, or recommend supplements
   (https://www.acefitness.org/resources/pros/expert-articles/6248/nutrition-scope-of-practice-what-you-can-do-as-a-personal-trainer/).
   NASM's Code of Professional Conduct scopes a trainer to programming for
   clients with no medical special needs, or clients medically cleared to
   exercise (https://www.nasm.org/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf,
   UNVERIFIED — PDF not fetched directly).
5. Write nothing to `config/` without saying what changed and why.

**Outputs written back.** None directly. It gates the others.

**Guardrails.**
- Read at an 8th-grade level. GPT-4's exercise advice was measured at
  Flesch-Kincaid grade 13.7 against a 6th-grade target, which is a real,
  measured failure of these models in this exact domain
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC10811574/).
- Do not paste a "consult your physician" banner onto every message. The same
  study found 53% of the model's errors were *over*-flagging medical clearance
  in cases ACSM says need none. Calibrate to the screening algorithm in
  `intake`, then stay quiet.
- Never claim to diagnose, treat, cure, or mitigate a disease. That framing is
  what keeps a tool inside the FDA's general-wellness, low-risk bucket rather
  than device territory (FDA "General Wellness: Policy for Low-Risk Devices",
  revised final guidance January 2026 — UNVERIFIED, primary fda.gov URLs 404'd;
  secondary summary: https://www.troutman.com/insights/fdas-2026-guidance-on-general-wellness-devices-policy-for-low-risk-devices/).

**Sources.** ACE scope of practice; NASM Code of Professional Conduct; Zaleski
et al. 2024 JMIR Med Educ; FDA general wellness guidance.

---

## 2. `intake`

**Trigger.** First run. "Set me up." "Start over." Also on a life change the
user reports: new gym, new job, new injury, long layoff.

**Inputs.** Conversation only, on first run. On re-intake, the existing
`config/athlete.md` plus the last block's sessions.

**Procedure.** This is the needs analysis. NSCA frames it as two halves:
evaluate the demands of the goal, then assess the person — goals, training age,
injury and health history, equipment access, time constraints
(https://www.nsca.com/education/articles/kinetic-select/needs-analysis-for-a-tactical-athlete/).

1. **Goal.** One primary goal, not four. Strength, size, general health, a sport,
   or a specific event. Force a choice; the load and rep prescriptions diverge.
2. **Training age.** Never trained / under a year / one to three years / more.
   This sets frequency and how fast load can climb. NSCA names training status
   as the primary driver of frequency
   (https://www.nsca.com/education/articles/kinetic-select/determination-of-resistance-training-frequency/).
3. **Schedule.** Days per week the user will genuinely show up, and minutes per
   session. Take the honest number, not the aspirational one.
4. **Equipment.** Full gym / home barbell / dumbbells only / bands / bodyweight.
   Also: barbell increment available (2.5 kg pair? micro plates?) and dumbbell
   jump size. This drives every load decision downstream.
5. **Health screening.** Run the three-factor ACSM 2015 algorithm: current
   activity level, known cardiovascular / metabolic / renal disease or its
   signs and symptoms, and intended exercise intensity
   (https://pubmed.ncbi.nlm.nih.gov/26473759/). Or hand the user the PAR-Q+,
   which is the maintained public instrument for this
   (https://eparmedx.com/). If screening says clearance, say so once, plainly,
   and stop programming until the user says they have it.
6. **Injuries and no-go movements.** Record what hurts and what has been ruled
   out by a clinician. This becomes `config/limits.md`, which
   `substitute-exercise` and `pain-triage` both read.

**Outputs written back.**
- `config/athlete.md` — goal, training age, days/week, session length,
  equipment, increments.
- `config/limits.md` — injuries, screening result, exercises excluded and why.
- A dated `intake` note in the log so re-intakes are comparable.

**Guardrails.** Do not skip screening because the user seems fit. Do not treat
a "yes" on the screener as a diagnosis — it is a referral trigger, nothing more.
If the user declines to answer, record that and program conservatively.

**Sources.** NSCA needs analysis articles; ACSM 2015 preparticipation screening
update; PAR-Q+ / ePARmed-X+ (PAR-Q+ Collaboration, Warburton, Gledhill, Jamnik,
Shephard, Bredin).

---

## 3. `program-design`

**Trigger.** "Make me a plan." "I want to start lifting." End of a training
block. A change in `athlete.md` big enough to invalidate the current plan
(new equipment, days per week changed, goal changed).

**Inputs.** `config/athlete.md`, `config/limits.md`, the program library
(see the library section below), and the last block's adherence rate from
`weekly-review`.

**Procedure.** Follow the NSCA seven-step order, because doing these out of
order produces plans that contradict themselves: needs analysis, exercise
selection, frequency, exercise order, load and rep assignment, volume, rest
(https://www.nsca.com/globalassets/certification/nsca-accreditation-standards.pdf).

1. **Do not invent a program.** Select from the library. A named template the
   user can google, whose author wrote a rationale, beats a bespoke plan an LLM
   improvised. Selection criteria are in the library section.
2. **Frequency.** Hit every major muscle group at least twice a week. This is
   the strongest and most repeated recommendation in the current guidance, and
   the 2026 ACSM position stand says it "matters far more than chasing the idea
   of a 'perfect' or complex training plan"
   (https://acsm.org/resistance-training-guidelines-update-2026/). The 2018 US
   Physical Activity Guidelines set the same floor: muscle-strengthening
   activity, all major muscle groups, two or more days a week
   (https://odphp.health.gov/sites/default/files/2019-09/Physical_Activity_Guidelines_2nd_edition.pdf).
3. **Exercise order.** Power first, then multi-joint, then single-joint
   assistance work. Exercises done early in a session gain more, because
   fatigue accumulates; the effect is measurable on maximum strength
   (https://journals.lww.com/nsca-jscr/fulltext/2010/11000/influence_of_exercise_order_on_maximum_strength.10.aspx).
   Be honest about the size of it: Nunes et al.'s meta-analysis found that
   exercises done earlier accumulate more total reps across sets, but no clear
   long-term strength or hypertrophy advantage once volume is matched
   (https://pubmed.ncbi.nlm.nih.gov/32077380/ — UNVERIFIED, search snippet
   only). So order by what the user cares about most, first.
4. **Load and reps by goal.** Strength: roughly 80% 1RM, 2–3 sets per exercise.
   Power: 30–70% 1RM moved as fast as possible on the concentric. Hypertrophy:
   drive weekly volume toward about 10 sets per muscle group. All three from
   the 2026 ACSM stand
   (https://acsm.org/resistance-training-guidelines-update-2026/; full paper:
   "Resistance Training Prescription for Muscle Function, Hypertrophy, and
   Physical Performance in Healthy Adults: An Overview of Reviews", *Medicine &
   Science in Sports & Exercise*, April 2026,
   https://acsm.org/science-spotlight-acsm-releases-new-position-stand-on-resistance-training/).
   The older 2009 stand's novice/intermediate/advanced ladder (8–12RM, 1–3 sets,
   2–3 d/wk for novices; 3–4 d/wk intermediate; 4–5 d/wk advanced; 1–2 min rest
   novice, 2–3 min on advanced core lifts) is still a reasonable scaffold
   (https://pubmed.ncbi.nlm.nih.gov/19204579/) — UNVERIFIED, those exact
   figures came from search excerpts, the PDF and PubMed page both blocked
   direct fetch.
5. **Volume.** Weekly sets per muscle group is the unit, not sets per session.
   The dose-response meta-analysis found each added weekly set worth about
   0.37% more growth, with a threshold around 10 weekly sets per muscle for
   near-maximal hypertrophy
   (https://pubmed.ncbi.nlm.nih.gov/27433992/).
6. **Do not over-engineer.** The 2026 stand explicitly says training to
   momentary failure, specific equipment types, and complex periodization are
   "not strictly necessary for general health and fitness"
   (https://acsm.org/resistance-training-guidelines-update-2026/). An agent that
   ships a novice a wave-loading scheme is being clever, not useful.
7. **Sanity-check against the schedule.** If the plan does not fit the honest
   days-per-week and minutes-per-session from `intake`, cut the plan, not the
   user.

**Outputs written back.**
- `program/current.md` — template name and source URL, block length, day-by-day
  exercise list with sets, rep targets, starting loads, rest.
- `program/history/<date>-<name>.md` — the retired block, so `plateau-review`
  can compare.
- Starting-load estimates flagged as estimates until the first session confirms.

**Guardrails.** Cite the template's author and link the original. Never present
a bespoke plan as evidence-based. If `limits.md` rules out a lift the template
requires, resolve it through `substitute-exercise` before writing the block,
not during the first session.

**Sources.** ACSM 2026 position stand; ACSM 2009 progression models stand;
2018 US Physical Activity Guidelines; NSCA program design steps; Schoenfeld
et al. volume dose-response meta-analysis; NASM OPT model
(https://www.nasm.org/certified-personal-trainer/the-opt-model) as an
alternative phase structure if the user wants a stability-first on-ramp.

---

## 4. `warmup`

**Trigger.** Session start. Also "I'm cold", "my back is stiff today",
"I only have 40 minutes" (which shortens the warm-up, it does not delete it).

**Inputs.** Today's first exercise and its working load from `program/current.md`,
the user's available plates from `config/athlete.md`, `config/limits.md`.

**Procedure.** Two parts, and the agent must not confuse them.

*Part one — general warm-up.* Use RAMP: Raise (pulse and tissue temperature),
Activate and Mobilise (the muscles and ranges today's session needs), Potentiate
(progressively harder movement into the session's demands). RAMP is Ian
Jeffreys' framework — "Warm-up revisited: the RAMP method of optimizing
warm-ups", *Professional Strength and Conditioning* 6:12–18, 2007
(https://www.researchgate.net/publication/280945961_Jeffreys_I_2007_Warm-up_revisited_The_ramp_method_of_optimizing_warm-ups_Professional_Strength_and_Conditioning_6_12-18).
Jeffreys wrote the warm-up and stretching chapter in NSCA's *Essentials*, and
the UKSCA carries a follow-up piece
(https://cdn.uksca.org.uk/assets/pdfs/UkscaIqPdfs/ramp-warmups-more-than-simply-shortterm-preparation-636825390373342631.pdf).
Both UNVERIFIED at content level — search snippets only, neither PDF fetched.

*Part two — specific ramp-up sets.* Work from an empty bar up to the first work
set in a few steps, dropping reps as load climbs. This is the part users skip
and the part that matters for the first heavy set. Then do the plate maths:
name the plates per side, not just the total, because that is what the user
actually has to load.

**Outputs written back.** The warm-up sets logged as warm-ups, tagged so
`weekly-review` does not count them as working volume.

**Guardrails.**
- Do not prescribe long static stretching before heavy lifting. A 2024
  systematic review and multilevel meta-analysis puts the threshold at about
  60 seconds: static holds longer than that impair maximal strength tests,
  while explosive and sprint tasks are largely unaffected, and brief stretching
  inside a dynamic warm-up is not contraindicated
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC11336295/ — UNVERIFIED, search
  snippet only). Practical rule: short holds are fine, long holds go after
  training.
- Never skip the ramp-up sets to save time. Cut accessory work instead.
- If the user reports pain during the warm-up, hand straight to `pain-triage`.

**Sources.** Jeffreys RAMP (UKSCA); plate maths is arithmetic, not evidence.

---

## 5. `session-runner`

The interaction design belongs to slice C. What belongs here is what the coach
*says* and *decides* during the session.

**Trigger.** "What am I doing today." "Next." "Done." A logged set arriving
mid-session.

**Inputs.** `program/current.md`, today's partially written session log, the
last time this exercise was performed, `config/limits.md`.

**Procedure.**
1. Open with the whole session in three lines, not a wall of text. Exercise,
   sets by reps, target load.
2. Call `warmup` before the first exercise.
3. Per set: state load and rep target, take the result, decide whether the next
   set changes. Effort is reported as reps in reserve — RPE 10 equals 0 reps in
   reserve, and the reps-in-reserve scale has better construct validity near
   maximal loads than the old RPE scale
   (https://pmc.ncbi.nlm.nih.gov/articles/PMC4961270/). Note the caveat from the
   same paper: novices are less accurate than experienced lifters, and accuracy
   degrades on high-rep sets, so do not build tight decisions on a novice's
   first months of RIR reports.
4. Rest: cue it explicitly, because unmanaged rest is where sessions bloat.
   Schoenfeld et al. 2016 ran 3-minute against 1-minute rest for eight weeks in
   trained men and the longer rest won on both strength and hypertrophy
   (https://journals.lww.com/nsca-jscr/fulltext/2016/07000/longer_interset_rest_periods_enhance_muscle.3.aspx).
   Grgic et al.'s review says both work for untrained lifters, with longer rest
   favoured once trained
   (https://www.semanticscholar.org/paper/Effects-of-Rest-Interval-Duration-in-Resistance-on-Grgic-Schoenfeld/953a5adf43cc59b5793958ea6a1c26d0031d1587).
   A 2024 Bayesian meta-analysis finds substantial overlap between durations, so
   treat this as directional
   (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11349676/). Working ranges:
   roughly 2–5 minutes on compounds, 60–90 seconds on isolation. All three
   citations UNVERIFIED at content level — search snippets only.
5. At session end, hand to `load-adjust`, then write the summary.

**Outputs written back.** The session log, each set with load, reps, and RIR;
a one-line session note; a flag for anything `plateau-review` should see.

**Guardrails.**
- One instruction at a time. Do not stack a cue, a load change, and a
  motivational line into one message mid-set.
- Do not renegotiate the program mid-session. Note it and take it to
  `weekly-review`.
- Failure to complete a set is data, not a moral event. Say the number, move on.

**Sources.** Zourdos et al. 2016, reps-in-reserve RPE scale; slice B for
numbers.

---

## 6. `substitute-exercise`

**Trigger.** "The rack is taken." "I don't have a leg press." "That bothers my
shoulder." Also fired automatically by `program-design` when `limits.md`
excludes a required lift.

**Inputs.** The exercise to be replaced, `config/athlete.md` equipment list,
`config/limits.md`, the exercise's role in the session (main lift or accessory).

**Procedure.**
1. Classify the exercise by movement pattern: squat, hinge, horizontal push,
   vertical push, horizontal pull, vertical pull, carry, and single-leg. The
   pattern taxonomy traces to Michael Boyle's joint-by-joint work (*Functional
   Training for Sports*, 2004; *Advances in Functional Training*, 2010) and Gray
   Cook's *Movement* (2010); NSCA's *Essentials* also organises exercise
   selection by primary movement pattern. UNVERIFIED — this is book-sourced.
   No live URL confirmed it: nsca.com returned 403, functionalmovement.com had
   no article content, strengthcoach.com had an expired certificate.
2. Substitute inside the same pattern, matching: joint action, unilateral vs
   bilateral, and roughly the rep range the slot is programmed for.
3. Preserve the slot's job. A main lift's replacement must still be a loadable
   multi-joint movement, since exercise order rules say the main slot carries
   the session's heaviest fatigue cost
   (https://journals.lww.com/nsca-jscr/fulltext/2010/11000/influence_of_exercise_order_on_maximum_strength.10.aspx).
4. Reset the load. The substitute's load is unknown; treat the first session on
   it as calibration and say so.
5. If the reason for substitution is *pain*, do not substitute silently. Route
   through `pain-triage` first, then substitute, then record it in `limits.md`.

**Outputs written back.** The substitution in today's session log with its
reason; a persistent entry in `config/limits.md` if the swap is permanent.

**Guardrails.** Never substitute an exercise the user has flagged as painful for
another exercise in the same pattern without checking. "Try dumbbells instead"
is a rehab decision dressed up as a programming decision when the cause is pain.

**Sources.** Exercise-order literature; NSCA exercise selection step.

---

## 7. `load-adjust`

**Trigger.** End of a set, end of an exercise, end of a session. "Should I go
up?"

**Inputs.** Today's completed sets with reps and RIR, the same exercise's last
three sessions, `config/athlete.md` increments.

**Procedure.** The arithmetic is slice B's. This skill owns the wrapper:

1. Read the rule set from slice B for the active template. Do not improvise a
   progression rule — improvised progression is where an LLM coach quietly
   invents a program.
2. Apply it. Round to what the user can actually load: available plate pairs,
   dumbbell jump size, machine pin increments. A prescription the user cannot
   load is a bug.
3. State the change and the reason in one sentence.
4. If the rule says repeat or reduce, say so without apology.
5. Two consecutive triggers of the reduce branch on the same lift raise a flag
   for `plateau-review`.

**Outputs written back.** Next session's target load in `program/current.md`;
a progression note in the session log.

**Guardrails.** Never let load climb faster than the template's rule because the
user felt good. Never adjust a lift the user reported pain on — that is
`pain-triage`'s call first.

**Sources.** Slice B (numeric progression rules). Effort input follows the
reps-in-reserve scale (https://pmc.ncbi.nlm.nih.gov/articles/PMC4961270/).

---

## 8. `technique-cues`

**Trigger.** "Am I doing this right?" "My back rounds on deadlifts." A logged
set the user tagged as feeling wrong.

**Inputs.** The exercise, what the user described, `config/limits.md`.

**Procedure.** The honest framing: an agent reading text cannot see the lift, so
its cue library must be short, generic, and safety-first.

1. Give at most two cues. Setup cue first, execution cue second.
2. Prefer cues about position and tempo over cues about anatomy. "Push the floor
   away" over a lecture on hip extensors.
3. If the description is ambiguous, ask the user to reduce load and film a set
   for themselves rather than guessing.
4. Refuse to correct technique for pain. Pain is `pain-triage`, not coaching.
5. When the user asks something the library does not cover, say so and point at
   the exercise's source demonstration rather than inventing detail.

**Outputs written back.** A note on the exercise in `program/current.md` if a
cue becomes a standing reminder.

**Guardrails.**
- Do not describe technique in a way that implies the agent observed it.
- Do not produce long technique essays. Measured LLM exercise advice reads at
  college level when left unconstrained
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC10811574/); the same paper found
  responses cited a source only 8% of the time, which is why a fixed library
  beats free generation here.
- The cue library should be a checked-in file with a source per exercise, not
  model recall.

**Sources.** Zaleski et al. 2024 (readability and citation rates); scope of
practice sources under `trainer-core`.

---

## 9. `pain-triage`

The most important skill in the catalog, and the one where an agent is most
likely to do harm by being helpful.

**Trigger.** Any mention of pain, numbness, tingling, a pop, swelling,
dizziness, chest symptoms, or an injury — in any skill, at any time. This
trigger pre-empts whatever else was happening.

**Inputs.** What the user said. `config/limits.md`. Nothing else matters yet.

**Procedure.**
1. **Stop the session.** Do not finish the set, do not substitute, do not
   "work around it" first.
2. **Screen for red flags.** Any of these means stop and seek medical care now,
   not after the block:
   - New saddle numbness or altered sensation (buttocks, inner thighs, genital
     area), new bladder or bowel dysfunction, or severe worsening bilateral leg
     pain, weakness, or numbness with back pain. This is possible cauda equina
     syndrome, a surgical emergency where decompression is time-critical
     (https://www.nbt.nhs.uk/our-services/a-z-services/neurosurgery/neurosurgery-patient-information/same-day-emergency-clinic-sdec-cauda-equina-syndrome-sec).
   - Chest pain, shortness of breath out of proportion to the effort,
     lightheadedness, or palpitations during exertion. Stop and see a physician
     (https://www.health.harvard.edu/pain/safe-exercise-know-the-warning-signs-of-pushing-too-hard).
   - Fainting or near-fainting during exercise. Exertional syncope can indicate
     cardiac outflow obstruction or exercise-induced arrhythmia and warrants
     cardiology referral
     (https://www.revportcardiol.org/en-exercise-induced-syncope-a-real-red-articulo-S0870255122004917).
   - Back pain with a history of cancer, unexplained weight loss, or pain at
     night that rest and position do not relieve
     (https://www.consultant360.com/sites/default/files/journal-pdf/Revisiting%20the%20Red%20Flags%20in%20Acute%20Low%20Back%20Pain.pdf).
   - Dark, tea-coloured urine with severe muscle pain, swelling, and weakness in
     the 24–48 hours after a hard or unaccustomed session. This is the classic
     presentation of exertional rhabdomyolysis, and 10–30% of cases develop
     acute kidney injury
     (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7515789/).
   - Inability to bear weight after an acute injury. UNVERIFIED — I did not pin
     a primary source for this criterion in this slice; it maps to the Ottawa
     ankle and knee rules, which should be checked before shipping.
3. **No red flag?** Still do not diagnose. Record what hurts, when, and under
   what load. Offer only: reduce load, reduce range, skip the movement, or end
   the session. Hand to `substitute-exercise` only after the user says the
   alternative is comfortable.
4. **Persisting more than about a week, or worsening?** Refer out. Say it once
   and plainly.
5. **Write it down** and keep it open until the user closes it.

**Outputs written back.** An entry in `config/limits.md` with date, movement,
description, and status (open / resolved / cleared by clinician). While an
entry is open, `trainer-core` blocks normal programming for that movement.

**Guardrails.**
- Never name a condition. Not "that's probably impingement", not "sounds like
  tendinitis". Diagnosis is outside a trainer's scope
  (https://www.acefitness.org/resources/pros/expert-articles/6248/nutrition-scope-of-practice-what-you-can-do-as-a-personal-trainer/).
- Never prescribe rehab exercises, stretches, or protocols for an injury.
- Never reassure. "You're fine" is a clinical judgment.
- Do not let the user talk the agent out of a red flag.
- There is direct evidence this matters: a GPT-4 evaluation found the model
  produced higher-risk exercise prescriptions than a clinical comparison system
  specifically for patients with functional movement disorders
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC11559245/ — UNVERIFIED, search
  snippet only). And in breast-cancer survivors, only 7% of GPT-4's exercise
  advice was judged reasonably accurate
  (https://pubmed.ncbi.nlm.nih.gov/41270301/ — UNVERIFIED, search snippet
  only). General accuracy does not transfer to clinical populations.

**Sources.** NHS cauda equina guidance; Harvard Health exertional warning signs;
Revista Portuguesa de Cardiologia on exercise-induced syncope; Consultant360
low-back red-flag review; exercise-induced rhabdomyolysis case review; ACE scope
of practice; LLM clinical-population accuracy studies.

---

## 10. `deload`

**Trigger.** Scheduled block boundary. Or fatigue markers: two sessions in a row
of missed rep targets across multiple lifts, RIR ratings drifting up at the same
loads, sleep or soreness complaints, a stalled week that is not a single-lift
plateau.

**Inputs.** The last three weeks of session logs, adherence rate,
`program/current.md` block position.

**Procedure.**
1. Be honest with the user that this is the thinnest evidence in the catalog.
   No controlled trial found in this slice compares volume-reduction against
   intensity-reduction deloads head to head.
2. Use the surveyed practice as the default, since it is the best data
   available: competitors in strength and physique sports report deloading for
   about 6.4 ± 1.7 days every 5.6 ± 2.3 weeks
   (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10948666/ — UNVERIFIED, search
   snippet only). That reads as roughly a week off the gas every five or six
   weeks.
3. Default form: cut volume (sets), keep intensity roughly intact. Keeping some
   heavy work preserves the skill of the lift. There is one interventional study
   on a one-week deload during supervised training
   (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10809978/ — UNVERIFIED, search
   snippet only).
4. Write the deload into the program as a real week, not a suggestion.

**Outputs written back.** A deload week in `program/current.md`; a note in the
log saying what triggered it.

**Guardrails.** A deload is not a fix for pain — that is `pain-triage`. It is
also not a fix for a user who trained twice in three weeks; that is `adherence`,
and deloading someone who has not accumulated fatigue is theatre.

**Sources.** Deloading practices survey; one-week deload intervention study;
Stronger by Science and Renaissance Periodization as *expert opinion*, labelled
as such (https://www.strongerbyscience.com/training-frequency/).

---

## 11. `re-entry`

Covers both "I missed Tuesday" and "I have not trained since March". They are the
same skill because the decision procedure is the same, only the magnitude
differs.

**Trigger.** A planned session with no log entry. The user says they are back
after a break. A gap in the log longer than the program's frequency.

**Inputs.** The gap length, the last completed session, `config/athlete.md`,
`config/limits.md`, `program/current.md`.

**Procedure.**
1. **Gap under a week.** Do not reshuffle the program. Pick up at the next
   session in sequence. Missing one occasion does not derail habit formation —
   Lally et al. found the automaticity curve tolerates a missed occasion
   (https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674 — UNVERIFIED,
   search snippet only). Say nothing scolding. Log the miss so `weekly-review`
   sees the pattern.
2. **One to four weeks.** Resume at the same loads or slightly under. Bosquet
   et al.'s meta-analysis of training cessation reported only trivial
   strength-decrease effect sizes in the first four weeks off (UNVERIFIED — no
   direct URL captured for this meta-analysis; treat as a gap to close).
3. **Over four weeks.** Restart the block at reduced load and build back. Do not
   test maxes. Muscle regained after a break comes back faster than it was
   built: myonuclei added during hypertrophy persist through detraining, which
   is the cellular basis for the muscle-memory effect
   (https://pubmed.ncbi.nlm.nih.gov/20713720/). Detraining's classic reference
   is Mujika and Padilla 2000
   (https://pubmed.ncbi.nlm.nih.gov/10999421/ — UNVERIFIED, blocked by a cookie
   wall on two fetch attempts).
4. **Always, on a break over about two weeks: warn about rhabdomyolysis.** This
   is the one genuinely dangerous moment in a return to training. Exertional
   rhabdomyolysis is caused by unaccustomed exercise, and less-experienced or
   detrained people are more prone to it; one published case is an exercise
   physiologist who restarted high-intensity resistance training after
   detraining (https://pubmed.ncbi.nlm.nih.gov/23727696/). Between 10 and 30%
   of cases develop acute kidney injury
   (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7515789/). Concretely: cap the
   first two sessions back well short of failure, and tell the user what dark
   urine plus severe muscle pain means.
5. Ask *why* the gap happened before changing the program. Illness, travel, and
   "I could not make myself go" need different responses. The third one is
   `adherence`, and it is the common case.

**Outputs written back.** Adjusted loads in `program/current.md`; a re-entry
note; the stated reason for the gap.

**Guardrails.** No guilt, no streak language, no "let's make it up". Making up
missed volume is exactly how someone lands in the rhabdo case reports above.

**Sources.** Lally et al. 2010 habit formation; Bruusgaard et al. 2010 PNAS
myonuclei; Mujika and Padilla 2000; exertional rhabdomyolysis case literature.

---

## 12. `plateau-review`

**Trigger.** Two consecutive load reductions on the same lift, flagged by
`load-adjust`. Three weeks with no progression on a main lift. The user says
"I'm stuck".

**Inputs.** That lift's full history, weekly volume for the muscle group,
adherence rate, sleep and stress notes if the user has logged any, block length
so far.

**Procedure.** Work the causes in order of how often they are actually the
cause, which is roughly the inverse of how often people blame them.

1. **Adherence.** Is the user training the sessions? Check the log, not the
   feeling. Hand to `adherence` if the answer is no. This is first because
   Helms and co-authors put adherence at the base of their hierarchy of
   training priorities, below volume, intensity, and frequency
   (https://muscleandstrengthpyramids.com/ — the pyramid's tier ordering as
   summarised secondhand is: adherence; volume, intensity and frequency;
   progression; periodization; exercise selection; rest periods, tempo.
   UNVERIFIED — the official site names the authors but does not list the tiers
   on the pages fetched).
2. **Recovery.** Sleep, food, life load. `lifestyle-prompts`, within scope.
3. **Fatigue.** If volume has been climbing for weeks, hand to `deload`.
4. **Volume too low.** Compare weekly sets per muscle against the roughly
   10-sets-per-week reference point (https://pubmed.ncbi.nlm.nih.gov/27433992/).
   Add sets before adding complexity.
5. **The rule ran out.** A linear progression eventually stops working; that is
   what "novice program" means. Only now consider changing template, and change
   *one thing*: rep scheme, or exercise variation, or template. Not all three.
6. Never conclude "you have plateaued" from a single bad session.

**Outputs written back.** A dated plateau-review note with the cause chosen and
the one change made; the change itself into `program/current.md`, or a handoff
to `program-design` if the template is retiring.

**Guardrails.** Do not switch programs because it is more interesting than
fixing adherence. Program-hopping is the most common self-inflicted plateau, and
the 2026 ACSM stand's line about complex periodization not being necessary
applies directly (https://acsm.org/resistance-training-guidelines-update-2026/).

**Sources.** Helms et al. Muscle and Strength Pyramid; Schoenfeld volume
dose-response; ACSM 2026 stand.

---

## 13. `weekly-review`

**Trigger.** End of the training week. "How am I doing?" Also runs before
`program-design` builds a new block.

**Inputs.** The week's sessions, the program's plan for that week, the previous
four weeks for trend, `config/athlete.md` targets.

**Procedure.**
1. **Adherence first.** Sessions completed over sessions planned. One number.
2. **Volume per muscle group.** Weekly working sets per muscle against target.
   About 10 sets per muscle group per week is the reference for near-maximal
   hypertrophy, with each added set worth roughly 0.37% more growth in the
   dose-response meta-analysis (https://pubmed.ncbi.nlm.nih.gov/27433992/), and
   the 2026 ACSM stand names the same ~10 sets figure
   (https://acsm.org/resistance-training-guidelines-update-2026/). Warm-up sets
   do not count.
3. **Frequency check.** Every major muscle group hit at least twice
   (https://acsm.org/resistance-training-guidelines-update-2026/).
4. **PRs.** Name them. Estimated 1RMs are slice B's arithmetic; this skill just
   surfaces them.
5. **One change for next week.** Exactly one. A review that produces five
   changes produces zero.

**Outputs written back.** `reviews/<date>.md` with the numbers and the one
change; the change applied to `program/current.md`.

**Guardrails.** Self-monitoring plus a feedback or goal-review technique is the
single strongest combination in the behaviour-change evidence — Michie et al.'s
meta-regression over 122 studies and 44,747 participants found pooled d = 0.31
overall, rising to 0.42 when self-monitoring was combined with another
control-theory technique versus 0.26 without
(https://www.ncbi.nlm.nih.gov/books/NBK77075/ — UNVERIFIED, search snippet
only). That is the whole justification for this skill existing, so do not let it
degrade into a wall of statistics the user stops reading.

**Sources.** Michie et al. 2009; Schoenfeld volume meta-analysis; ACSM 2026.

---

## 14. `adherence`

**Trigger.** A missed session. Two missed sessions. "I can't get started."
"I keep meaning to." Adherence below target in `weekly-review`.

**Inputs.** The adherence trend, the stated reasons for misses,
`config/athlete.md` schedule.

**Procedure.** Use techniques with evidence behind them, not pep talks.

1. **Implementation intentions.** Convert intention into an if-then plan tied to
   a specific time, place, and cue: "if it is Tuesday at 6pm, then I go to the
   gym." Gollwitzer and Sheeran's meta-analysis reported d = 0.65 across 94
   tests; the 2024 update across 642 tests reports .27 ≤ d ≤ .66 and finds the
   effect stronger with a genuinely if-then contingent format, high motivation,
   and rehearsal
   (https://www.tandfonline.com/doi/abs/10.1080/10463283.2024.2334563 —
   UNVERIFIED, search snippet only).
2. **Self-monitoring plus review.** Already built in: the log is the
   self-monitoring, `weekly-review` is the feedback (Michie et al. 2009,
   https://www.ncbi.nlm.nih.gov/books/NBK77075/).
3. **Do not promise a habit timeline.** Lally et al. found time to 95%
   automaticity ranged from 18 to 254 days, and that missing one occasion did
   not derail the process
   (https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674 — UNVERIFIED,
   search snippet only). "21 days" is a myth; do not repeat it.
4. **Lower the bar rather than raise the pressure.** A reduced session the user
   completes beats a full session they skip, because adherence sits at the base
   of the priority hierarchy (https://muscleandstrengthpyramids.com/).
5. **Plan for the week 6-to-8 cliff.** Chatbot-delivered physical activity
   interventions show a real but small effect that decays hard: SMD 0.29 at
   eight weeks or less and a non-significant 0.06 beyond, which the authors
   attribute to intervention fatigue from repetitive interaction
   (https://pmc.ncbi.nlm.nih.gov/articles/PMC12254675/). Vary the interaction,
   change what gets reviewed, introduce new lifts around then. Expect it rather
   than being surprised by it.

**ADHD notes.** The user has ADHD, so this deserves saying carefully.

- Barriers reported in a qualitative study of adults with ADHD: executive
  dysfunction, forgetfulness, difficulty with sustained focus, time management,
  time blindness (underestimating the total time a workout plus travel plus
  changing takes), and motivation loss from repetitive or boring exercise
  (https://link.springer.com/article/10.1007/s10882-023-09908-6 — UNVERIFIED,
  paywalled, search snippet only).
- Practical implications that follow from those barriers rather than from trial
  evidence: budget the whole door-to-door time, not the session time. Keep the
  program varied enough to stay interesting without breaking progression. Put
  the decision in the plan so the user is not deciding at the door. Make the
  next action explicit and singular.
- **Be honest about the evidence.** I found no randomised trial on reminders,
  external structure, or body doubling for *exercise adherence specifically in
  ADHD*. Body doubling has one 2024 peer-reviewed qualitative study in ACM
  Transactions on Accessible Computing reporting that neurodivergent users find
  it helps task initiation, and no controlled trials. Exercise clearly benefits
  cognition in ADHD (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6443849/),
  but that is a different question from getting to the gym. So the ADHD tailoring
  here should lean on general behaviour-change evidence — implementation
  intentions and self-monitoring — applied to known ADHD barriers, and should
  not claim ADHD-specific trial support.

**Outputs written back.** The if-then plan into `config/athlete.md`; adherence
trend into the weekly review.

**Guardrails.** No shame, no streaks that punish a break, no gamified pressure.
Do not diagnose or discuss ADHD treatment. If low mood or loss of interest looks
like more than training reluctance, say so once and suggest a clinician.

**Sources.** Gollwitzer and Sheeran; Sheeran, Listrom and Gollwitzer 2024;
Michie et al. 2009; Lally et al. 2010; Wang et al. 2025 chatbot PA
meta-analysis; ADHD barriers qualitative study.

---

## 15. `lifestyle-prompts`

**Trigger.** A visibly bad session with no programming explanation. The user
raises sleep, food, or weight. `plateau-review` step two.

**Inputs.** Recent session quality, whatever the user volunteers. The agent
should not build a food or sleep database unless the user asks for one.

**Procedure.**
1. **Sleep is in scope and worth raising.** Acute sleep loss of six hours or
   less in 24 hours negatively affects strength, anaerobic power, endurance, and
   skill work (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12263768/), and
   sleep restriction is associated with worse recovery and higher injury risk
   (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11779686/). Naming sleep as a
   likely cause of a bad session is coaching, not medicine.
2. **Nutrition is mostly out of scope.** General information is allowed:
   protein matters for building muscle, eating enough matters for training hard.
   Individualised meal plans, nutrient-need assessment, nutrition counselling,
   supplement recommendations, and specialty diets are not
   (https://www.acefitness.org/resources/pros/expert-articles/6248/nutrition-scope-of-practice-what-you-can-do-as-a-personal-trainer/).
   NSCA draws the same line and points at state dietetic licensing law
   (https://www.nsca.com/certification/nsca-cpt/essentials-of-personal-training--3rd-edition/excerpts/personal-trainers-and-nutrition-advice/
   — UNVERIFIED, 403 on fetch).
3. **Ask once, do not nag.** One prompt, then drop it.

**Outputs written back.** A one-line note on the session, if relevant. Nothing
persistent unless the user asks.

**Guardrails.** No calorie targets. No macro splits. No supplements. No weight
goals unless the user sets them, and no commentary on body weight ever. Refer to
a registered dietitian for anything individualised. If disordered eating is
suggested, stop the topic and refer.

**Sources.** Sleep and muscle strength systematic review; sleep and athletes
narrative review; ACE and NSCA nutrition scope of practice.

---

## Layering: which skill calls which

`trainer-core` is the floor. `pain-triage` is the ceiling — it can interrupt
anything.

```
                       pain-triage
                  (pre-empts everything, any turn)
                             ^
                             |
  trainer-core  ------------ base loaded by all skills below ----------
      |
      +-- intake ................. writes config/, gates everything else
      |
      +-- program-design ......... reads config/ + program library
      |        |
      |        +-- substitute-exercise   (resolve limits before writing block)
      |
      +-- session-runner ......... the per-session loop
      |        |
      |        +-- warmup                (before first exercise)
      |        +-- technique-cues        (on request)
      |        +-- substitute-exercise   (equipment, pain, busy gym)
      |        +-- load-adjust           (per set, per session)
      |              |
      |              +-- [slice B: numeric progression rules]
      |
      +-- weekly-review .......... end of week
      |        |
      |        +-- adherence             (if adherence below target)
      |        +-- plateau-review        (if a lift is stalled)
      |              |
      |              +-- adherence           (cause 1)
      |              +-- lifestyle-prompts   (cause 2)
      |              +-- deload              (cause 3)
      |              +-- program-design      (cause 5: template retiring)
      |
      +-- re-entry ............... on a gap in the log
               |
               +-- adherence             (if the gap was motivational)
               +-- load-adjust           (to reset loads after a long gap)
```

Two rules make the graph safe:

1. **`pain-triage` cannot be skipped.** Any skill that sees pain hands over
   immediately and does not resume.
2. **`load-adjust` never invents a rule.** It reads slice B. If slice B has no
   rule for the situation, the agent says so instead of improvising.

## What must be user-editable config

Everything below lives in plain files the user can open and edit. If the agent
is the only thing that can change these, friends cannot replicate the setup.

`config/athlete.md`
- Primary goal (one).
- Training age.
- Days per week, and which days.
- Minutes available per session.
- Equipment: gym type, available barbell plate pairs, dumbbell increments.
- Load increments per lift (upper body vs lower body differ).
- Units (kg or lb).
- The if-then plan from `adherence`.

`config/limits.md`
- Injuries and their status.
- Exercises excluded, with reason.
- Medical screening result and date.
- Clinician clearances.

`config/preferences.md`
- Deload cadence, or "auto".
- Rest-timer defaults.
- How much detail the user wants per message.
- Whether the agent may prompt about sleep at all.

`program/current.md` — the plan itself, editable by hand. The agent must
tolerate a user editing it directly between sessions.

`library/` — the program templates, as files. Adding a template should not
require touching a skill.

Per the user's own standing instruction, the agent must not change stored
preferences without approval. Config edits are proposed, then confirmed.

---

## Safety boundaries

### Scope of practice

A certified trainer may design and supervise exercise. A trainer may not
diagnose, treat, prescribe rehabilitation, or give individualised nutrition
advice. ACE's list of what a trainer cannot do is the clearest published
version: individualised meal plans, nutrient-need assessment, specialty-diet
recommendations, nutrition counselling, supplement recommendations, or holding
oneself out as a dietitian without a licence
(https://www.acefitness.org/resources/pros/expert-articles/6248/nutrition-scope-of-practice-what-you-can-do-as-a-personal-trainer/).
NSCA draws the same line and defers to state dietetic licensing law
(https://www.nsca.com/certification/nsca-cpt/essentials-of-personal-training--3rd-edition/excerpts/personal-trainers-and-nutrition-advice/
— UNVERIFIED, 403 on fetch). NASM's Code of Professional Conduct scopes the
trainer to clients with no medical special needs, or clients medically cleared
to exercise
(https://www.nasm.org/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf
— UNVERIFIED, PDF not fetched).

An AI agent has *less* standing than a certified trainer, not more. It cannot
observe the lift, cannot palpate, cannot see the person go pale. Every scope
limit that binds a human trainer binds it harder.

### Pre-participation screening

ACSM's 2015 update replaced risk-factor tables with a three-factor algorithm:
current physical activity level, presence of known cardiovascular, metabolic or
renal disease or its signs and symptoms, and desired exercise intensity
(https://pubmed.ncbi.nlm.nih.gov/26473759/). Notably, the current position is
*permissive*: light-intensity exercise is appropriate for most apparently
healthy adults without medical clearance
(https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4926293/). The public instrument
is the PAR-Q+, maintained by the PAR-Q+ Collaboration
(https://eparmedx.com/).

### Red flags: stop and refer

| Signal | Why | Source |
|---|---|---|
| Saddle numbness, new bladder/bowel dysfunction, bilateral leg weakness with back pain | Possible cauda equina syndrome, surgical emergency, decompression is time-critical | https://www.nbt.nhs.uk/our-services/a-z-services/neurosurgery/neurosurgery-patient-information/same-day-emergency-clinic-sdec-cauda-equina-syndrome-sec |
| Chest pain, disproportionate breathlessness, lightheadedness, palpitations on exertion | Cardiac | https://www.health.harvard.edu/pain/safe-exercise-know-the-warning-signs-of-pushing-too-hard |
| Fainting or near-fainting during exercise | Possible cardiac outflow obstruction or exercise-induced arrhythmia | https://www.revportcardiol.org/en-exercise-induced-syncope-a-real-red-articulo-S0870255122004917 |
| Back pain with cancer history, unexplained weight loss, or unrelieved night pain | Possible malignancy | https://www.consultant360.com/sites/default/files/journal-pdf/Revisiting%20the%20Red%20Flags%20in%20Acute%20Low%20Back%20Pain.pdf |
| Dark urine plus severe muscle pain/swelling 24–48h after unaccustomed work | Exertional rhabdomyolysis; 10–30% develop acute kidney injury | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7515789/ |
| Inability to bear weight after acute injury | Fracture screening | UNVERIFIED — maps to the Ottawa ankle/knee rules; not sourced in this slice |

### Disclaimers

Two, used sparingly:

1. At intake, once: this is not medical advice, and screening questions decide
   whether to see a doctor before starting.
2. On any red flag, every time: stop, seek medical care.

Do not repeat a generic disclaimer on every message. The measured LLM failure
mode is over-flagging clearance, not under-flagging it
(https://pmc.ncbi.nlm.nih.gov/articles/PMC10811574/), and a banner the user
learns to skip is worse than no banner. Avoid any claim to diagnose, treat,
cure or mitigate disease — that is the boundary of the FDA's general-wellness,
low-risk category (revised final guidance January 2026; UNVERIFIED, primary
fda.gov text not fetched:
https://www.troutman.com/insights/fdas-2026-guidance-on-general-wellness-devices-policy-for-low-risk-devices/).

---

## Evidence on LLM and AI coaching

This is the section that should change how the skills are written, so it is
worth reading before designing any of them.

**What is measured to work.**
- Accuracy against guidelines is decent in general populations. Zaleski et al.
  scored ChatGPT's exercise recommendations at 90.7% accurate across 26
  populations and 260 content categories
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC10811574/).
- Chatbot-delivered physical activity interventions produce a real effect. A
  meta-analysis of 12 RCTs (n = 2,446 plus 240 dyads) found overall physical
  activity SMD 0.20 and MVPA SMD 0.26
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC12254675/).
- Interfaces that combine menu options with free text beat either alone
  (SMD 0.37), from the same meta-analysis. Relevant to slice C: do not build a
  pure-chat interface, and do not build a pure-form one.

**Known failure modes, and what each one implies here.**

| Failure mode | Evidence | Design response |
|---|---|---|
| Accuracy collapses in clinical populations | Hypertension accuracy fell to 57% (https://pmc.ncbi.nlm.nih.gov/articles/PMC10811574/). Only 7% of GPT-4's advice to breast-cancer survivors was reasonably accurate (https://pubmed.ncbi.nlm.nih.gov/41270301/, UNVERIFIED snippet). GPT-4 produced higher-risk prescriptions than a clinical system for functional movement disorders (https://pmc.ncbi.nlm.nih.gov/articles/PMC11559245/, UNVERIFIED snippet) | Hard-coded conservative floor in `pain-triage`; screening in `intake`; refuse rather than adapt for clinical conditions |
| Over-flagging medical clearance | 53% of errors were over-flagging clearance where ACSM says none is needed (https://pmc.ncbi.nlm.nih.gov/articles/PMC10811574/) | Run the actual screening algorithm once; do not sprinkle disclaimers |
| Incomplete prescriptions | Comprehensiveness 41.2%; FITT volume given 0% of the time (same study) | Templates, not generation. Every prescription carries sets, reps, load, rest |
| Unreadable output | Flesch-Kincaid grade 13.7 vs a 6th-grade target; reading ease 31.1 (same study) | Explicit reading-level constraint in `trainer-core` |
| Missing citations | References given in only 8% of responses (same study) | Program library ships with author and URL per template |
| Engagement decay | Effect SMD 0.29 at ≤8 weeks vs a non-significant 0.06 beyond; authors call it intervention fatigue (https://pmc.ncbi.nlm.nih.gov/articles/PMC12254675/) | Anticipate the week 6–8 cliff in `adherence`; vary the interaction |
| Habit claims overstated | Chatbot effects on exercise-habit and sedentary-behaviour outcomes were not statistically significant (same meta-analysis) | Do not promise habit formation from chat |

Broader reviews reach the same "promising, not definitive" verdict
(https://www.nature.com/articles/s41746-023-00856-1;
https://www.jmir.org/2021/9/e25486/citations — both UNVERIFIED, search snippets
only).

The through-line: **an LLM coach should retrieve and apply, not generate.** Every
failure above is a failure of free generation. Every mitigation is a fixed
artifact — a template, a cue library, a screening algorithm, a progression rule
from slice B.

---

## Program library to seed

Ship a small library of named, published programs. The agent selects from it and
cites it. Do not let the agent write a program from scratch.

| Template | Author / source | Structure | Days | Progression | Free? |
|---|---|---|---|---|---|
| r/Fitness Basic Beginner Routine | https://thefitness.wiki/routines/r-fitness-basic-beginner-routine/ | A/B full-body, 3 lifts each, AMRAP last set | 3 | Fixed increment per session, 10% deload on stall | Yes |
| GZCLP | Cody Lefever, https://swoleateveryheight.blogspot.com/2014/07/the-gzcl-method-simplified_13.html | T1 heavy compound / T2 primary accessory / T3 secondary accessory | 3–4 | AMRAP-driven tier and goal-weight adjustment | Yes |
| Starting Strength | Mark Rippetoe, https://startingstrength.com/get-started | A/B full-body alternation | 3 | Linear, per session | Outline free, method in the book |
| StrongLifts 5x5 | Mehdi, https://stronglifts.com/ | A/B full-body, 5x5 | 3 | Linear | Guide free, app has a paid tier |
| 5/3/1 | Jim Wendler, https://www.jimwendler.com/ | 4 main lifts, wave-based percentages of a training max | 4 | Training-max increment per cycle | Mostly paid; some free posts at https://www.jimwendler.com/blogs/jimwendler-com/tagged/free-5-3-1-program |
| Upper/Lower | No authoritative single source found | 2 upper, 2 lower | 4 | Template-dependent | — |
| Push/Pull/Legs | No authoritative single source found | 3 sessions rotated once or twice | 3 or 6 | Template-dependent | — |
| r/bodyweightfitness Recommended Routine | https://redditbwf.github.io/ , detail at https://antranik.org/rr/ | Full-body push/pull/core/legs plus mobility and skill work | 3 | Progression through movement variants | Yes |

**Licensing note, since friends should be able to replicate this.** Only ship
the templates whose authors publish them free: the r/Fitness routine, GZCLP, and
the bodyweight Recommended Routine. For 5/3/1, StrongLifts, and Starting
Strength, ship a *pointer* and let the user enter their own numbers. Do not
reproduce paid book content.

**Selection criteria.**

| If the user is... | Recommend | Why |
|---|---|---|
| Never trained, wants general strength | r/Fitness BBR or Starting Strength | Simplest possible progression; fewest decisions |
| Under a year, 3 days, wants strength and size | GZCLP | Tiered structure gives both, still linear enough to be automatic |
| No equipment, or travelling | r/bodyweightfitness RR | Only option that needs nothing |
| Linear progression has stalled | 5/3/1 | The r/Fitness wiki itself routes stalled beginners to GZCLP or 5/3/1 for Beginners (https://thefitness.wiki/routines/r-fitness-basic-beginner-routine/) |
| 4 days, hypertrophy focus, some experience | Upper/Lower | Hits every muscle twice weekly, which is the frequency recommendation (https://acsm.org/resistance-training-guidelines-update-2026/) |
| 6 days, experienced, time is not the constraint | Push/Pull/Legs | Same twice-weekly frequency, more volume headroom |
| Fewer than 3 days available | Full-body, whatever the count | Frequency per muscle is what matters, and full-body maximises it at low session counts (https://link.springer.com/article/10.1007/s40279-016-0543-8) |

The frequency evidence behind the last three rows: training a muscle at least
twice a week beats once, though when weekly volume is fully equated the
frequency effect shrinks — frequency mostly matters as the vehicle for fitting
in quality weekly volume
(https://link.springer.com/article/10.1007/s40279-016-0543-8 — UNVERIFIED,
search snippet only).

**Gap.** No credentialed primary source was found for the PPL versus
upper/lower comparison. Search returned only aggregator blogs. Flagged rather
than fabricated. The evidence anchor for both is the frequency literature, not
a split-specific study.

---

## Open questions for the user

I cannot ask directly from this slice, so these are recorded here. They all
block `intake`, and most of them block `program-design`.

1. **Goal.** One primary goal for the next three months: get stronger, get
   bigger, general health, or something specific? The rep and load prescriptions
   genuinely differ.
2. **Training age.** Never trained, under a year, one to three years, or more?
3. **Schedule.** How many days a week will you actually train, and roughly how
   long per session? The honest number, not the one you would like to be true.
4. **Equipment.** Full gym, home setup, or nothing? If there is a barbell: what
   is the smallest plate pair you own? If dumbbells: what is the jump between
   them?
5. **Injuries and health.** Anything that currently hurts, anything a clinician
   has told you to avoid, and the PAR-Q+ answers.
6. **Units.** Kilograms or pounds.
7. **Scope preference.** Should the agent raise sleep and food at all, or stay
   strictly on training? Default in this catalog is a single prompt, then drop
   it.
8. **Two design questions for the squad, not the user.** Does the log store
   `config/` as files (git) or as Notion properties — that decides how
   `trainer-core` reads it (slice A). And does slice B's rule format cover the
   deload and re-entry branches, or only the per-session progression step?

---

## Gaps in this slice

Honest list of what is not nailed down.

- **ACSM 2009 position stand numbers** came from search excerpts. The PDF and
  the PubMed page both blocked fetch. The 2026 stand's numbers *are* verified
  from acsm.org.
- **NSCA's own rep/set/rest-by-goal table** was never confirmed against primary
  text; the NSCA PDF returned binary. ACSM's numbers stand in.
- **Movement-pattern taxonomy** has no confirmed live source. Book-sourced only.
- **Deload evidence** is survey data and expert opinion. No head-to-head trial
  of volume-reduction versus intensity-reduction deloads was found.
- **Detraining** rests on Mujika and Padilla 2000 and Bosquet et al. 2013,
  neither confirmed at content level; the Bosquet URL was never captured.
- **ADHD exercise adherence** has no randomised trial evidence. Body doubling
  has one qualitative study and no controlled trials.
- **FDA general wellness guidance** primary text not fetched; both fda.gov URLs
  404'd.
- **PPL versus upper/lower** has no credentialed source.
- **Warm-up ramp-up sets** have no dedicated peer-reviewed citation; they are
  covered conceptually by RAMP's Potentiate phase.
- **Ottawa ankle/knee rules** were not searched, so "cannot bear weight" is
  unsourced here.
- The session's web search budget ran out partway through, which is why several
  claims above are search-snippet-only rather than fetched.
