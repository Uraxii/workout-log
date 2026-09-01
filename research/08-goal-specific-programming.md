# Goal-specific programming: how the plan changes with the goal

Research slice 08. Written 2026-08-31.

Sibling slices: 07 baselining, 09 sport-specific, 10 medical and special
populations, 11 transgender athletes, 12 trainer practice. This file covers
goal-driven program design for general clients: not clinical, not sport-specific.

Scope note from the user: "There will be all kinds of different ways to train
based on what the goals are... Life-style mobility, achievements, flexibility,
general strength, cardiovascular health. This is not an exhaustive list." The
nine goals below are the ones a general-population trainer agent will meet most.
The list is open. Section 12 says what to do when a goal is not on it.

---

## TL;DR

The goal picks the model. Everything else follows from that one choice.

| # | Client goal | Primary driver | Model | Progression | Sessions/wk |
|---|---|---|---|---|---|
| 1 | General health / longevity | Weekly minutes | Guideline dose, not periodized | Minutes then intensity | 3-5 |
| 2 | Maximal strength | Load | Linear -> block or DUP | Load per session/week | 3-4 |
| 3 | Hypertrophy | Weekly hard sets | Volume progression, MEV->MRV | Sets per week, then load | 3-5 |
| 4 | Cardio fitness | Weekly duration + intensity mix | Polarized or pyramidal | Duration first, intervals second | 3-5 |
| 5 | Mobility / flexibility | Weekly stretch time per muscle | Daily dose, low ceremony | Total time, then range | 3-7 (short) |
| 6 | Skill "achievement" | Practice frequency | Skill ladder + strength base | Rung, not load | 3-6 (short) |
| 7 | Fat loss / recomp | Diet; training preserves muscle | Hypertrophy template + cardio | Hold loads, add steps | 3-5 |
| 8 | Power / athleticism | Movement speed | Low-volume quality work | Intent and height, not fatigue | 2-4 |
| 9 | Two goals at once | Priority ranking | Concurrent with a stated first goal | Priority goal progresses, other maintains | 4-6 |

**The one rule that generalizes:** name the primary goal, program it properly,
and run everything else at maintenance dose. Two priorities is zero priorities.

---

## How to read this file

Every claim carries a source URL. Evidence quality is graded on each section:

- **Strong** = multiple meta-analyses or a position stand, consistent direction.
- **Moderate** = a meta-analysis or several RCTs, real heterogeneity.
- **Weak** = few trials, small samples, or extrapolation from adjacent findings.
- **Practice** = coaching convention with no direct trial support. Usable, but
  say so out loud.
- **UNVERIFIED** = I could not open the primary source inside the timebox.

---

## Shared vocabulary: the seven programming variables

Every goal below is described with the same seven knobs. This is the ACSM
framing and it is the one the agent should use internally.

| Variable | What it means | Who cares most |
|---|---|---|
| Frequency | Sessions per week; exposures per muscle or per system | Skill, hypertrophy |
| Intensity | %1RM, RPE/RIR, %HRmax, zone | Strength, cardio |
| Volume | Sets x reps, or minutes | Hypertrophy, cardio |
| Exercise selection | Which movements, which ranges | Hypertrophy, mobility |
| Rest | Between sets, between intervals | Strength, power |
| Tempo | Time under tension, eccentric control | Weakest lever of the seven |
| Exercise order | What comes first in the session | Concurrent goals, power |

The ACSM 2009 position stand names progressive overload, specificity and
variation as the organising principles, and recommends ordering large before
small muscle groups, multi-joint before single-joint, and higher intensity
before lower intensity ([ACSM 2009, PMID 19204579](https://pubmed.ncbi.nlm.nih.gov/19204579/)).
It also says the benefits of periodization typically show up after about six
months of continuous training, which is the reason novices do not need it (same
source).

**Currency warning.** ACSM published a new resistance training position stand
in April 2026, "Resistance Training Prescription for Muscle Function,
Hypertrophy, and Physical Performance in Healthy Adults: An Overview of
Reviews", an umbrella review of over 137 studies and 30,000+ participants
([ACSM announcement](https://acsm.org/science-spotlight-acsm-releases-new-position-stand-on-resistance-training/),
[PMID 41843416](https://pubmed.ncbi.nlm.nih.gov/41843416/)). I could not open
either abstract inside the timebox, so its specific numbers are **UNVERIFIED**
here. Anything in this file sourced to ACSM 2009 must be re-checked against the
2026 stand before it ships in a trainer agent. That is open question 1.

---

## Goal 1: General health and longevity

**Evidence quality: Strong.** This is the best-sourced goal in the file.

### The dose

| Source | Aerobic | Strength | Note |
|---|---|---|---|
| PAG 2018 (US) | 150-300 min moderate, or 75-150 min vigorous, or equivalent mix | 2+ days/wk, all major muscle groups | 10-minute bout minimum was removed |
| WHO 2020 | 150-300 min moderate, or 75-150 min vigorous | 2+ days/wk | Adds "reduce sedentary time", unquantified |
| ACSM 2011 | >=150 min/wk moderate, or >=75 min vigorous, 500-1000 MET-min/wk | 2-3 days/wk | Adds neuromotor work (balance, agility) 2-3 days/wk |

Sources: [PAG 2018 summary, PMID 30418471](https://pubmed.ncbi.nlm.nih.gov/30418471/),
[PAG 2018 full PDF](https://www.niddk.nih.gov/-/media/Files/Diet-Nutrition/Physical_Activity_Guidelines_2nd_edition.pdf),
[WHO 2020, PMID 33239350](https://pubmed.ncbi.nlm.nih.gov/33239350/),
[WHO recommendations, NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK566046/),
[ACSM 2011, PMID 21694556](https://pubmed.ncbi.nlm.nih.gov/21694556/).

### The mortality curve

Arem et al. 2015 pooled six cohorts and mapped the dose-response against the
7.5 MET-hr/wk guideline minimum. Versus no leisure-time activity: below the
minimum, 20% lower mortality; 1-2x the minimum, 31%; 2-3x, 37%. Benefit
plateaus at 3-5x the minimum (39%), and there was no harm signal even at 10x
([PMID 25844730](https://pubmed.ncbi.nlm.nih.gov/25844730/)).

Two consequences for the agent:

1. **The steepest part of the curve is the first hour a week.** A sedentary
   client going from zero to 60 min/wk captures most of the available benefit.
   Program for adherence, not optimality.
2. **The ceiling is soft.** There is no evidence-based reason to cap a
   motivated client at 300 min, and no evidence of harm at very high volumes in
   this dataset.

Also note PAG 2018's own figure: about 80% of US adults meet neither the aerobic
nor the strength guideline; roughly half meet the aerobic one
([PAG 2018](https://www.niddk.nih.gov/-/media/Files/Diet-Nutrition/Physical_Activity_Guidelines_2nd_edition.pdf)).
The realistic comparison for a new client is not "optimal" but "nothing".

### Programming variables

| Variable | Prescription |
|---|---|
| Frequency | 3-5 days aerobic, 2-3 days resistance, spread across the week |
| Intensity | Mostly moderate (talk test: can talk, can't sing); some vigorous |
| Volume | 150 min/wk target, 300 min/wk stretch; RT 1-3 sets x 8-12 per major group |
| Selection | Compound, machine-or-free, whatever the client will actually do |
| Rest | Not a priority variable; 60-90 s is fine |
| Tempo | Controlled; not a programmed variable |
| Order | Not a priority variable |

### Progression model

Minutes first, then intensity, then load. Add roughly 10-20% of weekly minutes
at a time, hold for 2-3 weeks, repeat. No periodization: there is no evidence a
sedentary adult needs a mesocycle structure, and ACSM's own note that
periodization pays off after ~6 months of training says the opposite
([ACSM 2009](https://pubmed.ncbi.nlm.nih.gov/19204579/)).

### Beginner / intermediate / advanced

- **Beginner:** anything, consistently. Target the guideline floor over 8-12 weeks.
- **Intermediate:** hit 150-300 min plus 2 lifting days. Add neuromotor work per ACSM 2011.
- **Advanced:** they are no longer a "general health" client. Ask what they
  actually want and re-route to another goal.

### Common mistakes

- Prescribing a physique program to someone who asked to be healthy.
- Treating 150 min as a threshold rather than a point on a curve. Under-dose
  still beats zero ([Arem 2015](https://pubmed.ncbi.nlm.nih.gov/25844730/)).
- Dropping the strength half. It is the half most people skip and it is in
  every guideline.
- Adding complexity that costs adherence. The dose you complete beats the dose
  you design.

---

## Goal 2: Maximal strength

**Evidence quality: Strong for load and specificity; moderate for periodization
structure.**

### The core finding

Load matters for strength in a way it does not for size. Schoenfeld et al. 2017
compared low load (<=60% 1RM) with high load (>60% 1RM), all sets to failure:
maximal strength gains favour heavy loads, while hypertrophy is achievable
across the loading spectrum ([PMID 28834797](https://pubmed.ncbi.nlm.nih.gov/28834797/)).

Strength is also more specific than size. It expresses in the tested lift, at
the tested load, in the tested position. Practice the lift you want to be
strong at ([ACSM 2009](https://pubmed.ncbi.nlm.nih.gov/19204579/)).

### Programming variables

| Variable | Prescription |
|---|---|
| Frequency | 3-4 sessions/wk; 2-3 exposures/wk per main lift |
| Intensity | 80-95% 1RM for the main work; RIR 1-3 on top sets |
| Volume | 3-6 sets x 1-6 reps per main lift; accessory work at higher reps |
| Selection | Squat, bench, deadlift, press, plus close variations. Few exercises, repeated |
| Rest | 3-5 min between heavy sets. Rest is a load-enabler, not wasted time |
| Tempo | Controlled eccentric, intent to move the bar fast concentrically |
| Order | Competition lift first, always, while fresh |

Rest: Schoenfeld et al. 2016 found 3-minute inter-set rest beat 1-minute for
both strength and hypertrophy in trained men over 8 weeks
([PMID 26605807](https://pubmed.ncbi.nlm.nih.gov/26605807/),
[JSCR full text](https://journals.lww.com/nsca-jscr/fulltext/2016/07000/longer_interset_rest_periods_enhance_muscle.3.aspx)).
For a strength goal specifically, short rest has no upside.

### Frequency

Grgic et al. 2018 found higher frequency produced greater strength gains
overall, but the effect disappeared in the volume-equated subgroup
([PMID 29470825](https://pubmed.ncbi.nlm.nih.gov/29470825/),
[PMC6081873](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6081873/)).
Read that as: frequency is a delivery mechanism for volume and practice, not an
independent magic variable. Practically, 2-3x/wk per lift lets you spread the
volume and get more skill reps at heavy loads.

### Periodization

Williams et al. 2017 meta-analysed periodized versus non-periodized resistance
training for maximal strength: periodized won, d = 0.43, dropping to d = 0.23
after adjusting for funnel-plot asymmetry
([Sports Medicine 2017](https://link.springer.com/article/10.1007/s40279-017-0734-y)).
Real, but small. And a meta-analysis of linear versus daily undulating
periodization for hypertrophy found no meaningful difference between the two
models ([PMID 28848690](https://pubmed.ncbi.nlm.nih.gov/28848690/)).

The honest summary: **having a plan beats not having one; which plan matters
much less than the internet suggests.**

| Model | What it is | Best fit |
|---|---|---|
| Linear progression | Add load every session until it stops working | Novice, 0-9 months |
| Block / linear periodization | Volume phase -> intensity phase -> peak | Intermediate with a test date |
| DUP | Rotate rep ranges within the week (heavy/medium/light) | Intermediate, no test date |
| Conjugate | Rotating max-effort and dynamic-effort days, varied lifts | Advanced, needs equipment and coaching. **Practice-grade evidence** |

### Beginner / intermediate / advanced

- **Beginner (0-9 mo):** linear progression. Add 2.5-5 kg to lower-body lifts and
  1-2.5 kg to upper-body lifts per session while form holds. No periodization
  needed ([ACSM 2009](https://pubmed.ncbi.nlm.nih.gov/19204579/)).
- **Intermediate (9 mo - 2-3 yr):** weekly rather than session progression. DUP
  or a simple block. Introduce deloads every 4-8 weeks.
- **Advanced:** monthly-to-quarterly progression, block or conjugate, planned
  peaking, autoregulation via RPE or velocity.

### Common mistakes

- Training strength with hypertrophy rep ranges and calling it strength work.
- Cutting rest to "keep the heart rate up" during a strength block. Directly
  contradicted ([Schoenfeld 2016](https://pubmed.ncbi.nlm.nih.gov/26605807/)).
- Rotating exercises constantly. Strength is specific; variation is for
  hypertrophy and for joint sanity, not for the tested lift.
- Running a novice through a block periodization spreadsheet.

---

## Goal 3: Hypertrophy and physique

**Evidence quality: Strong for volume and load; moderate for frequency,
proximity to failure and exercise selection.**

### Volume is the primary driver

Schoenfeld, Ogborn and Krieger 2017 pooled 15 volume-manipulation trials: each
additional weekly set added ~0.37% to hypertrophy gains, with <5 sets/wk
sub-optimal, 5-9 better, and 10+ best
([PMID 27433992](https://pubmed.ncbi.nlm.nih.gov/27433992/)).

A newer meta-regression set re-examined the shape of that curve across linear
and non-linear forms
([PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/),
[SportRxiv preprint](https://sportrxiv.org/index.php/server/preprint/view/460)).
I did not open the full text; **its exact plateau point is UNVERIFIED here** and
is open question 2.

Working range for the agent: **10-20 hard sets per muscle per week**, entered at
the low end and progressed.

### Volume landmarks (RP framework)

Renaissance Periodization's MV / MEV / MAV / MRV vocabulary is the most usable
planning frame, but note that it is a **coaching model layered on top of the
volume literature, not a finding in its own right**
([RP Strength](https://rpstrength.com/blogs/articles/training-volume-landmarks-muscle-growth)).

| Landmark | Meaning | Typical intermediate value |
|---|---|---|
| MV | Maintains current size | ~6 sets/muscle/wk |
| MEV | Fewest sets that still grow | 4-8 sets/muscle/wk |
| MAV | Best return per unit of effort | 12-20 sets/muscle/wk |
| MRV | Most you can recover from | 18-30 sets/muscle/wk |

Treat the specific numbers as **Practice-grade**. The MV number is the most
useful one in the whole table, because it is what you drop a secondary muscle
group to when the client's priority is elsewhere.

### Load and rep range

Hypertrophy is load-tolerant: similar growth from roughly 30% to 85% 1RM when
sets are taken close to failure ([Schoenfeld 2017](https://pubmed.ncbi.nlm.nih.gov/28834797/)).
Use 6-12 as the default because it is the most time-efficient, not because
other ranges fail. Heavy work (<6) fatigues joints; very light work (>20)
fatigues willpower.

### Proximity to failure

Refalo et al. 2023 found only a trivial-to-small hypertrophy advantage for sets
taken to failure versus stopping short (ES ~0.15-0.21 across analyses,
15 studies) ([PMID 36334240](https://pubmed.ncbi.nlm.nih.gov/36334240/),
[PMC9935748](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9935748/)). A 2024
meta-regression extended this to a dose-response between estimated proximity to
failure, strength and hypertrophy
([PMID 38970765](https://pubmed.ncbi.nlm.nih.gov/38970765/)).

Practical: **0-3 RIR on most sets.** Failure buys little and costs recovery,
which costs volume, which is the thing that actually drives growth.

### Frequency

Volume-equated, frequency does not meaningfully change hypertrophy; pick what
lets the client distribute their sets
([Schoenfeld & Grgic review](https://www.sciencedirect.com/science/article/abs/pii/S1440244018308624)).
2x/muscle/wk is the pragmatic default because it splits 10-20 sets into
chunks that are actually completable.

### Exercise selection and regional hypertrophy

- Training at long muscle lengths beats short: partial reps at long muscle
  length produced greater hypertrophy than at short length, ES = 0.283
  ([Sport Sciences for Health 2025](https://link.springer.com/article/10.1007/s11332-025-01586-5)).
- Lengthened partials produce adaptations similar to full ROM in trained people
  ([PMID 39959841](https://pubmed.ncbi.nlm.nih.gov/39959841/),
  [PeerJ full text](https://peerj.com/articles/18904/)).
- Regional (within-muscle) differences by exercise are real but the evidence is
  thin and heterogeneous; treat exercise-for-a-specific-head claims as
  **Weak** ([PMC10407320](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10407320/)).

Selection rule: pick exercises that load the target muscle in a stretched
position, that the client can add load to, and that do not hurt.

### Rest and tempo

3 minutes beats 1 minute for hypertrophy too
([Schoenfeld 2016](https://pubmed.ncbi.nlm.nih.gov/26605807/)). Use 2-3 min for
compounds, 60-90 s for isolation. Tempo is the weakest of the seven variables;
"control the eccentric, don't bounce" is the whole prescription.

### Beginner / intermediate / advanced

- **Beginner:** 8-10 sets/muscle/wk, full-body 3x, focus on learning the lifts.
  Load progression alone drives growth for months.
- **Intermediate:** 12-18 sets/muscle/wk, upper/lower or push/pull/legs,
  progress sets across a 4-6 week block then deload.
- **Advanced:** approach MRV within a block, specialize one or two muscle
  groups per block while holding the rest at MV, deload deliberately.

### Common mistakes

- Chasing failure on every set and losing the volume that matters
  ([Refalo 2023](https://pubmed.ncbi.nlm.nih.gov/36334240/)).
- Novelty for its own sake. Progressive overload needs a stable exercise.
- Counting warm-up sets in weekly volume.
- Starting at MRV. There is nowhere to progress to.

---

## Goal 4: Cardiovascular fitness and endurance

**Evidence quality: Strong for HIIT vs moderate on VO2max; moderate for
intensity distribution models; weak for the 10% rule.**

### Zone models

Two live systems. Do not mix them in one sentence to a client.

| 3-zone (Seiler) | 5-zone (common in cycling/running) | Marker |
|---|---|---|
| Z1 easy | Z1-Z2 | Below first lactate threshold / can hold conversation |
| Z2 threshold | Z3-Z4 (tempo, threshold) | Between LT1 and LT2 |
| Z3 hard | Z5 | Above second threshold / VO2max work |

Seiler's descriptive work on elite endurance athletes found a converging
pattern: roughly 75-80% of sessions at low intensity and 15-20% with
substantial high-intensity work, i.e. **polarized**
([Seiler & Kjerland 2006, PMID 16430681](https://pubmed.ncbi.nlm.nih.gov/16430681/),
[Seiler 2010, PMID 20861519](https://pubmed.ncbi.nlm.nih.gov/20861519/)).

A caution the agent must carry: **that distribution was observed in athletes
training 10-13 times per week.** A client training 3 times a week is not
running an 80/20 split; they are running three sessions and the labels barely
apply. Applying elite intensity distribution to low-volume trainees is the most
common misuse of Seiler's work. **Practice-grade extrapolation.**

Recent syntheses support polarized over other distributions, especially in
interventions under 12 weeks and in highly trained athletes
([PMC11329428](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11329428/),
[PMC11679080](https://pmc.ncbi.nlm.nih.gov/articles/PMC11679080/)).

| Distribution | Shape | Best fit |
|---|---|---|
| Polarized | Lots of easy, some hard, almost no middle | High volume, high training age, short blocks |
| Pyramidal | Most easy, some threshold, least hard | Base building, marathon-type goals |
| Threshold | Heavy on the middle zone | Time-crunched; risks accumulating fatigue with little adaptation |

### HIIT protocols

| Protocol | Structure | Evidence |
|---|---|---|
| Norwegian 4x4 | 4 x 4 min @ 90-95% HRmax, 3 min active recovery @ 70% | Helgerud 2007: beat long slow distance and lactate-threshold work for VO2max at matched total work; ~7% VO2max in 8 weeks, 3x/wk ([PDF](https://rcc.hslu.ch/fileadmin/user_upload/downloads/sport/Aerobic_High-Intensity_Intervals_Improve_J.Helgerud_2007.pdf), [Semantic Scholar](https://www.semanticscholar.org/paper/Aerobic-high-intensity-intervals-improve-VO2max-Helgerud-H%C3%B8ydal/263bb580cc0f447793be7a49db7cdca326794e19)) |
| 15/15 | 15 s @ 90-95% HRmax / 15 s active rest | Same trial, similar VO2max effect to 4x4 |
| Tabata | 20 s @ ~170% VO2max / 10 s rest, 8 rounds | Tabata 1996: VO2max +7 ml/kg/min AND anaerobic capacity +28%; moderate training improved neither anaerobically ([Waseda record](https://waseda.elsevierpure.com/en/publications/effects-of-moderate-intensity-endurance-and-high-intensity-interm/)) |
| SIT (sprint intervals) | 20-30 s all-out, long recovery | Effective but supramaximal; aerobic 4x4-style intervals appear superior for VO2max in well-trained men ([PMC10099854](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10099854/)) |

Buchheit & Laursen's two-part framework is the right mental model for
prescribing intervals: work duration, relief duration, relief intensity,
number of reps, series structure, and exercise mode are all independent knobs
([Part I, PMID 23539308](https://pubmed.ncbi.nlm.nih.gov/23539308/),
[Springer](https://link.springer.com/article/10.1007/s40279-013-0066-5)).

**Tabata caveat for a general client:** the original protocol was performed on
a cycle ergometer at ~170% VO2max by trained subjects. What gyms call "Tabata"
is usually neither the intensity nor the modality. Say so.

### Modality notes

| Modality | Notes |
|---|---|
| Running | Highest impact load, highest injury rate, no equipment. Also the modality that interferes most with lifting (see Goal 9) |
| Cycling | Low impact, easy to control intensity, least interference with lifting |
| Rowing | Whole-body, technique-dependent, back fatigue overlaps with deadlifts |
| Swimming | Lowest joint load, highest skill barrier; heart rate runs lower than on land, so HR zones need offsetting. **Practice-grade** |

### Progression and the 10% rule

The "increase weekly volume by no more than 10%" rule is **not supported by the
trial that tested it.** Buist et al. 2008 (GRONORUN) randomised 532 novice
runners to a graded 13-week 10%-rule program or a standard 8-week program:
injury incidence was 21% vs 20%, no difference
([PMID 17940147](https://pubmed.ncbi.nlm.nih.gov/17940147/),
[SAGE](https://journals.sagepub.com/doi/abs/10.1177/0363546507307505)).
The wider training-error literature is similarly weak
([PMC3290924](https://pmc.ncbi.nlm.nih.gov/articles/PMC3290924/)), though
Nielsen et al. 2014 did find that large weekly distance jumps associate with
specific injury types
([JOSPT](https://www.jospt.org/doi/10.2519/jospt.2014.5164)).

Agent policy: **use gradual progression as a sane default, but do not present
the 10% rule as evidence-based injury prevention.** Say it is a convention.

Couch-to-5k style run/walk progressions are **Practice-grade**: widely used,
well-liked, no controlled evidence I could find that the specific interval
ladder beats any other gradual ramp. That is open question 3.

### Programming variables

| Variable | Prescription |
|---|---|
| Frequency | 3-5 sessions/wk; at least 1 hard, rest easy |
| Intensity | 80% of session time easy, 20% hard, once volume supports it |
| Volume | Duration first. Build a base of easy minutes before adding intervals |
| Selection | The modality of the goal; cross-train to manage impact load |
| Rest | Interval-specific; 4x4 uses 3 min active recovery |
| Tempo | n/a (cadence and technique substitute) |
| Order | Hard days not stacked back-to-back; 48 h between hard sessions |

### Beginner / intermediate / advanced

- **Beginner:** all easy work plus run/walk or equivalent. Build to 20-30
  continuous minutes before any interval work.
- **Intermediate:** one interval session and one longer session per week, rest
  easy. Pyramidal is fine here.
- **Advanced:** polarized, periodized around an event, two hard sessions a
  week, deliberate taper.

### Common mistakes

- The grey-zone trap: every session at moderate-hard. Too hard to recover from,
  too easy to drive VO2max ([Seiler 2010](https://pubmed.ncbi.nlm.nih.gov/20861519/)).
- Adding intervals before a base exists.
- Selling 80/20 to a client who trains 3 hours a week.
- Presenting the 10% rule as injury-proofing ([Buist 2008](https://pubmed.ncbi.nlm.nih.gov/17940147/)).

---

## Goal 5: Mobility versus flexibility

**Evidence quality: Strong for stretching increasing ROM; moderate for dose;
weak-to-absent for branded systems and for "mobility work prevents injury".**

### The distinction matters

- **Flexibility** = passive range of motion. What a joint allows when something
  else moves it.
- **Mobility** = active range of motion under control. What the client can
  reach and own using their own muscles.

The gap between the two is not tissue-limited: subjects consistently reach more
range passively than actively, which is a nervous-system control problem rather
than a tissue-length problem
([Motive Training review of the FRC evidence](https://www.movewithpurpose.com/is-frc-evidence-based) —
**secondary source, use with care**). That gap is the entire argument for
training end-range strength rather than only stretching.

### Dose

The frequently-quoted "5 minutes per week per muscle" figure traces to Thomas
et al. 2018, which analysed stretching typology and duration against ROM
outcomes (International Journal of Sports Medicine; I could only reach a
[mirrored PDF](https://paulogentil.com/pdf/The%20Relation%20Between%20Stretching%20Typology%20and%20Stretching%20Duration%20-%20The%20Effects%20on%20Range%20of%20Motion.pdf),
so the exact figure is **UNVERIFIED** against the publisher version).

Better-sourced modern dose work:

- Total weekly stretch duration matters more than the length of any individual
  bout ([Chronic effects of stretching on ROM with moderators](https://www.sciencedirect.com/science/article/pii/S2095254623000571)).
- A 2024 multivariate meta-regression on optimising static stretching dose for
  flexibility ([PMID 39614059](https://pubmed.ncbi.nlm.nih.gov/39614059/),
  [Sports Medicine](https://link.springer.com/article/10.1007/s40279-024-02143-9)).
- Mechanisms behind ROM change are mostly stretch-tolerance, not permanent
  tissue lengthening, in typical durations
  ([PMID 40180774](https://pubmed.ncbi.nlm.nih.gov/40180774/)).

Working prescription: **~5-10 min per week per target muscle, accumulated in any
bout size, held for 30-60 s at a time, most days.**

### Static vs dynamic vs PNF, and when to do them

Behm et al. 2016 systematic review of acute effects: static stretching -3.7%
performance, dynamic +1.3%, PNF -4.4%, small-to-moderate, largest when testing
happens immediately afterwards; prolonged static stretching over ~60 s per
muscle group without a proper dynamic warm-up is where the acute decrement
shows up
([Northampton record](https://pure.northampton.ac.uk/en/publications/acute-effects-of-muscle-stretching-on-physical-performance-range-/),
[earlier Behm & Chaouachi review, PMID 21373870](https://pubmed.ncbi.nlm.nih.gov/21373870/)).

| Type | Use it | Avoid it |
|---|---|---|
| Dynamic | Warm-up, before anything explosive | Not a ROM-building tool on its own |
| Static | After training, or as a standalone session | Long holds immediately before power or strength work |
| PNF | Standalone ROM sessions, larger acute ROM gains | Immediately pre-performance |
| Loaded stretching | Combined ROM + hypertrophy stimulus | As a substitute for training volume |

### Loaded and long-duration stretching

Warneke et al. 2024 meta-analysed chronic static stretching for maximal
strength and hypertrophy: small strength increases (d = 0.30), with stretching
duration and intervention length as significant moderators
([PMID 38637473](https://pubmed.ncbi.nlm.nih.gov/38637473/),
[Sports Medicine - Open](https://link.springer.com/article/10.1186/s40798-024-00706-8)).
A companion multilevel meta-analysis on hypertrophy found only a trivial
positive effect overall; where growth appeared, the protocols used **>=15 min
per session, >=5 sessions/wk, >6 weeks**
([PMC11438763](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11438763/)).

Translation for a client: stretching to build muscle is technically real and
practically absurd for a general population. It requires more time than
lifting. Do not program it as a hypertrophy tool. Do use loaded stretching as
an efficient way to combine ROM work with training you are doing anyway.

### FRC, CARs, PAILs/RAILs

The underlying concepts (active end-range control, isometrics at end range) are
defensible and overlap with mainstream eccentric and isometric training. The
**branded system is not itself evidence-based**: I found one registered trial
of FRC for chronic non-specific low back pain
([NCT03456050](https://clinicaltrials.gov/study/NCT03456050)) and no published
efficacy meta-analysis for the system as a whole. **Weak / Practice-grade.**

Agent policy: teach the mechanism (train the range you want to own, actively,
under load), name the branded terms only if the client uses them, and never
claim the brand is validated.

### When mobility work actually improves function

Honest answer: when a specific, measured ROM restriction is blocking a specific
task the client cares about (hip flexion blocking a squat depth, ankle
dorsiflexion blocking a lunge, shoulder flexion blocking an overhead press).
General "mobility work" as a health habit has much weaker support than the
volume of content about it implies. That is open question 4.

### Programming variables

| Variable | Prescription |
|---|---|
| Frequency | Most days; short sessions beat weekly marathons |
| Intensity | Point of mild discomfort, not pain; 6-7/10 stretch |
| Volume | 5-10 min/wk per target muscle, accumulated |
| Selection | Only the 2-4 restrictions that block a real task |
| Rest | n/a |
| Tempo | 30-60 s holds; for mobility, 5-10 s active end-range holds |
| Order | Dynamic before training, static after or standalone |

### Common mistakes

- Long static holds immediately before heavy or explosive work
  ([Behm 2016](https://pure.northampton.ac.uk/en/publications/acute-effects-of-muscle-stretching-on-physical-performance-range-/)).
- Stretching a joint that is unstable rather than stiff.
- Treating passive ROM gains as mobility. Range you cannot control is not usable.
- Programming 20 mobility drills. Pick the ones that unblock a task.

---

## Goal 6: Achievements and skill goals

**Evidence quality: Weak-to-Practice.** Almost everything here is convention
built on top of the strength and skill-acquisition literature. Flag it as such.

### The general shape

Every achievement decomposes into: (a) a strength or endurance prerequisite,
(b) a skill component, (c) a ladder of regressions that bridge the gap. Program
the prerequisite with the relevant goal's rules (Goal 2 or Goal 4), and practise
the skill separately, frequently, and fresh.

### Greasing the groove

Pavel Tsatsouline's method: frequent submaximal practice through the day,
typically ~40-60% of max reps, never near failure, treating strength as a skill
([The Naked Warrior, 2003; see summary](https://getfitcraft.com/science/greasing-the-groove) —
**secondary source; I could not reach a primary text. UNVERIFIED**).

The mechanism is consistent with what is known: early strength gains are
neural (recruitment and coordination) rather than hypertrophic, and frequency
distributes volume without adding fatigue
([Grgic 2018](https://pubmed.ncbi.nlm.nih.gov/29470825/)). But GtG itself has
no controlled trial support that I found. Present it as a well-liked method,
not a validated one.

### Progression ladders

| Achievement | Ladder | Typical timeline (**Practice-grade**) |
|---|---|---|
| First pull-up | Scapular pulls -> band-assisted -> eccentric-only (5 s lowers) -> partial ROM -> full | 8-16 wk from 0 |
| First muscle-up | Strict pull-up x8 + straight-bar dip x8 -> high pull to sternum -> transition drills -> kip or strict MU | 6-18 mo after a solid pull-up |
| Handstand | Wall plank -> chest-to-wall hold 60 s -> heel pulls -> freestanding kick-up -> 30 s hold | 6-24 mo, highly variable |
| Pistol squat | Box squat descending height -> assisted (TRX/pole) -> counterweight -> full | 8-20 wk with adequate ankle dorsiflexion |
| 100 push-ups | GtG-style daily submaximal sets, weekly total volume progression | 3-6 mo |
| 5k continuous | Run/walk intervals -> continuous 20 min -> 5k | 8-10 wk from sedentary |
| 10k | 5k base -> long run progression + one quality session | 8-12 wk after a 5k |
| Half marathon | 10k base -> long run to 16-18 km, weekly volume 30-50 km | 12-20 wk after a 10k |
| 2x bodyweight deadlift | Standard strength block programming; the goal is a load target, not a skill | 1-3 yr, heavily bodyweight-dependent |

These timelines are **coaching convention, not measured medians.** I found no
primary source giving population timelines for calisthenic milestones. That is
open question 5.

### Programming variables

| Variable | Prescription |
|---|---|
| Frequency | High. 3-6x/wk for skill; skill is practice, not a workout |
| Intensity | Submaximal on skill work (~40-60% of max effort); heavy on the strength prerequisite |
| Volume | Many short exposures, low fatigue per exposure |
| Selection | The movement itself, plus its nearest regression |
| Rest | Full recovery between skill attempts. Fatigued practice teaches fatigued technique |
| Tempo | Slow eccentrics are the highest-value regression for pulling and pressing goals |
| Order | Skill first in the session, always, while the nervous system is fresh |

### Beginner / intermediate / advanced

- **Beginner:** the prerequisite is usually general strength, not the skill.
  Build the base and the ladder progresses itself.
- **Intermediate:** dedicated skill practice plus targeted assistance work.
- **Advanced:** the achievement is a load or time target; run the strength or
  endurance goal's model and test periodically.

### Common mistakes

- Practising a skill to failure. Skill practice is not conditioning.
- Skipping the strength prerequisite and grinding the regression forever.
- Testing weekly. Test every 4-6 weeks; test days are not training days.
- Chasing an achievement that a bodyweight change would make trivially easier
  and not saying so (in scope: relative strength; out of scope: prescribing the
  diet to achieve it, see Goal 7).

---

## Goal 7: Fat loss and body recomposition

**Evidence quality: Strong for the deficit/lean-mass relationship; moderate for
training's role.** Note the scope boundary hard: most of this goal is not the
trainer's to prescribe.

### Scope boundary, stated first

**A personal trainer is not a dietitian.** Within scope: general healthy-eating
information, protein adequacy in general terms, energy balance as a concept,
referral. Out of scope: individualised meal plans, calorie or macro
prescriptions, supplement protocols, anything for a client with a diagnosed
eating disorder, diabetes, or other clinical condition. The agent must route
those to a registered dietitian or physician. Slice 12 owns the detailed scope
rules; this file flags the boundary at every point it is touched.

### What the evidence says

Murphy & Koehler 2022 meta-analysed resistance training under energy deficit:
lean mass gains were impaired versus training in energy balance, but **strength
gains were comparable**. The meta-regression put the crossover around a
**~500 kcal/day deficit**, beyond which lean mass gain was prevented; the
authors' recommendation is to avoid deficits larger than that when preserving
lean mass matters
([PMID 34623696](https://pubmed.ncbi.nlm.nih.gov/34623696/),
[Wiley](https://onlinelibrary.wiley.com/doi/10.1111/sms.14075)). Note the
authors' own caveat: protein intake was not a covariate in that regression.

Two things follow:

1. **Training does not create the deficit; it protects what is inside it.**
   Resistance training is the muscle-retention tool. Cardio and steps are
   energy-expenditure tools with a much smaller effect than diet.
2. **Strength is the metric to track in a deficit,** because it holds up when
   size does not. That is also the best adherence lever available: the client
   can still PR while losing weight.

### Programming variables

| Variable | Prescription |
|---|---|
| Frequency | 3-4 lifting sessions/wk plus daily step target |
| Intensity | Keep loads heavy. This is the single most important instruction |
| Volume | Maintain, do not increase. Recovery is compromised in a deficit |
| Selection | Compounds. Efficiency matters when energy is short |
| Rest | Normal (2-3 min). Do not turn lifting into conditioning |
| Tempo | Unchanged |
| Order | Lifting before cardio on combined days |

### Progression model

**Hold, do not push.** In a deficit the realistic goal is to keep loads and
sets where they are. Progression comes from steps and cardio minutes, not from
adding lifting volume the client cannot recover from.

### Beginner / intermediate / advanced

- **Beginner:** genuine recomposition is achievable. Untrained people in a
  moderate deficit can gain lean mass and lose fat simultaneously.
- **Intermediate:** expect maintenance of lean mass, not gain.
- **Advanced:** expect small lean-mass loss; minimise it with a smaller deficit
  and unchanged training intensity.

### Common mistakes

- Switching to high-rep "toning" circuits, which drops the exact stimulus that
  protects muscle ([Murphy & Koehler 2022](https://pubmed.ncbi.nlm.nih.gov/34623696/)).
- Adding training volume and cutting food simultaneously.
- Using scale weight as the only metric.
- Giving calorie numbers. Out of scope. Refer.

---

## Goal 8: Power and general athleticism

**Evidence quality: Moderate.**

### The core stimulus is intent, not load

Power work is quality work: few reps, full recovery, maximum movement speed.
The moment bar speed or jump height drops meaningfully, the set is over.

Markovic 2007 meta-analysed plyometric training for vertical jump: statistically
significant and practically relevant improvements, mean effects 4.7% (squat
jump and drop jump), 7.5% (countermovement jump with arms) up to 8.7%
([PMID 17347316](https://pubmed.ncbi.nlm.nih.gov/17347316/)). A 2019
meta-analysis extended this to jumping, sprinting and lower-body strength in
healthy adults ([PMID 31136014](https://pubmed.ncbi.nlm.nih.gov/31136014/)).

### Velocity-based training basics

Pareja-Blanco et al. 2017 compared 20% versus 40% velocity loss thresholds in
the squat over 8 weeks: the 20% group did roughly half the total reps and still
matched or beat the 40% group on the outcomes that matter, with different
structural adaptations
([Scand J Med Sci Sports](https://onlinelibrary.wiley.com/doi/abs/10.1111/sms.12678)).
A later review compared VBT with traditional percentage-based methods for
strength, power and sprint speed
([J Sports Sci 2022](https://www.tandfonline.com/doi/full/10.1080/02640414.2022.2059320)).

For a general client without a velocity device, the usable version is:
**stop the set when the bar visibly slows.** That is the poor-person's velocity
loss threshold and it is the correct instinct.

### Programming variables

| Variable | Prescription |
|---|---|
| Frequency | 2-3 power sessions/wk, always as part of a strength program |
| Intensity | Jumps/throws: bodyweight to light. Olympic derivatives: 60-80% 1RM |
| Volume | Low. 3-6 sets x 2-5 reps; 60-120 total foot contacts for plyos as a starting range (**Practice-grade**) |
| Selection | Jumps, throws, hops, sprints; hang power clean, high pull, push press over full lifts |
| Rest | Full. 2-3 min minimum; power work with short rest is conditioning |
| Tempo | Maximal concentric intent, fast |
| Order | First in the session, after warm-up, before everything |

### Olympic lift derivatives

Prefer derivatives (hang power clean, mid-thigh pull, push press) over full
competition lifts for general clients: most of the power stimulus, a fraction
of the coaching time. **Practice-grade**; I did not find a meta-analysis
directly comparing derivatives against full lifts for general populations
inside the timebox.

### Beginner / intermediate / advanced

- **Beginner:** build a strength base first. Low-intensity jumps and landings
  to teach absorption; volume very low.
- **Intermediate:** true plyometrics, derivatives, sprint work; still after a
  strength block, not instead of one.
- **Advanced:** velocity monitoring, contrast/complex training, seasonal
  planning.

### Common mistakes

- Programming plyometrics for conditioning. High reps, short rest, tired
  landings: no power stimulus and higher injury exposure.
- Power work at the end of the session.
- Skipping the strength base. Force precedes rate of force development.
- Chasing an exercise's difficulty rather than its speed.

---

## Goal 9: Concurrent goals and the interference effect

**Evidence quality: Moderate, and the picture has changed since 2012.**

### What changed

Wilson et al. 2012 meta-analysed 21 studies / 422 effect sizes. Hypertrophy
effect sizes: strength training alone 1.23, endurance alone 0.27, concurrent
0.85. Power: 0.91 / 0.11 / 0.55. Crucially, interference scaled with the
**modality, frequency and duration** of the endurance work: concurrent
**running** hurt hypertrophy and strength significantly, **cycling did not**
([JSCR 2012](https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx)).

Schumann et al. 2022 updated the picture across 43 studies: concurrent training
did **not** significantly reduce maximal strength or hypertrophy versus strength
training alone. It did produce smaller gains in **explosive strength**
([PMC8891239](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8891239/),
[JCU record](https://researchonline.jcu.edu.au/71546/)). Related work on
muscle-fibre-level hypertrophy points the same direction
([PMID 35476184](https://pubmed.ncbi.nlm.nih.gov/35476184/)). Stronger by
Science's read of the newer literature is the same: the interference effect
keeps shrinking ([SBS](https://www.strongerbyscience.com/research-spotlight-interference-effect/)).

**Summary for the agent: interference is real but narrow. It hits power hardest,
size and strength barely, and it scales with endurance volume, running as the
modality, and how close the two sessions sit.**

### Sequencing rules

| Situation | Rule |
|---|---|
| Same session, strength is the priority | Lift first, cardio after |
| Same session, cardio is the priority | Cardio first, lift after |
| Same session, power is the priority | Power first, and consider not doing both |
| Separate sessions same day | 6+ hours apart if possible |
| Separate days | Best option. Hard cardio not the day before a heavy lower-body session |
| Modality choice under a strength goal | Cycling or rowing over running ([Wilson 2012](https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx)) |
| Endurance dose under a strength goal | Keep frequency and duration low; interference scales with both |

### Priority rules when a client wants two goals

1. **Make them rank.** "Which one would you keep if you could only keep one?"
2. **Program the first goal properly.** Full volume, full progression.
3. **Run the second at maintenance.** For muscle, MV is roughly 6 sets/wk
   ([RP](https://rpstrength.com/blogs/articles/training-volume-landmarks-muscle-growth)).
   For cardio, 1-2 sessions/wk holds fitness.
4. **Swap the priority every 8-12 weeks** rather than splitting every week.
   Sequential beats simultaneous when the goals conflict.
5. **Some pairs do not conflict at all.** Health + strength, hypertrophy +
   fat loss, mobility + anything. Only power+endurance and, mildly,
   hypertrophy+high-volume-endurance actually fight.

### Common mistakes

- Over-applying 2012-era interference fear and refusing to let a lifter run
  ([Schumann 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8891239/)).
- Under-applying it for a power athlete, where the effect is real.
- Doing hard cardio the evening before a heavy squat day.
- Letting a client have three priorities.

---

## Weekly templates

Read these as starting shapes to be modified, not prescriptions. All assume an
intermediate client unless stated. FB = full body, U/L = upper/lower,
PPL = push/pull/legs.

### Goal 1: General health

| Sessions/wk | Structure |
|---|---|
| 2 | 2x FB lifting (45 min) + hit step target daily. Cardio comes from walking |
| 3 | 2x FB lifting + 1x 30 min moderate cardio |
| 4 | 2x FB lifting + 2x 30 min cardio (one moderate, one brisk) |
| 5 | 2x FB lifting + 3x 30-40 min cardio + daily walking. Hits 150+ min comfortably |

### Goal 2: Maximal strength

| Sessions/wk | Structure |
|---|---|
| 2 | FB A (squat heavy, bench, row) / FB B (deadlift heavy, press, chin) |
| 3 | Squat focus / Bench focus / Deadlift focus, each with a secondary lift at lighter load |
| 4 | U/L x2: Lower heavy, Upper heavy, Lower volume, Upper volume |
| 5 | 4-day U/L + 1 accessory/weak-point day. Deload every 4-6 wk |

### Goal 3: Hypertrophy

| Sessions/wk | Structure |
|---|---|
| 2 | 2x FB, 2-3 sets per major muscle per session (~8-10 sets/muscle/wk, at MEV) |
| 3 | 3x FB, or U/L/FB. ~10-12 sets/muscle/wk |
| 4 | U/L x2. ~14-18 sets/muscle/wk. The default for most physique clients |
| 5 | PPL + U/L, or 4-day U/L + 1 specialization day. 16-20+ sets on priority muscles |

### Goal 4: Cardiovascular fitness

| Sessions/wk | Structure |
|---|---|
| 2 | 1x long easy (45-60 min) + 1x intervals (4x4 or equivalent) |
| 3 | 2x easy + 1x intervals. The minimum that looks like a real program |
| 4 | 3x easy + 1x intervals (roughly pyramidal) |
| 5 | 4x easy (one long) + 1x intervals; add a second hard session only if recovery allows |

### Goal 5: Mobility and flexibility

| Sessions/wk | Structure |
|---|---|
| 2 | 2x 20 min dedicated sessions. Below the useful dose for multiple targets; pick 2 |
| 3 | 3x 15 min, targets rotated, plus dynamic warm-ups on training days |
| 4 | 4x 10 min daily-habit format + end-range holds after lifting |
| 5-7 | 5-10 min daily, 2-3 targets. Highest-adherence format and the one to default to |

### Goal 6: Achievements

| Sessions/wk | Structure |
|---|---|
| 2 | 2x FB strength with the skill practised first, fresh, every session |
| 3 | 2x strength + 1 dedicated skill session; GtG-style micro-sets on off days |
| 4 | 3x strength (U/L or FB) + 1 skill session; skill primer before every session |
| 5-6 | Daily short skill practice (10-15 min) + 3-4 strength sessions |

### Goal 7: Fat loss

| Sessions/wk | Structure |
|---|---|
| 2 | 2x FB lifting, loads maintained + daily step target (the actual lever) |
| 3 | 3x FB lifting + steps + 1 optional easy cardio session |
| 4 | U/L x2 + steps + 2 easy cardio sessions (after lifting or separate) |
| 5 | 4x lifting + 1 cardio + steps. Do not add lifting volume in the deficit |

### Goal 8: Power and athleticism

| Sessions/wk | Structure |
|---|---|
| 2 | 2x FB: jumps/throws first (low volume), then strength work |
| 3 | 3x FB: power emphasis rotated (vertical / horizontal / upper) |
| 4 | U/L x2, power block leading each session; sprint work on one lower day |
| 5 | 4x strength+power + 1 dedicated speed/agility session |

### Goal 9: Concurrent (strength primary, cardio secondary)

| Sessions/wk | Structure |
|---|---|
| 4 | Mon lift lower, Tue easy cardio, Thu lift upper, Sat lift FB + short cardio |
| 5 | Mon lower, Tue cardio intervals, Wed upper, Fri lower, Sat easy long cardio |
| 6 | 4 lifting days + 2 cardio days, hard cardio never adjacent to heavy lower body |

---

## Goal -> template decision procedure

For the agent, in order:

1. **Ask for one primary goal.** If the client names several, make them rank.
2. **Classify it** against the nine above. If it does not fit, decompose it into
   the physical qualities it needs (see "Goals not on this list") and program those.
3. **Read training age**: 0-9 months, 9 months to ~3 years, or beyond.
4. **Read available sessions per week**, honestly, including the bad weeks.
5. **Pick the template** from the tables above at that session count.
6. **Set the progression rule** from the goal's section: load, sets, minutes, or
   ladder rung.
7. **Set the secondary goals to maintenance dose** and say out loud that they
   are on maintenance.
8. **Set the review date**: 4-6 weeks, or a block boundary.

---

## Conflicts between sources, and how to resolve them

| Conflict | Positions | Resolution |
|---|---|---|
| Interference effect size | Wilson 2012 found meaningful interference; Schumann 2022 found essentially none for strength/size | Prefer the newer and larger analysis. Keep Wilson's *moderating* findings (running worse than cycling; scales with frequency and duration) which Schumann does not contradict. Interference is real for **power** in both |
| Training frequency | Higher frequency helps strength (Grgic 2018 overall) vs no effect when volume-equated (same paper's subgroup) | Frequency is a delivery mechanism for volume. Prescribe frequency to make the weekly volume achievable, not as an independent stimulus |
| Volume dose-response | Schoenfeld 2017 says more is better up to at least 10+ sets; newer meta-regressions probe for a plateau | Use 10-20 sets/muscle/wk as the working band, start low, progress. Do not claim an optimum |
| Training to failure | Bodybuilding tradition says failure is required; Refalo 2023 finds a trivial-to-small edge | 0-3 RIR. The recovery cost of failure buys back more volume than the failure itself delivers |
| Periodization | Williams 2017 favours periodized; the adjusted effect is small; LP vs DUP shows no difference | Have a plan and a progression rule. Do not sell a specific periodization model as superior |
| The 10% rule | Universal coaching advice; Buist 2008 RCT found no injury difference | Use gradual progression as a default, and label the 10% rule as convention, not evidence |
| Stretching before exercise | "Always stretch first" vs Behm 2016's acute performance decrements | Dynamic before, static after. Static holds under ~60 s per muscle group with a full dynamic warm-up are unlikely to matter |
| Stretching for hypertrophy | Enthusiastic online claims vs trivial meta-analytic effects requiring 15+ min/session, 5x/wk | Not a practical hypertrophy tool for general clients. Say the dose out loud and let the client decide |
| Polarized training | 80/20 presented as universal vs derived from athletes training 10-13x/wk | Apply the *principle* (most easy, some hard, avoid living in the middle). Do not apply the *ratio* to a 3-session-a-week client |
| Branded mobility systems | FRC/CARs marketing vs the actual published evidence | Teach the mechanism, which is defensible. Do not endorse the brand |
| Volume landmarks (MEV/MAV/MRV) | Presented as measured values vs a coaching heuristic on top of the volume literature | Use the vocabulary for planning; do not present the specific numbers as research findings |

**General resolution rule for the agent:** when a position stand and a newer
meta-analysis disagree, prefer the meta-analysis for the specific question and
the position stand for the framing. When a coaching convention and a trial
disagree, the convention may still be a fine default, but it must be labelled
as a convention.

---

## Goals not on this list

The user was explicit that the list is not exhaustive. For an unlisted goal
("I want to keep up with my kids", "I want to not be sore at my desk", "I want
to look good at a wedding in June"), decompose it:

1. Which physical qualities does the goal actually need? Strength, size,
   aerobic capacity, ROM, power, skill, body composition.
2. Rank them.
3. Program the top one with its section's rules, hold the rest at maintenance.
4. Define an observable success test the client agrees with, so progress is
   checkable at the 4-6 week review.

Most "novel" goals are one or two of the nine wearing a different name.

---

## Open questions for the user

1. **ACSM published a new resistance training position stand in April 2026**
   ([announcement](https://acsm.org/science-spotlight-acsm-releases-new-position-stand-on-resistance-training/),
   [PMID 41843416](https://pubmed.ncbi.nlm.nih.gov/41843416/)). I could not open
   either full text in the timebox. Everything cited to ACSM 2009 here should be
   re-checked against it. Do you want a follow-up pass that gets the full text?
2. The newest **volume dose-response meta-regression**
   ([PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/)) may change the
   10-20 sets/week band. Worth reading properly before the numbers ship in an
   agent.
3. **Couch-to-5k style ladders** have no controlled evidence I could find for
   the specific interval structure. Fine as a default, but is that acceptable
   for an agent that cites its reasoning?
4. **General mobility work** has much weaker support than the amount of content
   about it suggests. Do you want the agent to program mobility only against a
   named restriction, or offer it as a general habit anyway?
5. **Achievement timelines** in Goal 6 are coaching convention, not measured
   medians. Should the agent give timelines at all, or only give the ladder and
   let progress speak?
6. **Scope boundary on nutrition** is stated here at a high level and owned by
   slice 12. Confirm the split so the two files do not contradict each other.
7. **Units and audience**: this file mixes kg, km and minutes. Which does the
   product default to?

---

## Source list

Position stands and guidelines:
- [ACSM 2009, Progression Models in Resistance Training for Healthy Adults, PMID 19204579](https://pubmed.ncbi.nlm.nih.gov/19204579/)
- [ACSM 2011, Quantity and Quality of Exercise, PMID 21694556](https://pubmed.ncbi.nlm.nih.gov/21694556/)
- [ACSM 2026, Resistance Training Prescription (overview of reviews), PMID 41843416](https://pubmed.ncbi.nlm.nih.gov/41843416/) — UNVERIFIED content
- [Physical Activity Guidelines for Americans 2nd ed, PMID 30418471](https://pubmed.ncbi.nlm.nih.gov/30418471/) / [full PDF](https://www.niddk.nih.gov/-/media/Files/Diet-Nutrition/Physical_Activity_Guidelines_2nd_edition.pdf)
- [WHO 2020 guidelines, PMID 33239350](https://pubmed.ncbi.nlm.nih.gov/33239350/) / [recommendations, NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK566046/)

Resistance training:
- [Schoenfeld, volume dose-response 2017, PMID 27433992](https://pubmed.ncbi.nlm.nih.gov/27433992/)
- [Volume/frequency dose-response meta-regressions, PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/)
- [Schoenfeld, low vs high load 2017, PMID 28834797](https://pubmed.ncbi.nlm.nih.gov/28834797/)
- [Schoenfeld, rest intervals 2016, PMID 26605807](https://pubmed.ncbi.nlm.nih.gov/26605807/)
- [Grgic, frequency and strength 2018, PMID 29470825](https://pubmed.ncbi.nlm.nih.gov/29470825/)
- [Schoenfeld & Grgic, frequency and hypertrophy review](https://www.sciencedirect.com/science/article/abs/pii/S1440244018308624)
- [Refalo, proximity to failure 2023, PMID 36334240](https://pubmed.ncbi.nlm.nih.gov/36334240/)
- [Refalo, proximity-to-failure meta-regressions 2024, PMID 38970765](https://pubmed.ncbi.nlm.nih.gov/38970765/)
- [Williams, periodized vs non-periodized 2017](https://link.springer.com/article/10.1007/s40279-017-0734-y)
- [LP vs DUP for hypertrophy, PMID 28848690](https://pubmed.ncbi.nlm.nih.gov/28848690/)
- [Long vs short muscle length partials, 2025](https://link.springer.com/article/10.1007/s11332-025-01586-5)
- [Lengthened partials vs full ROM, PMID 39959841](https://pubmed.ncbi.nlm.nih.gov/39959841/)
- [Regional hypertrophy at long and short lengths, PMC10407320](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10407320/)
- [RP volume landmarks (coaching model)](https://rpstrength.com/blogs/articles/training-volume-landmarks-muscle-growth)

Endurance:
- [Seiler & Kjerland 2006, PMID 16430681](https://pubmed.ncbi.nlm.nih.gov/16430681/)
- [Seiler 2010, best practice for intensity distribution, PMID 20861519](https://pubmed.ncbi.nlm.nih.gov/20861519/)
- [Polarized vs other distributions, meta-analysis, PMC11329428](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11329428/)
- [Polarized TID and VO2max, systematic review, PMC11679080](https://pmc.ncbi.nlm.nih.gov/articles/PMC11679080/)
- [Helgerud 2007, 4x4 intervals (PDF)](https://rcc.hslu.ch/fileadmin/user_upload/downloads/sport/Aerobic_High-Intensity_Intervals_Improve_J.Helgerud_2007.pdf)
- [Tabata 1996](https://waseda.elsevierpure.com/en/publications/effects-of-moderate-intensity-endurance-and-high-intensity-interm/)
- [Buchheit & Laursen, HIIT Part I, PMID 23539308](https://pubmed.ncbi.nlm.nih.gov/23539308/) / [Part II](https://link.springer.com/article/10.1007/s40279-013-0066-5)
- [Aerobic intervals vs sprint intervals, PMC10099854](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10099854/)
- [Buist 2008, GRONORUN graded program RCT, PMID 17940147](https://pubmed.ncbi.nlm.nih.gov/17940147/)
- [Nielsen 2014, excessive weekly distance progression](https://www.jospt.org/doi/10.2519/jospt.2014.5164)
- [Training errors and running injuries, systematic review, PMC3290924](https://pmc.ncbi.nlm.nih.gov/articles/PMC3290924/)

Stretching and mobility:
- [Thomas 2018, stretching typology and duration (mirrored PDF)](https://paulogentil.com/pdf/The%20Relation%20Between%20Stretching%20Typology%20and%20Stretching%20Duration%20-%20The%20Effects%20on%20Range%20of%20Motion.pdf) — UNVERIFIED against publisher
- [Warneke 2024, chronic static stretching, strength and hypertrophy, PMID 38637473](https://pubmed.ncbi.nlm.nih.gov/38637473/)
- [Chronic static stretching and hypertrophy, multilevel meta-analysis, PMC11438763](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11438763/)
- [Optimising static stretching dose, PMID 39614059](https://pubmed.ncbi.nlm.nih.gov/39614059/)
- [Mechanisms of ROM improvement, PMID 40180774](https://pubmed.ncbi.nlm.nih.gov/40180774/)
- [Chronic effects of stretching on ROM, moderators](https://www.sciencedirect.com/science/article/pii/S2095254623000571)
- [Behm 2016, acute effects of stretching](https://pure.northampton.ac.uk/en/publications/acute-effects-of-muscle-stretching-on-physical-performance-range-/)
- [Behm & Chaouachi 2011 review, PMID 21373870](https://pubmed.ncbi.nlm.nih.gov/21373870/)
- [FRC for chronic low back pain, NCT03456050](https://clinicaltrials.gov/study/NCT03456050)

Power:
- [Markovic 2007, plyometrics and vertical jump, PMID 17347316](https://pubmed.ncbi.nlm.nih.gov/17347316/)
- [Plyometric training in healthy adults, PMID 31136014](https://pubmed.ncbi.nlm.nih.gov/31136014/)
- [Pareja-Blanco 2017, velocity loss thresholds](https://onlinelibrary.wiley.com/doi/abs/10.1111/sms.12678)
- [VBT vs percentage-based training review 2022](https://www.tandfonline.com/doi/full/10.1080/02640414.2022.2059320)

Concurrent and body composition:
- [Wilson 2012, concurrent training meta-analysis](https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx)
- [Schumann 2022, updated concurrent training meta-analysis, PMC8891239](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8891239/)
- [Concurrent training and muscle fibre hypertrophy, PMID 35476184](https://pubmed.ncbi.nlm.nih.gov/35476184/)
- [Arem 2015, activity and mortality dose-response, PMID 25844730](https://pubmed.ncbi.nlm.nih.gov/25844730/)
- [Murphy & Koehler 2022, energy deficit and lean mass, PMID 34623696](https://pubmed.ncbi.nlm.nih.gov/34623696/)

Secondary sources (used only where flagged):
- [Stronger by Science, interference effect research spotlight](https://www.strongerbyscience.com/research-spotlight-interference-effect/)
- [Motive Training, FRC evidence review](https://www.movewithpurpose.com/is-frc-evidence-based)
- [Greasing the groove summary](https://getfitcraft.com/science/greasing-the-groove) — UNVERIFIED, no primary source reached
