# How a team builds a program: the workflow around the plan

Research slice 22. Written 2026-09-06.

In plain words: this file is about who does what, in what order, when a group of
people writes one athlete a training plan. It is the process, not the plan.

Sibling slices: 07 baselining, 08 goal-specific programming, 09 sport-specific
programming, 10 medical and special populations, 12 trainer practice and ethics.

Scope note: slices 08 and 09 own what goes inside the program, and slice 12 owns
the solo trainer's client flow. This one owns the sequence, the authority, and
the handover, and points at the sibling slice wherever a step needs a number.

---

## TL;DR

Three things decide the whole workflow.

1. **The competition calendar is fixed before anyone writes a session.** The
   annual plan is built backwards from dated events. The strength plan is shaped
   last, not first.
2. **The medical gate is a hard stop with a narrow owner.** A physician opens it
   and a physician reopens it after injury. Nobody else may.
3. **Everything else is a negotiation between two departments reporting to one
   person.** Health and coaching are separate lines of authority joined at a
   performance director, and the friction between them is designed in.

### The sequence

| # | Step | Leader | Input | Output | Sign-off |
|---|---|---|---|---|---|
| 0 | Fix the calendar | Sport coach | Fixture list, selection targets | Dated events, ranked by priority | Performance director |
| 1 | Periodic health evaluation | Physician | History, exam, tests | Fitness-to-train status plus restrictions | Physician, with athlete consent |
| 2 | Needs analysis | S&C coach | Sport, position, calendar, restrictions | Needs analysis document | Head coach on sport content |
| 3 | Baseline testing | S&C coach | Athlete availability, test menu | Numbers, and named gaps | S&C coach |
| 4 | Annual plan | S&C coach | Steps 0 to 3 | Macrocycle map, phases, peaks | Head coach, because it costs practice time |
| 5 | Block plan | S&C coach | The annual plan plus current status | Mesocycle, 3 to 6 weeks | S&C coach |
| 6 | Deliver sessions | S&C coach | The block | Logged sets, session RPE | S&C coach |
| 7 | Monitor and review | Sport scientist | Session logs, wellness, medical notes | Readiness status per athlete | Reviewed as a group |
| 8 | Revise, or return to play | Depends on trigger | Step 7 output | An amended plan | See the revision table |

Steps 0 and 1 gate everything below them. Steps 5 to 8 loop, and step 4 reopens
only at a phase boundary or after an injury long enough to cost a phase.

---

## How to read this file

Same grading as slices 08 and 09, minus the trial-backed grades. Process research
has almost no experiments behind it, so the top grade available is a consensus
statement naming who decides.

- **Strong** = consensus statement or governing-body standard, sources agreeing.
- **Moderate** = one consensus paper, or several descriptive accounts agreeing.
- **Practice** = how it is done, described but never tested.
- **UNVERIFIED** = the primary source did not open inside the timebox.

Expect Practice on most rows, and treat any row with a number as the exception.
Every citation points at a stored copy under
`research/sources/22-team-program-workflow/`, and the Sources table at the end
carries the original URL and how faithful the capture is.

---

## 1. The cast

The UK Athletics model, written up after London 2012, is the clearest published
account of who holds what. It splits the support staff into two departments with
separate lines of authority.

| Role | Leads | Decides | Cannot decide |
|---|---|---|---|
| Performance director or CEO | Both departments | Which path to take once the medical opinion is in | Anything clinical where the athlete lacks capacity |
| Chief medical officer | The health department | Clinical policy, and holds ultimate clinical and medicolegal responsibility | Training content |
| Sports medicine physician | The athlete's case | Diagnosis, initial management, referral to specialists | Whether the athlete competes, in the end |
| Physiotherapist | Rehab | Rehab loading, and hands the athlete back to the coach | Diagnosis |
| Head coach | The coaching department, including S&C | Sport content, practice time, selection | Medical decisions |
| S&C coach | The gym plan | Exercise selection, load, block structure | How much practice time is available |
| Sport scientist | Monitoring | What gets measured and how it is reported | The training response to it |
| Athlete | Their own body | Whether to compete on good information, in most cases | Nothing they lack capacity to decide |

[Dijkstra 2014, integrated performance health management model, stored copy](sources/22-team-program-workflow/dijkstra-2014-integrated-performance-health-management-model.md)

Two details are worth keeping.
A clinician line manages the CMO, on purpose, because a non-clinician line
manager puts confidentiality and clinical responsibility at risk.
Referral to outside specialists belongs to the medical department, so a coach who
books an athlete a scan has broken the process even when the scan was a good idea.

The NSCA reaches the same conclusion from the other direction: the scope of
strength and conditioning has grown past what one person can hold, so roles have
to be written down and matched to who is competent at them.
[NSCA strength and conditioning professional standards, stored copy](sources/22-team-program-workflow/nsca-strength-conditioning-professional-standards.md)

---

## 2. The annual layer: the calendar comes first

Nobody designs a training year from the training.
The planning sequence puts every known competition and its location on the sheet
first, ranks them to find where peak performance is needed, and only then cuts
the year into macrocycles.
[Periodization planning steps, stored copy](sources/22-team-program-workflow/human-kinetics-periodization-steps-excerpt.md)

The nesting runs multiyear plan, annual plan, macrocycle, phase, mesocycle,
microcycle, session. The annual plan is written during the transition phase at
the end of the previous year, so the window to write it is the off-season.

The calendar is often not even the club's to set.
A rugby sevens squad's four-year plan to Rio was periodized around World Rugby's
circuit, an external fixture list the coaching staff took as given.
[Robineau 2020, road to Rio rugby sevens case study, stored copy](sources/22-team-program-workflow/road-to-rio-rugby-sevens-periodization-case-study.md)

Two consequences for everyone downstream.

- The sport coach's fixture list is an input, not a topic. Slice 09 carries what
  the phases do to gym volume and intensity.
- The negotiation is over practice time, not training theory. Slice 09 records
  that sport coaches commonly set gym work too, and that the duplication is
  dangerous.

Periodization is also not only about training.
The integrated view periodizes recovery, nutrition, psychological skills, and
skill acquisition against the same calendar, which is why the plan needs sign-off
from people who never write a set or a rep.
[Mujika 2018, integrated periodization, abstract, stored copy](sources/22-team-program-workflow/mujika-2018-integrated-periodization-paper.md)

---

## 3. The medical gate

Two gates, not one, and they have different owners.

### Gate one: entry

A periodic health evaluation is run by a physician with sports medicine
training, ideally the athlete's own team physician, and it needs the athlete's
free and informed consent.
[IOC periodic health evaluation consensus, stored copy](sources/22-team-program-workflow/ioc-periodic-health-evaluation-consensus-statement-2009.md)

A physician who finds a serious risk must strongly discourage continuing, but
the IOC panel leaves the decision to continue with the athlete.
Cardiovascular abnormality is the exception, where external guidelines can
disqualify outright, and the same statement warns against over-disqualifying
findings that are not lethal.

The general-population version of this gate is the ACSM 2015 screening algorithm.
Slice 10 owns it, including the clearance rule and what a clearance letter has to
contain before anyone acts on it.

### Gate two: re-entry after injury or illness

The six-society team physician consensus is blunt about authority.
Coordinating the process with athletic trainers, coaches, and school officials is
desirable. Being ultimately responsible for the return-to-play decision is
essential, and that responsibility sits with the team physician.
[Team physician return-to-play consensus 2012, stored copy](sources/22-team-program-workflow/team-physician-return-to-play-consensus-statement-2012.md)

That statement also puts paperwork before the season starts.
The team physician prepares a letter of understanding with the administration
defining authority, responsibilities, and who makes return-to-play calls, in the
off-season, before there is an injured athlete to argue about.

Return to play is a continuum, not a switch.
The Bern statement splits it into return to participation, return to sport, and
return to performance, and the decision can reverse into a removal from sport at
any point.
It is shared among stakeholders except where the athlete's health is at risk, and
then the clinician acts alone.
[Ardern 2016, Bern return to sport consensus, stored copy](sources/22-team-program-workflow/ardern-2016-return-to-sport-bern-consensus-statement.md)

The mechanism underneath is a comparison, not a checklist.
The StARRT framework assesses risk in two steps, tissue health and the stresses
the activity applies, then compares that against a stated risk tolerance.
Above the tolerance line the answer is no, and the factors people used to call
decision modifiers belong to the tolerance side rather than the assessment side.
Shrier's stated reason for the framework is the useful one for a coach: making
the reasoning explicit reduces conflict, whoever holds the authority.
[Shrier 2015, StARRT framework, stored copy](sources/22-team-program-workflow/shrier-2015-starrt-return-to-play-risk-framework.md)

### Where the sources disagree

| Question | Team physician 2012 | Dijkstra 2014 | Ardern 2016 |
|---|---|---|---|
| Who decides return to play | The team physician, ultimately | The performance director may choose another path once the medical opinion is in | Shared among stakeholders |
| When is one person allowed to act alone | The physician throughout | Never a non-clinician, where the athlete lacks capacity | The clinician, where health is at risk |

This is a real conflict, not a wording difference.
The 2012 statement is written for a US team physician carrying the liability, the
2014 model for a governing body whose athletes are adult professionals and whose
physician advises rather than commands.
Both agree on one hard floor: a non-clinician may never overrule a clinical
decision when the athlete cannot decide for themselves, concussion being the case
they name.

Overruling happens anyway. A 2025 study of one English Championship club recorded
practitioners reporting the head coach overriding medical return-to-play calls.
[Odetoyinbo and McKay 2025, healthcare team and player availability, stored copy](sources/22-team-program-workflow/odetoyinbo-mckay-2025-healthcare-team-player-availability-football.md)

---

## 4. The revision loop

Plans change on a trigger, and the trigger decides who may act and how fast.

| Trigger | Who may change it | How fast | What they may not touch |
|---|---|---|---|
| The athlete is heavy today | S&C coach, alone | In the session | The block's target |
| Missed sessions, poor sleep, high session RPE | S&C coach, alone | Within the week | The medical restrictions |
| Progress has stalled across a block | S&C coach with the head coach | At the block boundary | The calendar |
| The fixture list moved | Head coach, then S&C replans | Immediately | The medical restrictions |
| New pain, new symptom, new diagnosis | Physician | Immediately, and training pauses | The physician's own restriction |
| Cleared to return | Physician, then a graded handover to the coach | Staged over weeks | The stage order |

Slice 12 carries the solo cadence for the first three rows, in "Reassessment,
expectations, realistic rates", and slice 07 carries the re-test cadence.
What the team adds is the readiness layer between them.

Revision does not run on a clock.
The rugby sevens plan was revised at mesocycle grain, roughly every 4 to 7 weeks,
triggered by observed fatigue and by how close the next qualification event was.

UK Athletics ran a real-time readiness status per athlete inside a shared
electronic record, colour coded green, orange, or red, regraded after each
clinical reassessment.
Readiness to compete came out of a discussion between athlete, coach, doctor, and
physiotherapist, and the head coach and athlete then set their own tolerance for
the assessed risk.

Meeting frequency is the closest thing to a measured process variable here.
In that one football club, meetings per two-week period ran a mean of 6.5 with a
range of 5 to 10, and both the count and staff satisfaction with the meetings
correlated positively with player availability.
One club, correlational. Practice with a number attached, not evidence that more
meetings cause availability.

A caution on monitoring data.
A 2026 water polo study of a daily seven-item wellness questionnaire says its own
instrument must not be used alone to diagnose fatigue, quantify adaptation, or
prescribe training changes, and works only as a descriptive aid needing context.
[Water polo wellness questionnaire monitoring study, stored copy](sources/22-team-program-workflow/water-polo-wellness-questionnaire-monitoring-study.md)
Read that as the rule for wellness scores. They start a conversation, and they do
not end one.

---

## 5. What actually moves between people

The workflow is only as good as the artifact each step hands on.

| Artifact | Written by | Read by | When |
|---|---|---|---|
| Ranked competition calendar | Sport coach | Everyone | Once a year, amended on fixture changes |
| Health evaluation record and restrictions | Physician | Physiotherapist, and the coach in summary only | Annual, plus after any event |
| Needs analysis | S&C coach | Head coach | Once per athlete, revisited on position change |
| Test results | S&C coach | Head coach, sport scientist | Every 8 to 12 weeks |
| Annual plan | S&C coach | Head coach, performance director | Written in the transition phase |
| Block plan and session plans | S&C coach | The athlete | Every 3 to 6 weeks |
| Session log and session RPE | S&C coach and athlete | Sport scientist | Every session |
| Readiness status | Sport scientist and clinicians | The whole group | Continuous |
| Letter of understanding on authority | Team physician and administration | The staff | Before the season |
| Progress report to the referring clinician | Trainer or S&C coach | The referring clinician | While the client is medically referred |

The NSCA's standards name three more that a gym is expected to hold: an
emergency response plan, injury and incident reports, and preparticipation and
return-to-participation clearance documents.

The last table row is not optional in the general-population case.
Slice 12's do, do not, refer table lists reporting progress to the referring
professional as a trainer's duty, and monitoring a medically referred client
without that reporting line as outside scope.

Note what the coach does not receive. The physician's record stays clinical, the
coach gets a status and a restriction, and confidentiality sits on the
clinician's side of the line.

---

## 6. The single practitioner

One person can hold most of this. They cannot hold all of it, and the parts they
cannot hold are the parts that exist to catch their own blind spots.

Working alone is also the normal case, not the degraded one.
In a survey of Czech football clubs the biggest reported barrier to monitoring
was staffing, not knowledge: 74.5% cited a lack of resources, and 75% of the S&C
coaches answering named human resources specifically.
[Bokuvka 2025, Czech football load monitoring survey, stored copy](sources/22-team-program-workflow/czech-football-training-load-monitoring-survey.md)

### What merges

| Team steps | Collapses to | Why it is safe to merge |
|---|---|---|
| 2, 3, 4, 5 | One planning sitting | The negotiation between needs analysis, testing, and plan is internal. There is no second party to convince, so the artifacts merge into one written plan. |
| 6 and 7 | The session itself | The person delivering the session is the person reading the data. The readiness status collapses into asking the client how they are and watching the first working set. |
| Performance director, head coach, S&C coach, sport scientist | The practitioner | All four are the same interests once the client's own goal is the performance strategy. |

### What survives

| Team step | Survives as | Why it cannot go |
|---|---|---|
| 0, fix the calendar | Ask what the client is training for and when it happens | Without a date the plan has no shape. This is slice 09's second question for a reason. |
| 1, medical gate | Screen, then refer, then wait for the letter | The practitioner cannot sign their own clearance. This is the one step where the second person is structural. |
| 4, the written annual plan | A written plan the client can read | The plan is the handover to your future self. A plan held in one head has no reviewer at all. |
| 8, revise on a trigger | The same trigger table, minus the authority column | The triggers are properties of the athlete, not of the staff structure. |
| The progress report | A note back to the referring clinician | Slice 12 puts this inside scope. Skipping it puts monitoring a referred client outside it. |
| The letter of understanding | A named referral list, chosen before anyone needs it | Same function, one person. Decide in advance who the physician, the physiotherapist, and the dietitian are. |

### What vanishes

- The meeting cadence. There is nobody to meet.
- The chain of command, and every artifact whose only job is to move information
  between people who do not share a room.
- The colour-coded shared record. The status survives as a note to self.
- The negotiation over practice time, unless the client has their own sport
  coach, and then it returns exactly as written in section 2.

### The one step that never collapses

Medical clearance.
Both scope-of-practice bodies define the personal trainer's job as starting with
people who are healthy or already cleared, and as recognising the limit of their
own expertise and referring out.
[NSCA scope of practice for personal trainers, stored copy](sources/22-team-program-workflow/nsca-ptq-scope-of-practice-personal-trainers.md),
[ACSM certified personal trainer exam content outline, stored copy](sources/22-team-program-workflow/acsm-cpt-exam-content-outline.md)

So the lone practitioner's version of the performance team is a referral list.
The team physician statement settles authority in the off-season, before an
injury exists. The solo equivalent is to know the names before the client needs
them, because the moment you need a physiotherapist is the worst moment to start
looking for one.

### What an agent occupies

An AI coach sits in the same seat as the lone practitioner.
Slices 10 and 12 already fix what it must refuse and what it must say instead,
and this workflow adds nothing to that list.
What it adds is the shape of the seat: an agent can hold steps 0 and 2 to 8, and
step 1 always ends in a human clinician.

---

## 7. Open questions for the user

1. Does the agent ever coach someone who has a real coach? If yes, section 2's
   negotiation is live and the agent has to ask what that coach already sets.
2. Where does the referral list live? It is the single-practitioner replacement
   for the whole health department, and nothing in the repo currently holds one.
3. Does the written plan get shown to the client, or only used to generate the
   next session? The team answer is that a plan is something somebody else reads.

---

## 8. Gaps and confidence

- The 2023 update of the team physician consensus statement is paywalled. The
  stored 2012 version answers the authority question, but the wording may have
  moved.
- Mujika 2018 is stored as a truncated abstract. Everything cited from it is in
  the part that came through.
- The periodization planning steps come from a publisher's excerpt page, not
  Bompa and Haff's book. `UNVERIFIED` against the book itself.
- The meeting-frequency numbers are one club, one season, correlational.
- No open source names a protocol for the S&C coach and the head coach
  negotiating training load. Section 2 says the negotiation exists and does not
  say how it is run.
- No source describes a single practitioner's workflow as a workflow. Section 6
  derives the collapse from what the team sources say each step is for and what
  the scope documents forbid. That derivation is mine, not a citation.
- The water polo record's title and DOI came from a search listing rather than
  from the stored page. Treat the title as unverified.

---

## Sources

All stored under `research/sources/22-team-program-workflow/`.

| File | Title | Originator | Year | Capture |
|---|---|---|---|---|
| `dijkstra-2014-integrated-performance-health-management-model.md` | Managing the health of the elite athlete: a new integrated performance health management and coaching model | Dijkstra, Pollock, Chakraverty, Alonso, BJSM 48(7) | 2014 | Raw full text, CC BY-NC |
| `team-physician-return-to-play-consensus-statement-2012.md` | The team physician and the return-to-play decision: a consensus statement | AAFP, AAOS, ACSM, AMSSM, AOSSM, AOASM | 2012 | Raw PDF |
| `ioc-periodic-health-evaluation-consensus-statement-2009.md` | IOC consensus statement on periodic health evaluation of elite athletes | IOC Medical Commission | 2009 | Raw PDF, excerpted |
| `ardern-2016-return-to-sport-bern-consensus-statement.md` | 2016 consensus statement on return to sport, Bern | Ardern et al., BJSM | 2016 | Raw PDF, excerpted |
| `shrier-2015-starrt-return-to-play-risk-framework.md` | Strategic Assessment of Risk and Risk Tolerance (StARRT) framework | Shrier, BJSM | 2015 | Raw PDF, excerpted |
| `odetoyinbo-mckay-2025-healthcare-team-player-availability-football.md` | Performance and healthcare team processes and structure impact player availability | Odetoyinbo, McKay et al., BMJ Open SEM | 2025 | Raw HTML |
| `mujika-2018-integrated-periodization-paper.md` | An integrated, multifactorial approach to periodization | Mujika, Halson, Burke, Balagué, Farrow, IJSPP 13(5) | 2018 | Abstract only, truncated |
| `human-kinetics-periodization-steps-excerpt.md` | Basic steps in the periodization training process | Human Kinetics excerpt page | Undated | Rendered extraction |
| `nsca-strength-conditioning-professional-standards.md` | NSCA strength and conditioning professional standards and guidelines | NSCA, Strength and Conditioning Journal 39(6) | 2017 | Raw PDF |
| `nsca-ptq-scope-of-practice-personal-trainers.md` | The scope of practice for personal trainers | Kompf, Tumminello, Nadolsky, NSCA PTQ 1(4) | 2014 | Raw PDF, re-hosted copy |
| `acsm-cpt-exam-content-outline.md` | ACSM certified personal trainer exam content outline | ACSM | 2025 | Raw PDF |
| `road-to-rio-rugby-sevens-periodization-case-study.md` | Road to Rio: workload periodization in a rugby sevens squad | Robineau et al., Frontiers | 2020 | Rendered extraction |
| `czech-football-training-load-monitoring-survey.md` | Training load and fitness monitoring in Czech football | Bokuvka et al., Frontiers | 2025 | Rendered extraction |
| `water-polo-wellness-questionnaire-monitoring-study.md` | Modified wellness questionnaire for short-term monitoring in elite male water polo players | Varga et al., Frontiers in Sports and Active Living | 2026 | Rendered extraction |

Each stored file carries a provenance header with the source URL, the retrieval
date, and how faithful the capture is. Sibling slices cited: 07, 08, 09, 10, 12.
