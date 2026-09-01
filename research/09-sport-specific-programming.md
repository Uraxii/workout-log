# Sport-specific strength and conditioning: how programming changes per sport

Research slice 09. Written 2026-08-31.

Sibling slices: 07 baselining, 08 goal-specific programming (general population),
10 medical and special populations, 11 transgender athletes, 12 trainer practice.
This file covers only the athlete case. It answers the user's question:
"sport-specific things that change based on the sport that they play."

Scope note: everything here is trainer scope. Nutrition, weight cutting protocols,
and injury diagnosis are flagged out of scope where they come up.

---

## TL;DR

### The needs analysis, in 8 steps

An agent can run all eight over chat. No lab needed.

| # | Step | What the agent asks or does |
|---|------|-----------------------------|
| 1 | Name the sport and the level | Sport, position or event, competitive level, and hours per week of sport practice. |
| 2 | Movement analysis | Which body movements, which planes, which joints, how much is unilateral, how much is contact. |
| 3 | Physiological analysis | Which qualities the sport pays for: max strength, power, speed, repeat-sprint, aerobic base, mobility. |
| 4 | Energy system analysis | Typical work bout length, rest between bouts, total event duration. |
| 5 | Injury analysis | Which injuries are common in this sport, plus the athlete's own injury history. |
| 6 | Athlete profile | Training age, gym access, schedule, recovery constraints, season phase. |
| 7 | Test | Pick two or three field tests that map to steps 3 and 5. Record numbers. |
| 8 | Write the plan | Season phase drives volume. Gaps found in step 7 drive exercise selection. |

Steps 2, 3 and 5 are the NSCA's three-part needs analysis: movement analysis,
physiological analysis, injury analysis.
[NSCA needs analysis for injury prevention](https://www.nsca.com/education/articles/kinetic-select/needs-analysis-for-injury-prevention/),
[NSCA, Essentials of Strength Training and Conditioning, 5th ed.](https://www.nsca.com/certification/cscs/essentials-of-strength-training-and-conditioning-5th-edition/)

### The in-season vs off-season rule of thumb

**Off-season you build. In-season you defend.**

- Off-season: 3 to 4 gym sessions a week, high volume, gym is the priority.
- Pre-season: 2 to 3 sessions, volume falls, intensity holds, sport practice rises.
- In-season: 1 to 2 sessions, low volume, keep the load heavy, never chase soreness.
- Post-season: 2 to 4 weeks of unstructured activity, then start again.

The in-season number is not a guess. One heavy session a week held strength,
sprint and jump gains across a 12-week competitive season in professional
soccer players. One session every second week did not: leg strength and 40 m
sprint both fell.
[Rønnestad et al., in-season strength maintenance frequency](https://www.researchgate.net/publication/51601921_Effects_of_In-Season_Strength_Maintenance_Training_Frequency_in_Professional_Soccer_Players)

---

## 1. The needs analysis as an agent-runnable script

This is the part the agent should be able to execute as a chat script for any
sport, including one it has no profile for. Ask, do not assume.

### Step 1. Sport, position, level

Ask:
- "What sport, and what position or event?"
- "How many hours a week do you actually train the sport, not the gym?"
- "Recreational, club, college, or professional?"
- "When is your next competition, and when does the season start and end?"

Position matters as much as sport. A soccer goalkeeper and a soccer winger share
a sport and almost nothing else. Same for an offensive lineman and a wide
receiver.

### Step 2. Movement analysis

The NSCA defines movement analysis as identifying the movement patterns and the
muscles involved.
[NSCA](https://www.nsga.com/needs-analysis-for-sports-training/)

The agent should classify the sport along five axes:

| Axis | Question | Effect on the program |
|------|----------|-----------------------|
| Plane | Sagittal, frontal, transverse, or all three | Rotation-heavy sports need anti-rotation and rotational power work |
| Limb | Bilateral or unilateral | Unilateral sports get split squats, single-leg RDLs, step-ups |
| Contact | None, incidental, or collision | Collision sports need neck work and higher lean mass |
| Overhead | How much and how fast | Overhead sports need shoulder capacity work, not shoulder mobility alone |
| Ground | Feet, bike, water, board, mat | Non-weightbearing sports (cycling, swimming) get bone loading from the gym |

### Step 3. Physiological analysis

Rank the qualities the sport pays for. The NSCA frames this as determining
strength, power, hypertrophy and muscular endurance priorities.
[NSCA](https://www.nsca.com/education/articles/kinetic-select/needs-analysis-for-injury-prevention/)

Force the ranking. Every sport "needs everything". A plan that trains everything
trains nothing. Ask the athlete to rank these six from 1 to 6:

max strength, explosive power, top speed, repeat-effort capacity, aerobic
endurance, mobility and positional tolerance.

The top two get the main lifts and the freshest part of each session.

### Step 4. Energy system analysis

Ask three numbers:
- How long is one hard effort?
- How long is the rest between efforts?
- How long is the whole event or match?

Rough mapping, from the classic bioenergetic model taught in the NSCA text:

| Effort length | Dominant system | Conditioning that matches |
|---|---|---|
| Under 10 s | Phosphagen | Short sprints, full recovery, 1:10 to 1:20 work:rest |
| 10 s to 2 min | Fast glycolysis | Intervals, 1:3 to 1:5 work:rest |
| 2 to 8 min | Glycolysis plus oxidative | Threshold and VO2max intervals |
| Over 8 min | Oxidative | Steady state and long intervals |

UNVERIFIED: the exact boundary numbers vary by textbook edition. Treat them as
planning aids, not physiology.

### Step 5. Injury analysis

Two parts.

Sport-level: which injuries dominate this sport. The per-sport profiles below
carry that.

Athlete-level: ask directly.
- "Any injury in the last two years that cost you training time?"
- "Anything that flares up when you push volume?"
- "Any surgery ever?"

Prior injury is the single most consistent risk factor across the injury
literature, and a previously injured athlete goes into the plan as a different
athlete.
[van Mechelen sequence of prevention model, four steps: establish the problem, establish causes, introduce a measure, evaluate](https://pubmed.ncbi.nlm.nih.gov/1509229/)

### Step 6. Athlete profile

- Training age in the gym, separate from sport age.
- Equipment: full gym, home rack, bands only, none.
- Days available and length of each session.
- Sleep and life load.
- Current season phase.

### Step 7. Testing

Pick two or three, not ten. Map them to the ranked qualities from step 3 and
to the injury hotspots from step 5.

| Quality | Cheap field test |
|---|---|
| Lower body max strength | 3 to 5 rep max back squat or trap bar deadlift |
| Lower body power | Countermovement jump height, broad jump distance |
| Reactive strength | Drop jump contact time, or 10 second pogo hops |
| Speed | 10 m and 30 m sprint from a timing app or gate |
| Repeat effort | 6 x 30 m sprint with 25 s rest, measure decrement |
| Aerobic | Yo-Yo IR1, 1.5 mile time trial, or 12 minute Cooper |
| Upper body | Pull-up max reps, bench 5RM |
| Asymmetry | Single-leg hop distance, left vs right, flag over 10% difference |

Strength testing is worth doing even in endurance sports. Greater maximal
strength tracks with better jumping, sprinting and change of direction, and with
lower injury risk.
[Suchomel, Nimphius and Stone 2016, The Importance of Muscular Strength in Athletic Performance](https://link.springer.com/article/10.1007/s40279-016-0486-0)

### Step 8. Write the plan

Order of operations:
1. Season phase sets total gym volume and session count.
2. Injury analysis sets the non-negotiable prevention block. It goes in every
   week of every phase.
3. The top two ranked qualities set the main lifts.
4. Test gaps set the accessories.
5. Sport practice hours set the conditioning. If the sport already delivers the
   energy system, the gym does not repeat it.

That last point is the one agents get wrong. A soccer player who plays and
trains five days a week does not need the trainer to add running.

---

## 2. Periodization for athletes

### The three time scales

| Term | Length | What it holds |
|---|---|---|
| Macrocycle | A full year, or a full season plus off-season | The whole competitive calendar |
| Mesocycle | 3 to 6 weeks | One block with one focus |
| Microcycle | 1 week, usually | The training week, arranged around games |

This nested structure comes from Matveyev by way of Bompa, whose *Periodization:
Theory and Methodology of Training* is the standard reference.
[Bompa and Buzzichelli, Periodization, Human Kinetics](https://us.humankinetics.com/products/periodization-7th-edition)

### The four season phases

| Phase | Gym sessions/week | Volume | Intensity | Main goal |
|---|---|---|---|---|
| Off-season | 3 to 4 | High | Moderate to high | Build. Hypertrophy then max strength. Fix asymmetries. |
| Pre-season | 2 to 3 | Falling | High | Convert strength to power. Ramp sport conditioning. |
| In-season | 1 to 2 | Low | High, low reps | Maintain. Manage fatigue. Never interfere with games. |
| Post-season | 0 to 2 | Very low | Optional | Active rest, 2 to 4 weeks, then restart. |

The classical off-season sequence is hypertrophy, then max strength, then power,
each block feeding the next. The rationale is that strength built first is what
later power work converts.
[Suchomel et al. 2016](https://link.springer.com/article/10.1007/s40279-016-0486-0)

### In-season maintenance: the actual numbers

This is the highest-value section for an AI trainer, because athletes most often
ask "can I stop lifting during the season". The answer is no, but the dose is
small.

**One session a week works for 12 weeks.** Professional soccer players who did
one strength maintenance session a week through the first 12 weeks of the season
held the strength, sprint and jump gains from a preceding 10-week preparation
block. Players doing one session every second week lost leg strength and 40 m
sprint speed.
[Rønnestad et al.](https://www.researchgate.net/publication/51601921_Effects_of_In-Season_Strength_Maintenance_Training_Frequency_in_Professional_Soccer_Players)

**Autoregulated single sessions also work.** A 2023 study of professional male
footballers found one autoregulated weekly strength session maintained physical
qualities and external match load across the season.
[Journal of Sports Sciences, 2023](https://www.tandfonline.com/doi/full/10.1080/02640414.2023.2227536)

**Volume can drop hard if intensity holds.** Bickel et al. trained adults 3 days
a week for 16 weeks, then randomised them to detraining or reduced-dose
maintenance for 32 weeks. Strength gained in phase 1 was largely retained, and a
dose response was visible, with the one-third dose maintaining the myofibre-type
shift better than lower doses. Older adults needed a higher weekly dose than
young adults to hold hypertrophy.
[Bickel, Cross and Bamman 2011, Med Sci Sports Exerc](https://pubmed.ncbi.nlm.nih.gov/21131862/)

**The general rule from the minimal-dose review.** Spiering et al. reviewed the
minimal dose needed to preserve endurance and strength over time, written for
deployed military personnel who cannot train normally.
[Spiering, Mujika, Sharp and Foulis 2021, J Strength Cond Res](https://journals.lww.com/nsca-jscr/fulltext/2021/05000/maintaining_physical_performance__the_minimal_dose.35.aspx)

UNVERIFIED: I could not open the Spiering full text (paywalled, HTTP 402). The
widely repeated summary is that intensity must be preserved while frequency and
volume can be cut sharply. Verify the exact frequency and volume figures against
the paper before an agent quotes them as numbers.

**Practical in-season prescription an agent can give:**

- 1 to 2 sessions a week.
- 2 to 4 exercises per session, no more.
- 3 to 6 reps at 80 to 90% 1RM, 2 to 3 sets.
- Stop 2 to 3 reps short of failure on everything.
- Total session under 40 minutes.
- Never within 48 hours before a competition.
- Keep the prevention block even when everything else gets cut.

### Competition week

Standard structure for a Saturday game, counting back:

| Day | Content |
|---|---|
| Sunday (day +1) | Recovery. Light movement or nothing. |
| Monday | Off, or low-intensity aerobic. |
| Tuesday | Hardest gym session of the week. Heaviest sport session. |
| Wednesday | Sport practice, moderate. |
| Thursday | Optional short power session. Low volume, high speed, no fatigue. |
| Friday | Activation only. Prevention block. Nothing that causes soreness. |
| Saturday | Compete. |

For two games a week, cut to one short power-focused gym session between them,
placed as far from both games as possible.

### Tapering

For a peak event, the evidence is unusually specific.

The optimal taper is **2 weeks long**, with **training volume reduced
exponentially by 41 to 60%**, and **intensity and frequency held constant**.
Bosquet et al. pooled 27 studies and found this combination gave the largest
performance gain.
[Bosquet et al. 2007, Med Sci Sports Exerc, Effects of tapering on performance: a meta-analysis](https://pubmed.ncbi.nlm.nih.gov/17762369/)

A 2023 meta-analysis in endurance athletes broadly reproduced this.
[Effects of tapering on performance in endurance athletes, PLOS One 2023](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0282838)

The single most common taper mistake is cutting intensity. Do not. Cut volume,
keep the fast and heavy work in.

### Concurrent training interference

Athletes lift and do endurance work in the same week. This costs something.

Wilson et al. pooled 21 studies and 422 effect sizes. Strength training alone
beat concurrent training for strength, hypertrophy and power. The size of the
interference depended on the endurance modality, frequency and duration.
Critically, **running produced significant decrements in strength and hypertrophy
while cycling did not**.
[Wilson et al. 2012, J Strength Cond Res, Concurrent Training: A Meta-Analysis](https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx)

What that means per sport:

- Cyclists and rowers can lift heavy with less conflict than runners can.
- Runners lifting for performance should keep gym volume low and lifts heavy
  and few. Hypertrophy work fights the sport.
- Team sport athletes get most of their interference from match running, not
  from anything the trainer adds.

Sequencing within a session matters too. A meta-analysis of intra-session
exercise order found the order changes the interference.
[Eddens et al. 2018, The Role of Intra-Session Exercise Sequence in the Interference Effect](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5752732/)

Practical sequencing rules for the agent:
- Whatever the athlete cares about most goes first, when fresh.
- Separate hard lifting and hard endurance by at least 6 hours if possible.
- Do not put a hard interval session the day before the heaviest lift day.

---

## 3. Transfer of training

Four principles the agent should reason with, not recite.

### Specificity has limits

Specificity says adaptation matches the imposed demand. Taken literally it leads
to nonsense like swinging a weighted bat or squatting on a Bosu. Those change
the motor pattern of the skill without adding force capacity.

The defensible version: the **gym trains physical capacity, the sport trains
skill**. Do not try to make the gym look like the sport.

### Dynamic correspondence

Verkhoshansky's framework asks whether a gym exercise matches the sport action on
amplitude and direction of movement, the region where force peaks, the rate and
time of force production, the dynamics of the effort, and the regime of muscular
work. UNVERIFIED: I did not fetch a primary source for the six criteria within
this timebox. Verify against Verkhoshansky and Siff, *Supertraining*, before
quoting the list.

Useful as a check, not a rule. A trap bar jump squat corresponds well to
sprinting acceleration. A leg extension does not.

### Generic strength still transfers

This is the point that saves an agent from over-engineering. Greater maximal
strength is associated with better jumping, sprinting and change of direction,
with a greater potentiation response, and with lower injury risk, across sports.
[Suchomel, Nimphius and Stone 2016](https://link.springer.com/article/10.1007/s40279-016-0486-0)

Practical read: for anyone who is not already strong, a squat, a hinge, a press,
a pull and a carry will do more for their sport than anything clever. Sport
specificity is a refinement layer on top of general strength, not a replacement
for it.

### When sport practice beats gym work

Sometimes the sport is the best exercise for the sport.

Hamstring injury is the clearest case. Sprinting activates the long head of
biceps femoris more than commonly used strengthening exercises including the
Nordic curl, and both underexposure and overexposure to high-speed running raise
injury risk. Regular sprint exposure is itself part of prevention.
[Comparative EMG activity of hamstrings during sprinting versus strengthening exercises](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11378697/),
[If You Want to Prevent Hamstring Injuries in Soccer, Run Fast](https://pmc.ncbi.nlm.nih.gov/articles/PMC11126098/)

Rule for the agent: if the sport already produces the stimulus at high quality,
the gym should not duplicate it. It should cover what the sport misses.

---

## 4. Load management for sport plus gym

### Session RPE

The cheapest useful load metric, and the one an AI trainer can actually collect
over chat.

```
session load (AU) = session RPE (0-10 scale) x session duration (minutes)
weekly load = sum of session loads over 7 days
monotony = weekly mean daily load / SD of daily load
strain = weekly load x monotony
```

Foster's method combines intensity and duration into one number. Monotony
measures day-to-day sameness, and monotonous training combined with high load
has been linked to overtraining onset. Strain is weekly load times monotony.
[Haddad et al. 2017, Session-RPE Method for Training Load Monitoring, Front Neurosci](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5673663/),
[Foster et al. 2001, A New Approach to Monitoring Exercise Training](https://paulogentil.com/pdf/A%20New%20Approach%20to%20Monitoring%20Exercise%20Training.pdf)

Collect RPE **about 30 minutes after the session**, not during. Ask a single
question: "How hard was that session overall, 0 to 10?"

### Acute:chronic workload ratio

```
ACWR = acute load (last 7 days) / chronic load (rolling 28-day average)
```

Gabbett's 2016 paper argued that high chronic workloads built gradually can be
protective, and proposed keeping the ratio roughly between **0.8 and 1.3**, with
a "danger zone" above about 1.5.
[Gabbett 2016, BJSM, The training-injury prevention paradox](https://pubmed.ncbi.nlm.nih.gov/26758673/),
[full text PDF](https://efsma.org/images/pdf/publications/Br-J-Sports-Med-2016-Gabbett-273-80.pdf)

### The ACWR critique, which matters

Do not let an agent present ACWR as an injury predictor. It has been seriously
challenged.

Impellizzeri and colleagues laid out conceptual issues and statistical pitfalls,
concluding there is no evidence supporting ACWR use in load-management systems
or for injury-risk recommendations, and that the ratio's statistical properties
make it an inaccurate metric that is hard to interpret.
[Impellizzeri, Tenan et al. 2020, Acute:Chronic Workload Ratio: Conceptual Issues and Fundamental Pitfalls](https://www.semanticscholar.org/paper/Acute:Chronic-Workload-Ratio:-Conceptual-Issues-and-Impellizzeri-Tenan/ede5743a426fd6429d28f8505500a3f771dbcf8b)

They also requested retraction or formal correction of a widely republished BJSM
figure that was labelled "illustrative only" and then reused at least seven
times as if it were data.
[Global Performance Insights summary of the retraction request](https://www.globalperformanceinsights.com/post/has-the-acute-chronic-workload-ratio-been-debunked)

**How an agent should use it anyway.** ACWR is a decent *communication device*
for "you ramped too fast", and a bad *prediction device*. Use it as a soft flag
that opens a conversation, never as a hard gate, and never say it predicts
injury.

### Weekly load caps an agent can apply

Defensible, simple, and honest about their basis:

- Raise weekly running volume or weekly total load by no more than about 10% a
  week during a build. UNVERIFIED as a hard rule. The 10% rule is widely taught
  and weakly evidenced. Treat it as a default, not a law.
- Do not raise sport load and gym load in the same week. Alternate.
- After a week off, come back at roughly the last normal week's load, not the
  peak week's.
- High-speed running exposure should be regular, not spiky. Both too little and
  too much raise hamstring injury risk.
  [PMC11126098](https://pmc.ncbi.nlm.nih.gov/articles/PMC11126098/)

### Monitoring for overtraining

An agent's weekly check-in should collect four things and act on the pattern,
not on any single answer:

| Marker | Question | Red flag |
|---|---|---|
| Sleep | Hours and quality, 1 to 5 | Two bad weeks running |
| Soreness | Persistent, 1 to 5 | Rising while load is flat |
| Mood and motivation | 1 to 5 | Sustained drop with no life explanation |
| Resting HR or HRV, if they have a wearable | Trend | Sustained shift from baseline |

Plus performance: if a known load feels harder for two sessions in a row, cut
volume before waiting for more data.

---

## 5. Injury prevention programs worth prescribing

Strength training is the single best-evidenced prevention modality. Lauersen et
al. found strength training programmes reduced sports injuries by roughly two
thirds, a significantly better result than multi-faceted programmes, and the
effect was dose dependent.
[Lauersen, Andersen and Andersen 2018, BJSM, Strength training as superior, dose-dependent and safe prevention](https://www.researchgate.net/publication/327150440_Strength_training_as_superior_dose-dependent_and_safe_prevention_of_acute_and_overuse_sports_injuries_A_systematic_review_qualitative_analysis_and_meta-analysis)

The earlier 2014 meta-analysis pooled 25 studies, 26,610 people and 3,464
injuries, and found strength training and proprioceptive training effective while
stretching alone was not.
[Lauersen et al. 2014, BJSM](https://www.ncbi.nlm.nih.gov/books/NBK169555/)

| Program | Target sport | Target injury | Evidence | Source |
|---|---|---|---|---|
| FIFA 11+ | Soccer, field sports | All lower limb | 32% reduction in injury incidence in 1,892 female players aged 13-17 over 8 months. Later reviews report 30 to 50% across populations. | [Soligard et al. 2008 BMJ, via FIFA 11+ narrative review](https://pubmed.ncbi.nlm.nih.gov/25878073/), [systematic review 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12856364/) |
| Nordic hamstring curl | Soccer, sprinting, all field sports | Hamstring strain | Programmes including the NHE roughly halve hamstring injury rate. Pooled RR 0.49 (95% CI 0.32-0.74) across 8,459 athletes, 525 injuries. | [van Dyk et al. 2019 BJSM](https://www.researchgate.net/publication/331367089_Including_the_Nordic_hamstring_exercise_in_injury_prevention_programmes_halves_the_rate_of_hamstring_injuries_A_systematic_review_and_meta-analysis_of_8459_athletes) |
| Nordic hamstring curl, caveat | | | A 2021 methodological reappraisal argued the preventive effect is inconclusive once methods are corrected. | [Why methods matter in a meta-analysis, J Clin Epidemiol 2021](https://www.sciencedirect.com/science/article/abs/pii/S0895435621002870) |
| Copenhagen adduction / Adductor Strengthening Programme | Soccer, ice hockey | Groin | ~41% reduction in self-reported groin problems. 35 teams, 652 players. 3x/week pre-season, 1x/week in-season. | [Harøy et al. 2019 BJSM](https://pubmed.ncbi.nlm.nih.gov/29891614/) |
| PEP program | Soccer, basketball, female athletes | ACL | 20 minutes, 2 to 3 sessions/week. Significant ACL risk reduction. | [Systematic review of ACL prevention in female athletes](https://pubmed.ncbi.nlm.nih.gov/23016067/) |
| Sportsmetrics | Jumping sports, female athletes | ACL | Significant ACL risk reduction, and improved athletic performance tests. | [Same review](https://pubmed.ncbi.nlm.nih.gov/23016067/) |
| Neuromuscular training, general | Female team sports | ACL | Pooled ~50% reduction in ACL injury risk. Compliance at or above 75% is the strongest moderator. | [Meta-analysis, female team athletes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12581765/) |
| Adductor strength ratio screen and intervention | Ice hockey | Groin | NHL players who later strained a groin had pre-season adduction at 78% of abduction strength vs 95% in uninjured. Intervening on the at-risk group cut injuries. | [Tyler et al., summarised](https://mikereinold.com/groin-injuries-in-hockey-players/) |
| Scapular and rotator cuff dryland | Swimming | Shoulder | Dry-land rotator strength programmes reduced shoulder injury in competitive swimmers. | [Dry-land shoulder rotators strength training in competitive swimmers](https://pmc.ncbi.nlm.nih.gov/articles/PMC7052717/) |
| Eccentric rotator cuff plus core | Tennis | Shoulder overuse | Kinetic-chain conditioning decreased overuse injury by 26%. Four-week ramp-up strategies cut injury incidence by up to 21%. | [Systematic review, high-performance tennis players 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12568103/) |
| Neuromuscular and core program on and off snow | Alpine skiing | ACL | 12 ACL injuries (3.9%) over 2 prevention years vs 35 (8.1%) in the control period. | [Prevention of ACL Injuries in Competitive Adolescent Alpine Skiers, Front Sports Act Living 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7739649/) |
| Heavy slow / eccentric / isometric patellar loading | Volleyball, basketball | Patellar tendinopathy | Eccentric, heavy slow and isometric loading show in-season benefit. Rest alone does not fix it. | [Patellar tendinopathy overview](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10541843/) |
| Neck strength training | Rugby, American football | Neck and head | Neck strength is a modifiable risk factor. Flexion-to-extension and left-right imbalances are potential risk factors. | [Reliability of repeated isometric neck strength in rugby union](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9031103/) |

Compliance is the whole game. The ACL literature identifies compliance at or
above 75% as the most effective factor.
[PMC12581765](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12581765/)
An agent should treat the prevention block as the last thing cut, and should
track adherence to it separately from adherence to the main program.

---

## 6. Sport profiles

Format for each: qualities, energy systems, injury hotspots, prevention, primary
lifts, accessory emphasis, conditioning, what to avoid, sample in-season week,
sample off-season week.

Sample weeks show gym sessions only. Sport practice is assumed on top.

---

### 6.1 Soccer / association football

- **Qualities.** Repeat-sprint ability, acceleration, change of direction,
  aerobic base, eccentric hamstring strength.
- **Energy.** Intermittent. Short maximal efforts inside a 90 minute aerobic
  frame.
- **Injury hotspots.** Hamstring, groin, ankle, ACL. Hamstring strain is around
  10% of all injuries in field-based sports.
  [Hamstring strain injuries review, Strength Cond J 2020](https://journals.lww.com/nsca-scj/fulltext/2020/06000/hamstring_strain_injuries__incidence,_mechanisms,.5.aspx)
- **Prevention.** FIFA 11+ as the warm-up. Nordic curls year round. Copenhagen
  adduction 3x/week pre-season, 1x/week in-season. Regular high-speed running
  exposure.
  [FIFA 11+ review](https://pubmed.ncbi.nlm.nih.gov/25878073/),
  [Harøy 2019](https://pubmed.ncbi.nlm.nih.gov/29891614/)
- **Primary lifts.** Back or front squat, trap bar deadlift, hip thrust, single
  leg RDL, split squat.
- **Accessory.** Calf and ankle, adductors, anti-rotation core.
- **Conditioning.** The sport provides it. Add only if match minutes are low.
- **Avoid.** Long slow running on top of training. High-volume leg hypertrophy
  in-season. Any hard gym work within 48 hours of a match.
- **In-season week.** 1 heavy session (squat 3x4 @85%, Nordic 3x4, hip thrust
  3x5) plus 1 short power session (jumps, med ball, 10 min) on a non-adjacent
  day. Prevention warm-up before every session and every practice.
- **Off-season week.** 3 to 4 sessions. Two lower (squat and hinge focus), one
  upper, one power and sprint day. Sprint exposure at 95%+ once a week from
  week 2.

### 6.2 Basketball

- **Qualities.** Vertical jump, repeat jump capacity, deceleration, lateral
  change of direction, landing mechanics.
- **Energy.** Intermittent, glycolytic and phosphagen dominant, long game frame.
- **Injury hotspots.** Ankle sprain, patellar tendinopathy, ACL. Patellar
  tendinopathy prevalence around 32% in elite basketball players, 20.8% pooled.
  [Patellar tendinopathy overview](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10541843/)
- **Prevention.** Neuromuscular ACL programme (Sportsmetrics or PEP) with
  landing mechanics. Isometric and heavy slow patellar loading in-season.
  Ankle proprioception and balance work.
  [ACL prevention review](https://pubmed.ncbi.nlm.nih.gov/23016067/)
- **Primary lifts.** Trap bar deadlift, front squat, split squat, hip thrust.
- **Accessory.** Calf raises heavy and high volume, tibialis, isometric wall
  sits and Spanish squats for tendon, adductors.
- **Conditioning.** The sport provides it. In-season conditioning is a mistake
  in a 3-games-a-week schedule.
- **Avoid.** Adding plyometrics in-season on top of game jumping. Jump volume is
  already the limiting factor.
- **In-season week.** 1 to 2 sessions, 30 minutes. Trap bar 3x4, split squat
  2x6/side, Copenhagen or adductor 2 sets, isometric wall sit 4x45s for the
  tendon, calf 3x10.
- **Off-season week.** 3 to 4. Two lower (one bilateral heavy, one unilateral),
  one upper, one plyometric progression session. Build jump capacity in a block
  before the season, not during.

### 6.3 Distance running

- **Qualities.** Running economy, aerobic capacity, tendon stiffness, hip and
  calf strength endurance.
- **Energy.** Oxidative dominant.
- **Injury hotspots.** Achilles, patellofemoral pain, tibial stress injury,
  plantar fascia, hip and glute overuse. Almost all overuse, almost all
  load-progression related.
- **Prevention.** Strength training, plus load management. Exercise-based
  prevention in endurance runners has been reviewed specifically.
  [Do Exercise-Based Prevention Programs Reduce Injury in Endurance Runners?, Sports Med 2024](https://link.springer.com/article/10.1007/s40279-024-01993-7)
- **Primary lifts.** Heavy squat or trap bar deadlift, low reps. Calf raises,
  both straight and bent knee, loaded heavy.
- **Accessory.** Single leg work, hip abductors, hamstring eccentrics, foot and
  tibialis.
- **Conditioning.** The sport is the conditioning. Do not add gym cardio.
- **Avoid.** High-rep leg work. Circuit-style "runner's strength" that adds
  fatigue without adding force. Hypertrophy blocks during a race build.
- **Evidence.** Strength training improves running economy by 2 to 8% and tends
  to improve 1.5 to 10 km time trial performance. Heavy and explosive strength
  both work.
  [Blagrove, Howatson and Hayes 2018, Sports Med](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5889786/),
  [Rønnestad and Mujika 2014, SJMSS](https://pubmed.ncbi.nlm.nih.gov/23914932/)
- **In-season / race block week.** 1 to 2 sessions. 3 to 4 exercises. Squat or
  deadlift 3x4 @85%, calf raise 3x6 heavy, single leg RDL 2x6, plyos 2x5 low
  volume. Never the day before a key session.
- **Off-season / base week.** 2 to 3 sessions. Same lifts, more sets, plus
  hypertrophy work for the posterior chain if the runner is underbuilt.

### 6.4 Sprinting and track sprints

- **Qualities.** Rate of force development, maximal strength relative to
  bodyweight, horizontal force production, eccentric hamstring strength.
- **Energy.** Phosphagen. 10 to 45 seconds of maximal effort with very long
  recovery.
- **Injury hotspots.** Hamstring, above all. Long head of biceps femoris is the
  most frequently damaged. Hamstring force rises about 1.3-fold going from 80%
  to 100% of max velocity.
  [Prevention and Rehabilitation of the Athletic Hamstring Injury](https://pmc.ncbi.nlm.nih.gov/articles/PMC12034042/)
- **Prevention.** Nordic curls plus regular maximal sprint exposure. Sprinting
  activates biceps femoris long head more than the Nordic does, so both belong
  in the plan.
  [EMG comparison](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11378697/)
- **Primary lifts.** Back squat, trap bar deadlift, hip thrust, power clean or
  clean pull, jump squat.
- **Accessory.** Nordic curl, RDL, calf and tibialis, hip flexor strength.
- **Conditioning.** Almost none. Tempo runs at 70% for recovery only.
- **Avoid.** Anything that leaves the athlete sore for a sprint session. Long
  aerobic work. Failure training.
- **In-season week.** 2 short sessions. Squat 3x3 @85%, hip thrust 3x5, Nordic
  2x4. Speed days are the priority. Gym is support.
- **Off-season week.** 3 to 4. Max strength block first, then a power and
  plyometric conversion block. Sprint volume stays year round.

### 6.5 Cycling

- **Qualities.** Sustained aerobic power, repeat high-power efforts, low mass,
  bone density (which cycling does not provide).
- **Energy.** Oxidative dominant with glycolytic surges.
- **Injury hotspots.** Low back, knee (patellofemoral from cleat and saddle
  position), neck, and crash trauma. Also low bone mineral density from a
  non-weightbearing sport.
- **Prevention.** Weightbearing lifting is itself the bone intervention.
  Position fit is out of trainer scope. Refer.
- **Primary lifts.** Squat, leg press, deadlift, step-up. Heavy, low rep.
- **Accessory.** Trunk endurance, glute medius, upper back for time-trial
  position tolerance.
- **Conditioning.** On the bike.
- **Avoid.** High-rep leg burnout that steals from bike sessions. Lifting the
  day before a key interval day.
- **Evidence.** Heavy strength training is specifically recommended for
  improving cycling economy, and improves power output at VO2max.
  [Rønnestad and Mujika 2014](https://pubmed.ncbi.nlm.nih.gov/23914932/),
  [heavy strength training in endurance cyclists, meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC12881108/)
- **Note.** Cycling produces less interference with strength than running does,
  which makes cyclists unusually good candidates for concurrent training.
  [Wilson et al. 2012](https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx)
- **In-season week.** 1 to 2 sessions. Squat 3x4, RDL 3x5, step-up 2x8, trunk.
- **Off-season week.** 2 to 3 sessions with real hypertrophy and max strength
  work. This is the only window where added muscle is affordable.

### 6.6 Swimming

- **Qualities.** Upper body pulling power and endurance, shoulder capacity,
  trunk stiffness, streamline mobility, start and turn power.
- **Energy.** Depends on event. 50 m is phosphagen. 1500 m is oxidative.
- **Injury hotspots.** Shoulder. Shoulder pain incidence 52 to 73% in elite
  swimmers. Also low back and breaststroker's knee.
  [Dry-land shoulder rotators strength training in competitive swimmers](https://pmc.ncbi.nlm.nih.gov/articles/PMC7052717/)
- **Prevention.** Dryland rotator cuff and scapular stabiliser work. Dry-land
  strengthening programmes reduce shoulder injury in competitive swimmers.
  [Same source](https://pmc.ncbi.nlm.nih.gov/articles/PMC7052717/),
  [Kabat D2 elastic band programme](https://pmc.ncbi.nlm.nih.gov/articles/PMC10679734/)
- **Primary lifts.** Pull-up, chin-up, row variants, trap bar deadlift, squat
  (for starts and turns), overhead press if the shoulder tolerates it.
- **Accessory.** External rotation, prone Y/T/W, face pull, serratus work,
  anti-extension core.
- **Conditioning.** In the pool.
- **Avoid.** High-volume overhead pressing on top of high overhead swim volume.
  Behind-the-neck anything. Adding pull volume during a heavy pool block.
- **In-season week.** 2 short sessions. Pull-up 3x5, row 3x8, trap bar 3x5,
  cuff and scapular circuit every session.
- **Off-season week.** 3 sessions with more lower body and general strength.
  Swimmers are often weak on land. This is where that gets fixed.

### 6.7 Rock climbing

- **Qualities.** Finger flexor strength and endurance, pulling strength, body
  tension, hip mobility, high strength-to-mass ratio.
- **Energy.** Bouldering is phosphagen. Route climbing is glycolytic with
  forearm-local endurance the limiter.
- **Injury hotspots.** Finger flexor pulleys, especially A2, A3 and A4. Pulley
  injury is consistently the most frequent climbing injury, followed by finger
  tenosynovitis and capsulitis. Then shoulder and elbow.
  [Miro, vanSonnenberg, Sabb and Schöffl 2021, Finger Flexor Pulley Injuries in Rock Climbers](https://pubmed.ncbi.nlm.nih.gov/33966972/),
  [Risk factors and injury prevention for overuse injuries in adult climbers, systematic review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10756908/)
- **Prevention.** Thorough progressive warm-up before hard finger loading.
  Manage the crimp grip specifically, since it is the injury mechanism. Build
  antagonist pushing and external rotation to balance the pulling.
- **Primary lifts.** Weighted pull-up, hangboard (as sport-specific loading, not
  a gym lift), front lever progressions, ring rows, overhead press.
- **Accessory.** Rotator cuff, scapular retraction, wrist extensors, hip
  mobility, core anti-extension.
- **Conditioning.** On the wall. Aerobic base only for recovery.
- **Avoid.** Adding hangboard volume during a hard climbing block. Loading
  fingers when they are already sore. Full crimp under maximal added load for
  beginners. Under 18s should not hangboard at all (growth plate risk).
  UNVERIFIED: growth plate claim widely stated in climbing medicine, I did not
  verify a primary source within the timebox.
- **In-season / project season week.** Climbing 3 days. Gym 1 to 2 short
  sessions: weighted pull-up 4x3, press 3x6, antagonist and cuff circuit.
- **Off-season week.** 2 to 3 gym sessions with more general strength and a
  structured hangboard protocol, plus lower body work climbers usually skip.

### 6.8 Martial arts, BJJ and MMA

- **Qualities.** Grip strength and grip endurance, isometric trunk and low back
  strength, repeat high-intensity effort, neck strength, hip mobility.
- **Energy.** Intermittent. High, moderate and low intensity actions interleaved
  in a match. Tournament format can mean 4 to 5 or more matches in a day.
  [Physical and Physiological Profiles of BJJ Athletes, Sports Med Open](https://link.springer.com/article/10.1186/s40798-016-0069-5)
- **Injury hotspots.** Sprains and strains to upper and lower extremity, plus
  neck. BJJ competition injury data is thin relative to MMA.
  [Injury prevalence in BJJ literature review](https://thesportjournal.org/article/injury-prevalence-in-brazilian-jiu-jitsu-and-mitigation-strategies-for-brazilian-jiu-jitsu-practitioners-and-instructors-a-literature-review/)
- **Prevention.** Neck strengthening. Shoulder external rotation capacity. Hip
  and knee control. Tap early, which is a coaching point, not a gym one.
- **Primary lifts.** Deadlift, front squat, weighted pull-up, overhead press,
  loaded carries.
- **Accessory.** Grip (thick bar, towel hangs, farmer's carry), neck harness or
  isometrics, rotational core, hip mobility.
- **Conditioning.** Rolling provides most of it. Add repeat-effort intervals if
  the athlete gasses in later rounds.
- **Avoid.** Heavy lifting the day before hard sparring. Failure training in
  season. Chasing grip fatigue when training already destroys grip.
- **In-season / camp week.** 2 short sessions. Deadlift or squat 3x3, pull-up
  3x5, carry 3 trips, neck isometrics.
- **Off-season week.** 3 to 4 sessions, hypertrophy and max strength, plus
  aerobic base building.
- **Weight class note.** See section 8.

### 6.9 Tennis and racquet sports

- **Qualities.** Rotational power, lateral movement and deceleration, shoulder
  and elbow durability, repeat-effort capacity over hours.
- **Energy.** Intermittent, phosphagen and glycolytic points inside a long
  aerobic frame.
- **Injury hotspots.** Lower limb dominates (48 to 56% of injuries), then lumbar
  (12 to 39%), then shoulder overuse. Contemporary professional injury incidence
  is 56.6 to 62.7 per 1000 hours.
  [Risk Factors and Prevention of MSK Injuries in High-Performance Tennis Players, systematic review 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12568103/)
- **Prevention.** Three clusters with evidence: external load control with a
  four-week ramp-up (up to 21% injury reduction), core stability plus eccentric
  rotator cuff training (26% reduction in overuse), and equipment fit, where
  grip-size personalisation halved lateral epicondylalgia.
  [Same review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12568103/)
  Loss of 15 degrees or more of shoulder internal rotation, scapular dyskinesis
  and posterior capsule tightness roughly double time-loss shoulder risk. Screen
  for these.
- **Primary lifts.** Split squat, lateral lunge, trap bar deadlift, single-arm
  row, landmine press, med ball rotational throws.
- **Accessory.** Eccentric infraspinatus and external rotation, scapular
  control, anti-rotation core, wrist and forearm.
- **Conditioning.** Repeat-sprint and lateral shuttles. Aerobic base for
  multi-hour matches.
- **Avoid.** Bilateral-only training. Ignoring the non-dominant side. Ramping
  match volume fast: ACWR at or above 1.3 in juniors and 1.5 in adults is the
  strongest extrinsic predictor in this population.
- **In-season week.** 2 sessions, 30 to 40 min. Split squat 3x6/side, single-arm
  row 3x8, med ball rotation 3x5/side, cuff circuit.
- **Off-season week.** 3 to 4. Add max strength, lateral plyometrics, and a
  dedicated shoulder capacity block.

### 6.10 Volleyball

- **Qualities.** Vertical jump, repeat jump capacity, landing control, shoulder
  capacity for hitting and serving, lateral movement.
- **Energy.** Phosphagen. Short rallies, frequent rests, long match frame.
- **Injury hotspots.** Patellar tendinopathy above all: highest prevalence of any
  sport at 24.8% pooled, 44.6% in elite players. Then ankle sprain and shoulder
  overuse.
  [Patellar tendinopathy overview](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10541843/)
- **Prevention.** Heavy slow, eccentric or isometric patellar loading, which
  works in-season. Ankle proprioception. Shoulder cuff and scapular work. Jump
  volume monitoring is the real intervention.
  [In-season management of patellar tendinopathy, scoping review](https://www.sciencedirect.com/science/article/abs/pii/S1466853X22000426)
- **Primary lifts.** Trap bar deadlift, front squat, split squat, hip thrust,
  overhead press if shoulder allows.
- **Accessory.** Spanish squat and wall sit isometrics, calf, tibialis, cuff.
- **Conditioning.** Minimal. The sport is anaerobic-alactic with rest.
- **Avoid.** Adding plyometric volume in-season. Deep-load jumping on a painful
  tendon without a loading plan.
- **In-season week.** 1 to 2 sessions. Trap bar 3x4, split squat 2x6/side,
  isometric wall sit 4x45s, cuff circuit.
- **Off-season week.** 3 to 4. Max strength, then a jump-capacity block. Fix
  tendon capacity before jump volume returns.

### 6.11 Ice hockey

- **Qualities.** Skating acceleration, lateral hip power, adductor strength,
  repeat-shift capacity, collision tolerance.
- **Energy.** Repeated 30 to 60 second maximal shifts with 2 to 4 minutes rest.
  Glycolytic dominant.
- **Injury hotspots.** Groin and adductor. Adductor and groin injuries are
  around a quarter of reported injuries in hockey. Also concussion, MCL,
  shoulder from boards.
  [Groin injuries in hockey players, summarising Tyler et al.](https://mikereinold.com/groin-injuries-in-hockey-players/)
- **Prevention.** Adductor strengthening. Screen adduction-to-abduction strength
  ratio: NHL players who later strained a groin had a pre-season ratio of 78%
  vs 95% in uninjured players, and an adductor programme for the at-risk group
  significantly reduced injuries. Copenhagen adduction is the modern default.
  [Same source](https://mikereinold.com/groin-injuries-in-hockey-players/),
  [Harøy 2019](https://pubmed.ncbi.nlm.nih.gov/29891614/)
- **Primary lifts.** Front squat, trap bar deadlift, lateral lunge, split squat,
  hip thrust.
- **Accessory.** Copenhagen adduction, adductor slides, hip flexor, neck,
  anti-rotation core.
- **Conditioning.** Bike intervals matching shift length. 40s hard, 2 min easy.
- **Avoid.** Ignoring the adductors, which is the single most common error in
  hockey programming. Long slow cardio.
- **In-season week.** 1 to 2 sessions. Trap bar 3x4, lateral lunge 2x6/side,
  Copenhagen 2x8/side (keep this even when everything else is cut), neck
  isometrics.
- **Off-season week.** 3 to 4. Max strength and hypertrophy, plus a dedicated
  adductor progression and on-ice conditioning ramp.

### 6.12 Rugby and American football

- **Qualities.** Maximal strength, mass, acceleration, collision tolerance, neck
  strength, repeat-effort capacity. Position-dependent to an extreme degree.
- **Energy.** Highly positional. American football linemen work in 5-second
  phosphagen bursts. Rugby back-row players work glycolytic and aerobic across
  80 minutes.
  [Narrative review of physical demands and workload management in American football, Sports Med 2017](https://link.springer.com/article/10.1007/s40279-017-0783-2)
- **Injury hotspots.** Hamstring, shoulder, knee, head and neck. Collision load
  is the driver. Collision counts and collision load computed via EWMA-ACWR were
  associated with injury risk (odds ratios 4.20 and 4.44).
  [Contact load in rugby union, Front Physiol 2025](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2025.1672824/full)
- **Prevention.** Neck strength training, which is a modifiable risk factor, and
  where flexion-to-extension and left-right imbalances are candidate risk
  factors. Nordic curls. Collision load monitoring alongside running load.
  [Isometric neck strength in rugby union](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9031103/)
- **Primary lifts.** Back squat, bench press, trap bar deadlift, power clean,
  overhead press, hip thrust.
- **Accessory.** Neck (all four directions), Nordic curl, upper back, loaded
  carries, single leg.
- **Conditioning.** Position-specific. Linemen do short high-intensity work.
  Backs do repeat-sprint and aerobic.
- **Avoid.** Treating all positions the same. Counting only running load and
  ignoring collisions. Heavy lifting inside 48 hours of a game.
- **In-season week.** 2 sessions. Day after game: upper, moderate. Mid-week:
  lower, heavy, low volume. Neck every session.
- **Off-season week.** 4 sessions, upper/lower split, hypertrophy block then max
  strength block, sprint and change of direction throughout.

### 6.13 Golf

- **Qualities.** Rotational power, thoracic rotation range, hip mobility, trunk
  stability, club head speed.
- **Energy.** Almost entirely aerobic and low intensity, punctuated by maximal
  rotational efforts. Walking 18 holes is the real endurance demand.
- **Injury hotspots.** Low back, dominant. Around 50% prevalence of low back
  pain in professional golfers, and golf-related low back pain accounts for 18
  to 54% of documented golf ailments.
  [Low back pain and golf: a review of biomechanical risk factors](https://pmc.ncbi.nlm.nih.gov/articles/PMC9219256/)
  Then lead-side wrist and elbow.
- **Prevention.** Trunk endurance and rotational control. Screen movement, for
  example with the TPI screen's 16 patterns, and train what the screen finds.
  [TPI screen, described in the LBP review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9219256/)
  Note: the strongest predictors of golf low back pain are age, higher body
  mass and prior back pain, not swing metrics like X-factor.
  [Same review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9219256/)
  That means an agent should not sell swing-metric fixes as injury prevention.
- **Primary lifts.** Trap bar deadlift, goblet or front squat, single-arm row,
  landmine rotation, med ball rotational throw.
- **Accessory.** Thoracic rotation mobility, hip internal rotation, anti-rotation
  and anti-extension core, forearm and wrist.
- **Conditioning.** Walking capacity. Zone 2 work so 18 holes is not fatiguing.
- **Avoid.** Loaded spinal rotation under heavy weight. Excessive lumbar
  extension work. Swing-specific weighted implements as strength training.
- **In-season week.** 2 sessions, 30 minutes. Deadlift 3x5, row 3x8, med ball
  rotation 3x5/side, anti-rotation 2 sets, mobility daily.
- **Off-season week.** 3 sessions with real max strength and power work. Strength
  training improves club head speed and driving distance.
  UNVERIFIED: I did not fetch a primary trial for the club head speed effect in
  this timebox. Widely reported but verify before an agent quotes a number.

### 6.14 Dance and gymnastics

- **Qualities.** Extreme range of motion under control, relative strength,
  landing control, jump capacity, aesthetic line under fatigue.
- **Energy.** Repeat short maximal efforts. Rehearsal and training volume is
  aerobic and very high.
- **Injury hotspots.** Lumbar spine (spondylolysis in gymnasts from repeated
  hyperextension), ankle and foot, hip. Plus the biggest one:
- **Energy availability.** Dancers and gymnasts are recognised at-risk
  populations for Relative Energy Deficiency in Sport. REDs affects bone,
  endocrine and immune health as well as performance, and overlaps with
  overtraining syndrome.
  [2023 IOC consensus statement on REDs, BJSM](https://stillmed.olympics.com/media/Documents/Athletes/Medical-Scientific/Consensus-Statements/REDs/BJSM-IOC-consensus-statement-on-Relative-Energy-Deficiency-in-Sport-REDs.pdf),
  [IOC announcement](https://www.olympics.com/ioc/news/ioc-publishes-new-consensus-statement-on-relative-energy-deficiency-in-sport-reds-to-protect-athlete-health)
  **Trainer scope stops here.** Screen and refer. Do not counsel on intake.
- **Prevention.** Strength through full range, not stretching alone. Calf and
  foot strength. Anti-extension core to spare the lumbar spine. Load monitoring
  through rehearsal season.
- **Primary lifts.** Split squat, single leg RDL, weighted pull-up, calf raise,
  hip thrust.
- **Accessory.** Foot intrinsics, tibialis, hip external rotators, anti-extension
  core, scapular work for gymnasts.
- **Conditioning.** Rehearsal and routine work provides it.
- **Avoid.** Adding hypertrophy volume during show or competition season.
  Stretching as the only intervention. Any conversation about bodyweight, which
  is not in trainer scope for this population.
- **In-season / show week.** 1 to 2 sessions, 25 minutes. Split squat 3x6/side,
  calf 3x10, single leg RDL 2x8, core 2 sets.
- **Off-season week.** 3 sessions with real loading. This population is usually
  under-strengthened and over-stretched.

### 6.15 Powerlifting

- **Qualities.** Maximal strength in squat, bench and deadlift. Nothing else is
  scored.
- **Energy.** Phosphagen only, with long rests.
- **Injury hotspots.** Low back, shoulder, knee. Injury incidence in powerlifting
  is 1.0 to 4.4 per 1000 hours of training, which is low compared with field
  sports.
  [Aasa et al. 2017, Injuries among weightlifters and powerlifters, BJSM](https://pubmed.ncbi.nlm.nih.gov/27328853/)
- **Prevention.** Load management and technique. The main risk is ramping volume
  or intensity too fast, not the lifts themselves.
- **Primary lifts.** The three competition lifts plus their close variants.
- **Accessory.** Whatever addresses the individual's weak point. Rows, dips,
  RDLs, leg press, triceps.
- **Conditioning.** Enough aerobic base to recover between sets and sessions.
  Two 20 to 30 minute easy sessions a week is plenty.
- **Avoid.** Chasing novelty. Running high volume and high intensity at the same
  time. Testing maxes outside a planned peak.
- **In-season / meet prep.** Peaking block: intensity rises, volume falls, then
  a taper of about a week to 10 days. Openers taken at around 90 to 93% two
  weeks out. Nothing new inside the last four weeks.
- **Off-season week.** 4 sessions, higher volume, more variation, hypertrophy
  emphasis on weak points.
- **Note.** For this sport, the gym IS the sport. The needs analysis collapses:
  movement analysis is the three lifts, physiological analysis is max strength,
  injury analysis is the athlete's own history.

### 6.16 Olympic weightlifting

- **Qualities.** Maximal strength, rate of force development, overhead and
  ankle/hip mobility, technical consistency under load.
- **Energy.** Phosphagen only.
- **Injury hotspots.** Low back, knee, shoulder and wrist. Incidence 2.4 to 3.3
  per 1000 hours.
  [Aasa et al. 2017](https://pubmed.ncbi.nlm.nih.gov/27328853/)
- **Prevention.** Mobility as a prerequisite for position, not as a warm-up
  ritual. Overhead stability. Technical volume at submaximal loads.
- **Primary lifts.** Snatch, clean and jerk, and their derivatives. Front squat,
  back squat, pulls, presses.
- **Accessory.** Overhead squat, ankle and thoracic mobility, upper back, core.
- **Conditioning.** Minimal. Light aerobic for recovery only.
- **Avoid.** High-fatigue conditioning that degrades technique. Grinding reps.
  Training the classic lifts when fatigued enough that positions break down.
- **In-season / meet prep.** Higher intensity, lower volume, tapering to
  singles. Technique quality is the stopping criterion, not rep count.
- **Off-season week.** 4 to 6 sessions, high technical volume, strength blocks
  on squats and pulls.

### 6.17 CrossFit-style training and functional fitness competition

- **Qualities.** Broad. Max strength, weightlifting technique, gymnastics
  skills, monostructural endurance, repeat-effort capacity.
- **Energy.** All of them, which is the programming problem.
- **Injury hotspots.** Shoulder (26%), spine (24%), knee (18%). Prevalence around
  30 to 35%, incidence around 3.2 per 1000 hours, comparable to weightlifting
  and powerlifting.
  [Musculoskeletal Injuries in CrossFit, systematic review and meta-analysis](https://www.germanjournalsportsmedicine.com/archive/archive-2021/issue-7/musculoskeletal-injuries-in-crossfitr-a-systematic-review-and-meta-analysis-of-injury-rates-and-locations/),
  [Injury in CrossFit: systematic review of epidemiology and risk factors](https://pubmed.ncbi.nlm.nih.gov/33322981/)
- **Prevention.** Shoulder capacity work as a standing block, since the shoulder
  is the top site. Cap high-rep technical lifting under fatigue. Progress
  gymnastics volume (kipping pull-ups, muscle-ups, handstand push-ups) slowly.
- **Primary lifts.** Squat, deadlift, press, snatch, clean and jerk.
- **Accessory.** Cuff and scapular, midline, grip, and unilateral work that
  competition programming skips.
- **Conditioning.** Built into the sport. The gap is usually a true aerobic base,
  which most CrossFit athletes lack.
- **Avoid.** Redlining every day, which is the sport's cultural default and the
  monotony problem from section 4. Programming for time on technical lifts when
  the athlete's technique breaks under fatigue.
- **In-season / Open or competition week.** Reduce total volume, keep intensity,
  keep skill practice, cut accessory work.
- **Off-season week.** Separate the qualities into blocks. A strength block that
  is actually a strength block. An aerobic block that is actually zone 2.
  Concurrent chaos is what caps this population.

### 6.18 Skiing and snowboarding

- **Qualities.** Eccentric quadriceps strength, isometric endurance in a flexed
  position, lateral stability, reactive balance, aerobic base for long days.
- **Energy.** 1 to 3 minute glycolytic runs with lift rides as rest, over a long
  aerobic day.
- **Injury hotspots.** Knee, above all ACL and MCL. Also shoulder and wrist,
  particularly in snowboarding. Recreational skiers with worse lower-extremity
  agility and balance have higher injury risk, and weaker core flexion strength
  and poorer neuromuscular control associate with higher ACL rupture risk.
  [Prevention of ACL Injuries in Competitive Adolescent Alpine Skiers](https://pmc.ncbi.nlm.nih.gov/articles/PMC7739649/)
- **Prevention.** A neuromuscular and core programme, on and off snow, focusing
  on performing exercises equally well on both legs. In a Swedish cohort this
  cut ACL injuries from 8.1% to 3.9%.
  [Same source](https://pmc.ncbi.nlm.nih.gov/articles/PMC7739649/)
- **Primary lifts.** Back squat, split squat, lateral lunge, RDL, step-down.
- **Accessory.** Eccentric quad work (slow tempo squats, Spanish squats), single
  leg balance, adductors and abductors, calf.
- **Conditioning.** Bike or ski erg intervals matching run length. Aerobic base
  for multi-hour days.
- **Avoid.** Showing up to the first day of the season untrained, which is the
  actual mechanism for most recreational knee injuries. Ignoring left-right
  asymmetry.
- **In-season week.** 1 to 2 short sessions on non-ski days. Split squat
  3x6/side, RDL 3x6, balance and landing work.
- **Off-season / pre-season week.** 3 sessions for 8 to 12 weeks before the
  season. Max strength, eccentric quad emphasis, plyometrics, plus the
  neuromuscular programme.

### 6.19 Hiking and backpacking

- **Qualities.** Eccentric quadriceps endurance (descents are the limiter),
  loaded carrying capacity, aerobic base, ankle and foot durability.
- **Energy.** Oxidative, over many hours.
- **Injury hotspots.** Knee (patellofemoral pain on descents), ankle sprain,
  blisters and foot problems, low back from pack load.
- **Prevention.** Eccentric quad conditioning before the trip. Progressive pack
  weight, not a jump straight to full load. Ankle strengthening.
  UNVERIFIED: I did not find a specific RCT for hiking injury prevention within
  this timebox. Treat the above as reasoned application of the general
  eccentric-loading and progressive-overload evidence, not a cited protocol.
- **Primary lifts.** Step-up and step-down (weighted), split squat, RDL, loaded
  carries, back squat.
- **Accessory.** Calf raise both straight and bent knee, tibialis, hip abductors,
  trunk endurance under load.
- **Conditioning.** Progressive loaded walking, ideally on the actual terrain
  type. Downhill walking specifically, since that is the injury mechanism and
  the muscle soreness driver.
- **Avoid.** Training only flat and uphill, then descending 1500 m on trip day.
- **Pre-trip block (12 weeks out).** 2 gym sessions plus 1 long loaded walk a
  week. Add 10% to pack weight or distance per week, not both.
- **Trip week.** Nothing hard in the last 5 days. Walk easy.

### 6.20 Esports and desk-bound work

Brief, because the trainer's job here is small.

- **Qualities.** Postural endurance, hip and thoracic mobility, upper limb
  tissue tolerance, general health.
- **Energy.** Not a factor.
- **Injury hotspots.** 73% of esports players reported pain in the past year.
  Spine 41% (neck specifically 48%), upper extremity 31%, wrist 37%. Professional
  players report more pain than amateurs. Inadequate sleep and no warm-up
  routine both associate with more pain.
  [Do Esports Players Experience Pain? Systematic review and meta-analysis, Sports Med Open](https://link.springer.com/article/10.1186/s40798-025-00971-1)
- **Prevention.** Regular breaks in prolonged sitting, ergonomic setup, and load
  management on practice volume. Tailored strengthening or mobility programmes
  may help upper limb disorders.
  [Musculoskeletal pain in eSports players: clinical implications](https://www.tandfonline.com/doi/full/10.1080/15438627.2025.2594401)
- **Program.** A general strength program with extra upper back, neck and
  shoulder work, plus hip and thoracic mobility. Two to three sessions a week.
  There is no in-season/off-season distinction to manage.
- **Avoid.** Selling "gamer-specific" wrist gadgets. The evidence supports
  breaks, sleep, warm-up and general strength.

---

## 7. Youth and masters athletes

### Youth

The NSCA position statement on long-term athletic development is the anchor
document. Ten pillars, published in J Strength Cond Res 30(6):1491-1509.
[Lloyd et al. 2016, NSCA Position Statement on Long-Term Athletic Development](https://www.nsca.com/globalassets/about/position-statements/nsca_position_statement_long-term_athletic_development.pdf)

Key points an agent should hold:

- Children are not miniature adults. Growth and maturation rates fluctuate, and
  this changes both training response and injury risk.
  [Same source](https://www.nsca.com/globalassets/about/position-statements/nsca_position_statement_long-term_athletic_development.pdf)
- Resistance training in youth is safe and beneficial when supervised and
  appropriately prescribed. The risk is bad supervision, not the barbell.
- Early specialisation raises injury risk and the NSCA position discourages it.
  [NSCA on LTAD, youth resistance training and early specialisation](https://www.nsca.com/about-us/position-statements/youth-training-and-long-term-athletic-development/ltad-youth-resistance-training-and-early-sport-specialization-what-it-all-means/)
- Program for movement competence first, load second.
- During peak height velocity, expect temporary coordination loss and higher
  overuse risk. Reduce plyometric and high-load volume through that window.
- Total hours across all sports and school teams is the load that matters, and
  it is the number nobody counts. Ask for it.

### Masters

NSCA has a position statement on resistance training for older adults.
[Fragala et al. 2019, Resistance Training for Older Adults: Position Statement from the NSCA](https://journals.lww.com/nsca-jscr/fulltext/2019/08000/resistance_training_for_older_adults__position.1.aspx)

Key points:

- Masters athletes who lift have greater strength, power, rate of force
  development, muscle volume and type II fibre cross-sectional area than
  untrained age-matched people, and voluntary activation similar to young adults.
  [Recovery from Resistance Exercise in Older Adults, Sports Med Open 2023](https://sportsmedicine-open.springeropen.com/articles/10.1186/s40798-023-00597-1)
- Power declines faster than strength with age. Prioritise fast concentric
  intent, not just heavy load.
- Recovery takes longer. Space hard sessions further apart, and expect the
  weekly hard-session count to be lower than a 25-year-old's.
- Older adults need a **higher** weekly maintenance dose than young adults to
  hold hypertrophy, even though strength holds well.
  [Bickel et al. 2011](https://pubmed.ncbi.nlm.nih.gov/21131862/)
  Practical read: the minimum in-season dose for a masters athlete is 2 sessions
  a week, not 1.
- Tendon adapts more slowly than muscle. Ramp plyometrics and sprint work over
  months, not weeks.

---

## 8. Weight-class sports, within trainer scope

Sports affected: wrestling, boxing, MMA, judo, taekwondo, weightlifting,
powerlifting, rowing lightweight, some climbing contexts.

**Nutrition and weight-cutting protocols are out of scope for a trainer agent.**
Say so explicitly and refer to a sports dietitian. What follows is the training
side only.

Facts that justify the referral:

- Prevalence of rapid weight loss among wrestlers is between 40 and 90%. The
  common methods are fluid restriction and dehydration, prolonged fasting, and
  high-intensity exercise in plastic suits.
  [Prevalence of rapid weight loss in Olympic style wrestlers](https://pmc.ncbi.nlm.nih.gov/articles/PMC9559051/)
- Three American college wrestlers died in November 1997 after food and fluid
  restriction combined with vapour-impermeable suits in heat.
  [ACSM Expert Consensus Statement on Weight Loss in Weight-Category Sports](https://researchonline.ljmu.ac.uk/id/eprint/17789/1/ACSM%20Consensus%20Statement%20Weight%20Making.pdf)
- Youth athletes have immature sweating function and are more likely than adults
  to raise core temperature in hot environments like saunas, so heat-stroke risk
  is higher.
  [Same source](https://researchonline.ljmu.ac.uk/id/eprint/17789/1/ACSM%20Consensus%20Statement%20Weight%20Making.pdf)
- Position statements from ACSM, the Association of Ringside Physicians and NATA
  warn against extreme practices.
  [Disturbing Weight Cutting Behaviors in Young Combat Sports Athletes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8863958/)
- ISSN has a position stand covering fight camp weight descent, fight week, and
  post-weigh-in recovery. That is the document to point a nutrition
  professional at.
  [ISSN position stand: nutrition and weight cut strategies for MMA and other combat sports](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11894756/)

Training-side rules an agent can apply:

- Do not program hypertrophy blocks in a weight-class athlete without asking
  what class they intend to make.
- Fight week or meet week: no new stimulus, no soreness, no failure work. Volume
  down, intensity preserved briefly, then stop.
- If the athlete describes dehydration methods, sauna suits, or fasting, stop
  programming and refer. Log the referral.
- Weight-class athletes doing a long slow descent should keep lifting heavy at
  low volume, which is exactly the in-season maintenance prescription in section
  2. Strength holds much better than hypertrophy in an energy deficit.
  UNVERIFIED: I did not fetch a primary source for the strength-vs-hypertrophy
  retention claim in deficit within this timebox.

---

## 9. What an agent should ask that it currently would not

A short list of prompts worth building into the needs-analysis script, because
each one changes the plan and athletes rarely volunteer them.

1. "How many hours of sport, across every team and club, this week?"
2. "When is your next competition, and how many between now and then?"
3. "What did your last injury cost you in weeks?"
4. "What does your coach already make you do in the gym?" (Duplication is common
   and dangerous.)
5. "Is there a weight class?"
6. "Are you in a growth spurt / has your shoe size changed recently?" (Youth.)

---

## 10. Open questions for the user

I could not resolve these. They need a decision, not more research.

1. **How deep should sport profiles go in the product?** Twenty profiles is a
   lot of content to maintain. Does the agent carry them as data, or does it
   run the needs-analysis script live and derive the profile each time? The
   script generalises to any sport. The profiles are faster and more accurate
   for the sports covered. I lean toward the script as the mechanism, with
   profiles as a cached lookup for the common cases, but that is a product call.

2. **Does the trainer agent monitor load, or just prescribe?** Session RPE
   collection needs a post-session prompt every session. That is a notification
   design question and an ADHD-adherence question, not a programming one.
   Without it, sections 4's formulas are decoration.

3. **How hard should the agent gate on the ACWR flag?** I recommend soft flag
   only, given the Impellizzeri critique. But if the user wants a harder stop
   ("agent refuses to increase load when ratio > 1.5"), that is a safety
   preference I should not set unilaterally.

4. **Referral thresholds.** Weight cutting, REDs symptoms, and pain that lasts
   more than two weeks all warrant "stop and refer". Who is the referral, in
   practice, for a solo user with no team medical staff? The agent needs
   something concrete to say.

5. **Which sports actually matter?** I covered 20 because the brief listed them.
   If the real user set is three sports, the maintenance burden argument in
   question 1 goes away and deeper profiles get affordable.

6. **Youth users.** Does this product accept under-18 users at all? If yes, the
   LTAD material needs to be a hard constraint in the agent, not a section in a
   research file. If no, say so and cut the youth section.

---

## 11. Gaps and confidence

What is well sourced here:
- The needs-analysis structure (NSCA).
- In-season maintenance frequency (Rønnestad).
- Taper numbers (Bosquet).
- Concurrent training interference (Wilson).
- ACWR and its critique (Gabbett, Impellizzeri).
- Session RPE (Foster, Haddad).
- Injury prevention programs (Lauersen, Soligard, van Dyk, Harøy, ACL reviews).
- Sport injury epidemiology for soccer, basketball, volleyball, tennis, hockey,
  swimming, climbing, esports, CrossFit, powerlifting, weightlifting, golf,
  skiing, rugby.

What is thin and marked UNVERIFIED in the text:
- Spiering 2021 exact minimal-dose numbers (paywalled).
- Verkhoshansky's six dynamic correspondence criteria (not fetched).
- The 10% weekly progression rule (widely taught, weakly evidenced).
- Youth hangboard / growth plate guidance in climbing.
- Golf strength training effect on club head speed (no primary trial fetched).
- Hiking injury prevention (no sport-specific RCT found).
- Strength vs hypertrophy retention in energy deficit.
- Energy system time boundaries in the step 4 table.

Not covered, out of time:
- Track and field throws, field hockey, surfing. Baseball and softball, rowing,
  triathlon and team handball are now covered in Appendix B.
- Para athlete considerations. Slice 10 may cover this.
- Detailed return-to-play progressions after injury.

---

## Sources

Needs analysis and general framework
- NSCA, Essentials of Strength Training and Conditioning, 5th ed.: https://www.nsca.com/certification/cscs/essentials-of-strength-training-and-conditioning-5th-edition/
- NSCA, Needs Analysis for Injury Prevention: https://www.nsca.com/education/articles/kinetic-select/needs-analysis-for-injury-prevention/
- NSCA / NSGA, Needs Analysis for Sports Training: https://www.nsga.com/needs-analysis-for-sports-training/
- van Mechelen, sequence of prevention: https://pubmed.ncbi.nlm.nih.gov/1509229/
- Bompa and Buzzichelli, Periodization: https://us.humankinetics.com/products/periodization-7th-edition

Strength, transfer, periodization
- Suchomel, Nimphius and Stone 2016, Sports Med: https://link.springer.com/article/10.1007/s40279-016-0486-0
- Rønnestad et al., in-season strength maintenance frequency in professional soccer: https://www.researchgate.net/publication/51601921_Effects_of_In-Season_Strength_Maintenance_Training_Frequency_in_Professional_Soccer_Players
- In-season autoregulation of one weekly strength session, J Sports Sci 2023: https://www.tandfonline.com/doi/full/10.1080/02640414.2023.2227536
- Bickel, Cross and Bamman 2011, Med Sci Sports Exerc: https://pubmed.ncbi.nlm.nih.gov/21131862/
- Spiering et al. 2021, J Strength Cond Res: https://journals.lww.com/nsca-jscr/fulltext/2021/05000/maintaining_physical_performance__the_minimal_dose.35.aspx
- Bosquet et al. 2007, Effects of tapering on performance: https://pubmed.ncbi.nlm.nih.gov/17762369/
- Tapering in endurance athletes, PLOS One 2023: https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0282838
- Wilson et al. 2012, Concurrent Training meta-analysis: https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx
- Intra-session exercise sequence and the interference effect: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5752732/

Load management
- Gabbett 2016, BJSM: https://pubmed.ncbi.nlm.nih.gov/26758673/ and https://efsma.org/images/pdf/publications/Br-J-Sports-Med-2016-Gabbett-273-80.pdf
- Impellizzeri, Tenan et al. 2020, ACWR conceptual issues and pitfalls: https://www.semanticscholar.org/paper/Acute:Chronic-Workload-Ratio:-Conceptual-Issues-and-Impellizzeri-Tenan/ede5743a426fd6429d28f8505500a3f771dbcf8b
- ACWR retraction request background: https://www.globalperformanceinsights.com/post/has-the-acute-chronic-workload-ratio-been-debunked
- Foster et al. 2001, A New Approach to Monitoring Exercise Training: https://paulogentil.com/pdf/A%20New%20Approach%20to%20Monitoring%20Exercise%20Training.pdf
- Haddad et al. 2017, Session-RPE method, Front Neurosci: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5673663/

Injury prevention
- Lauersen et al. 2014, BJSM: https://www.ncbi.nlm.nih.gov/books/NBK169555/
- Lauersen et al. 2018, BJSM, strength training as superior prevention: https://www.researchgate.net/publication/327150440_Strength_training_as_superior_dose-dependent_and_safe_prevention_of_acute_and_overuse_sports_injuries_A_systematic_review_qualitative_analysis_and_meta-analysis
- FIFA 11+ narrative review: https://pubmed.ncbi.nlm.nih.gov/25878073/
- FIFA 11+ systematic review of RCTs, 2025: https://pmc.ncbi.nlm.nih.gov/articles/PMC12856364/
- van Dyk et al. 2019, Nordic hamstring meta-analysis: https://www.researchgate.net/publication/331367089_Including_the_Nordic_hamstring_exercise_in_injury_prevention_programmes_halves_the_rate_of_hamstring_injuries_A_systematic_review_and_meta-analysis_of_8459_athletes
- Nordic hamstring methodological reappraisal, J Clin Epidemiol 2021: https://www.sciencedirect.com/science/article/abs/pii/S0895435621002870
- Harøy et al. 2019, Adductor Strengthening Programme RCT: https://pubmed.ncbi.nlm.nih.gov/29891614/
- ACL prevention training in female athletes, systematic review: https://pubmed.ncbi.nlm.nih.gov/23016067/
- Neuromuscular training for knee injuries in female team athletes, meta-analysis: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12581765/
- Tyler et al. adductor screen and intervention, summarised: https://mikereinold.com/groin-injuries-in-hockey-players/
- Dry-land shoulder rotators strength training in swimmers: https://pmc.ncbi.nlm.nih.gov/articles/PMC7052717/
- Kabat D2 elastic band dry-land programme in swimmers: https://pmc.ncbi.nlm.nih.gov/articles/PMC10679734/
- ACL prevention in adolescent alpine skiers: https://pmc.ncbi.nlm.nih.gov/articles/PMC7739649/
- Patellar tendinopathy overview: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10541843/
- In-season management of patellar tendinopathy, scoping review: https://www.sciencedirect.com/science/article/abs/pii/S1466853X22000426
- Isometric neck strength in rugby union: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9031103/

Sport-specific
- Blagrove, Howatson and Hayes 2018, strength training and distance running: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5889786/
- Rønnestad and Mujika 2014, strength training for running and cycling: https://pubmed.ncbi.nlm.nih.gov/23914932/
- Heavy strength training in endurance cyclists, meta-analysis: https://pmc.ncbi.nlm.nih.gov/articles/PMC12881108/
- Exercise-based prevention in endurance runners, Sports Med 2024: https://link.springer.com/article/10.1007/s40279-024-01993-7
- Hamstring strain injuries, Strength Cond J 2020: https://journals.lww.com/nsca-scj/fulltext/2020/06000/hamstring_strain_injuries__incidence,_mechanisms,.5.aspx
- Prevention and rehabilitation of the athletic hamstring injury: https://pmc.ncbi.nlm.nih.gov/articles/PMC12034042/
- Sprint training for hamstring injury prevention in soccer: https://pmc.ncbi.nlm.nih.gov/articles/PMC11126098/
- Hamstring EMG, sprinting vs strengthening exercises: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11378697/
- Miro, vanSonnenberg, Sabb and Schöffl 2021, finger flexor pulley injuries: https://pubmed.ncbi.nlm.nih.gov/33966972/
- Overuse injury risk factors and prevention in adult climbers: https://pmc.ncbi.nlm.nih.gov/articles/PMC10756908/
- Physical and physiological profiles of BJJ athletes: https://link.springer.com/article/10.1186/s40798-016-0069-5
- BJJ injury prevalence literature review: https://thesportjournal.org/article/injury-prevalence-in-brazilian-jiu-jitsu-and-mitigation-strategies-for-brazilian-jiu-jitsu-practitioners-and-instructors-a-literature-review/
- Risk factors and prevention in high-performance tennis players, 2025: https://pmc.ncbi.nlm.nih.gov/articles/PMC12568103/
- Contact load in rugby union, Front Physiol 2025: https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2025.1672824/full
- Physical demands and workload management in American football, Sports Med 2017: https://link.springer.com/article/10.1007/s40279-017-0783-2
- Low back pain and golf, biomechanical risk factors: https://pmc.ncbi.nlm.nih.gov/articles/PMC9219256/
- Aasa et al. 2017, injuries in weightlifting and powerlifting: https://pubmed.ncbi.nlm.nih.gov/27328853/
- CrossFit musculoskeletal injuries, meta-analysis: https://www.germanjournalsportsmedicine.com/archive/archive-2021/issue-7/musculoskeletal-injuries-in-crossfitr-a-systematic-review-and-meta-analysis-of-injury-rates-and-locations/
- Injury in CrossFit, epidemiology and risk factors: https://pubmed.ncbi.nlm.nih.gov/33322981/
- Esports pain prevalence, systematic review and meta-analysis: https://link.springer.com/article/10.1186/s40798-025-00971-1
- Musculoskeletal pain in esports players, clinical implications: https://www.tandfonline.com/doi/full/10.1080/15438627.2025.2594401

Populations
- Lloyd et al. 2016, NSCA Position Statement on Long-Term Athletic Development: https://www.nsca.com/globalassets/about/position-statements/nsca_position_statement_long-term_athletic_development.pdf
- NSCA on LTAD, youth resistance training and early specialisation: https://www.nsca.com/about-us/position-statements/youth-training-and-long-term-athletic-development/ltad-youth-resistance-training-and-early-sport-specialization-what-it-all-means/
- Fragala et al. 2019, NSCA Resistance Training for Older Adults position statement: https://journals.lww.com/nsca-jscr/fulltext/2019/08000/resistance_training_for_older_adults__position.1.aspx
- Recovery from resistance exercise in older adults, Sports Med Open 2023: https://sportsmedicine-open.springeropen.com/articles/10.1186/s40798-023-00597-1
- 2023 IOC consensus statement on REDs: https://stillmed.olympics.com/media/Documents/Athletes/Medical-Scientific/Consensus-Statements/REDs/BJSM-IOC-consensus-statement-on-Relative-Energy-Deficiency-in-Sport-REDs.pdf
- IOC REDs announcement: https://www.olympics.com/ioc/news/ioc-publishes-new-consensus-statement-on-relative-energy-deficiency-in-sport-reds-to-protect-athlete-health
- ACSM Expert Consensus Statement on Weight Loss in Weight-Category Sports: https://researchonline.ljmu.ac.uk/id/eprint/17789/1/ACSM%20Consensus%20Statement%20Weight%20Making.pdf
- ISSN position stand, weight cut strategies for MMA and combat sports: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11894756/
- Prevalence of rapid weight loss in Olympic style wrestlers: https://pmc.ncbi.nlm.nih.gov/articles/PMC9559051/
- Disturbing weight cutting behaviors in young combat sports athletes: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8863958/

---

## Appendix B: additional sports

Added 2026-08-31, closing four of the gaps flagged in section 11: baseball and
softball, rowing, triathlon, team handball. Same template as section 6:
qualities, energy systems, injury hotspots, prevention, primary lifts,
accessory emphasis, conditioning, what to avoid, sample in-season and
off-season week.

### B.1 Baseball and softball

- **Qualities.** Rotational power, hip-shoulder separation, single-leg push-off
  strength, scapular control, arm speed. Softball's windmill pitch is a
  different motion from baseball's overhand throw, but both load the throwing
  shoulder and elbow heavily and repeatedly.
- **Energy.** Phosphagen for any single pitch, throw or swing. The game itself
  sits in a long, mostly low-intensity aerobic frame with intermittent maximal
  bursts.
- **Injury hotspots.** Baseball: UCL (elbow) and shoulder in pitchers, driven
  by pitch volume. Elbow and forearm injury rates in high school baseball and
  softball players have risen since the mid-2000s even as overall injury rates
  fell.
  [Epidemiological trends of elbow and forearm injuries in high school baseball and softball players, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12277728/)
  Softball: windmill pitching produces shoulder distraction stress and elbow
  compressive forces comparable to baseball overhand pitching, concentrated on
  the biceps-labrum complex.
  [Biomechanics of windmill softball pitching and shoulder/elbow injury mechanisms](https://pubmed.ncbi.nlm.nih.gov/15722291/)
  UNVERIFIED: a commonly repeated figure that youth pitchers throwing over 100
  innings a year are 3.5x more likely to be injured traces back to Fleisig et
  al.'s pitcher survey work; I did not fetch that primary paper within the
  timebox. Treat the multiplier as directionally right, not as a confirmed
  number.
- **Prevention.** Two pieces, both load-bearing. First, cap throwing volume:
  MLB and USA Baseball's Pitch Smart sets daily pitch-count limits by age
  (85 pitches for ages 11-12, 95 for 13-16, 105 for 17-18) and mandatory rest
  days that scale with pitches thrown (for ages 15-18: 0 days rest at 1-30
  pitches, up to 4+ days rest above 80), plus no pitching on three consecutive
  calendar days and 4 months off pitching per year for anyone 18 or under.
  [MLB / USA Baseball Pitch Smart guidelines, summarised](https://www.usabaseball.com/news/mlb-usa-baseball-announce-updates-to-pitch-smart-program-251090688)
  Second, run the arm-care program: the Thrower's Ten, developed by Kevin Wilk
  and James Andrews from ASMI EMG research, targets the rotator cuff and
  scapular stabilisers with 10-15 reps per exercise, 3-4 times a week in
  season, never immediately before an outing. A youth variant exists for
  athletes without full pain-free range of motion yet.
  [The Thrower's Ten Program, clinical reference](https://www.jagpt.com/blog/the-throwers-ten-program-a-clinical-reference-guide-for-physical-therapists-and-athletic-trainers/),
  [Youth Thrower's Ten variant, IJSPT](https://ijspt.scholasticahq.com/article/29923-the-youth-throwers-ten-exercise-program-a-variation-of-an-exercise-series-for-enhanced-dynamic-shoulder-control-in-the-youth-overhead-throwing-athlet)
  For softball, apply the same cuff and scapular work, plus core and hip/lower
  body strength to reduce reliance on the arm alone, and coach fatigue
  recognition since mechanics break down before pain does.
- **Primary lifts.** Trap bar deadlift, front squat, split squat, single-arm
  row or weighted pull-up, landmine or med ball rotational throw.
- **Accessory.** Thrower's Ten block (external rotation, scapular retraction,
  serratus, forearm and wrist flexor-pronator work), hip and core
  anti-rotation, single-leg stability for the push-off leg.
- **Conditioning.** Short sprint and agility work. The game does not demand a
  large aerobic base; do not add distance running.
- **Avoid.** Exceeding Pitch Smart counts and rest days. Pitching for multiple
  teams in the same window (showcase and travel-ball overlap is a known
  overuse driver, out of the trainer's control but worth asking about).
  High-volume overhead pressing stacked on top of high throwing volume.
  Skipping the arm-care block because the athlete "feels fine."
- **In-season week.** 1 to 2 short gym sessions, placed away from pitching or
  hard-throwing days. Thrower's Ten 3 to 4x/week, never right before an
  outing. Trap bar 3x4, split squat 2x6/side, rotational med ball throw 3x5.
- **Off-season week.** 3 to 4 sessions. Build max strength and rotational
  power first; arm-care work continues year-round at lower frequency, not
  zero.

### B.2 Rowing

- **Qualities.** High aerobic power, leg-drive force, trunk endurance under
  repeated spinal loading, technical consistency as fatigue rises.
- **Energy.** A 2000 m race runs roughly 5.5 to 7.5 minutes: heavy glycolytic
  plus aerobic effort. Training volume is mostly oxidative, long steady-state
  pieces with periodic threshold and sprint work.
- **Injury hotspots.** Low back pain is the dominant complaint. Prior back
  pain history and high ergometer training volume are the most consistent risk
  factors; rowers with low back pain show excessive erector spinae and
  latissimus dorsi activity and more spinal flexion at the catch and finish,
  worse under fatigue.
  [Risk factors associated with low back pain in rowers, systematic review and meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC12218018/),
  [Trunk muscle activities during ergometer rowing in rowers with and without low back pain](https://pmc.ncbi.nlm.nih.gov/articles/PMC10245001/)
  Secondary hotspots: rib stress fracture, knee (patellofemoral), and wrist or
  forearm overuse from the drive-recovery cycle.
- **Prevention.** Trunk extensor endurance work, since extensor endurance is
  specifically protective of the back under rowing loads.
  [World Rowing, guide for managing low back pain in rowers](https://worldrowing.com/2021/05/11/guide-for-managing-low-back-pain-in-rowers/)
  Technique correction so spinal flexion does not creep in at the catch or
  finish, especially late in a piece. A pilot trial of perturbation-based
  trunk stabilisation training in elite rowers reduced disability scores and
  improved trunk function; treat as promising, not yet the standard.
  [Perturbation-based trunk stabilization training in elite rowers, pilot study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9119454/)
  Progress erg volume gradually rather than in large jumps, the same 10%
  caution from section 4.
- **Primary lifts.** Trap bar deadlift or conventional deadlift, front squat,
  single-arm row, weighted pull-up, leg press.
- **Accessory.** Trunk extensor endurance (back extensions, prone holds,
  loaded carries), scapular control, forearm and grip endurance.
- **Conditioning.** On the erg or water. The sport already delivers the
  aerobic base; the gym does not need to repeat it.
- **Avoid.** Loaded spinal flexion work (rounded-back good mornings or RDLs)
  in anyone with a low back pain history. Stacking a heavy lift session
  immediately before or after a long erg piece without spacing.
- **Note.** Rowing is one of the sports, alongside cycling, where concurrent
  training interferes with strength gains less than running does, which makes
  heavier lifting more affordable here than in run-dominant sports.
  [Wilson et al. 2012, concurrent training meta-analysis](https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx)
- **In-season week.** 1 to 2 sessions. Trap bar deadlift 3x4, single-arm row
  3x8, trunk extensor endurance work every session, technique cueing built
  into warm-up.
- **Off-season week.** 3 to 4 sessions with a real hypertrophy and max
  strength block. Like cycling, this is the affordable window for building
  muscle before the interference cost of high rowing volume returns.

### B.3 Triathlon

- **Qualities.** Aerobic capacity and economy across three disciplines,
  tissue capacity to absorb high combined weekly volume, and the
  neuromuscular skill of running well on fatigued "brick" legs after cycling.
- **Energy.** Oxidative dominant. Event length ranges from about an hour
  (sprint distance) to 8 to 17 hours (Ironman distance); training volume is
  overwhelmingly aerobic with some threshold and VO2max work layered in.
- **Injury hotspots.** Running carries the largest injury burden of the three
  disciplines: Achilles, ITB, patellofemoral pain, tibial stress injury. Swim
  volume adds shoulder overuse; the aerodynamic cycling position adds low back
  and neck load.
  [Training and Competition Readiness in Triathlon, Sports 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6571715/),
  [Applying a Holistic Injury Prevention Approach to Elite Triathletes](https://pmc.ncbi.nlm.nih.gov/articles/PMC11359884/)
- **Prevention.** Individualised periodisation across all three disciplines at
  once, because loads are not simply additive: each discipline's training
  stress can mask a combined systemic overload the athlete does not feel
  until it is an injury. USA Triathlon's own injury-prevention guidance
  emphasises total-body strength integration (squat, hinge, lunge, push,
  pull, jump patterns together) and cross-training variety alongside the
  three core disciplines.
  [USA Triathlon, injury prevention checklist](https://www.usatriathlon.org/training-tips/your-injury-prevention-checklist)
- **Primary lifts.** Trap bar deadlift or back squat, single-leg RDL, hip
  thrust, pull-up or row for swim and aero-position posture. Two full-body
  sessions a week, kept low volume.
- **Accessory.** Hip abductor and calf and tendon work for running, cuff and
  scapular work for swimming, anti-flexion core for the aero position.
- **Conditioning.** The three disciplines are the conditioning. Concurrent
  training interference is real here, and running specifically is the
  discipline that most degrades strength and hypertrophy gains, more than
  cycling or swimming do.
  [Wilson et al. 2012](https://journals.lww.com/nsca-jscr/fulltext/2012/08000/concurrent_training__a_meta_analysis_examining.35.aspx)
- **Avoid.** Applying a per-discipline 10% progression rule to each sport
  separately while ignoring total combined load across all three. Heavy leg
  lifting the day before a key run session. Treating triathlon injury
  prevention as three separate single-sport problems rather than one combined
  load problem.
- **In-season / race-build week.** 1 to 2 short full-body sessions. Trap bar
  or squat 3x4, single-leg RDL 2x6/side, hip thrust 3x5, calf raise 3x8. Kept
  light enough to never compromise the next hard swim, bike or run session.
- **Off-season week.** 2 to 3 sessions with more volume, addressing whichever
  discipline or muscle group is weakest, usually general upper body strength.
  This is the window before combined multi-discipline volume climbs again.

### B.4 Team handball

- **Qualities.** Repeat jump and throw power, rotational throwing velocity,
  change of direction, collision tolerance. Shares the overhead-throwing
  shoulder demand with baseball and softball, on top of a contact team-sport
  profile.
- **Energy.** Intermittent, two 30-minute halves, glycolytic efforts inside an
  aerobic frame, closer to basketball and soccer than to baseball in overall
  match demand.
- **Injury hotspots.** Shoulder overuse from throwing volume is the
  distinguishing hotspot among overhead-throwing team sports. ACL and other
  knee injury from jumping and cutting, plus ankle sprain, round out the
  profile.
- **Prevention.** The OSTRC Shoulder Injury Prevention Programme, tested in a
  cluster-randomised trial of 660 elite handball players (45 teams, one
  season), delivered by coaches and captains 3 times a week as part of the
  warm-up. It targets glenohumeral internal and external rotation, scapular
  muscle strength, kinetic chain and thoracic mobility. Result: 28% lower risk
  of shoulder problems (OR 0.72, 95% CI 0.52-0.98) and a 22% lower risk of
  substantial shoulder problems.
  [Andersson et al. 2017, BJSM, preventing overuse shoulder injuries in 660 elite handball players](https://ostrc.no/globalassets/publications/andersson_2016_bjsm_preventing-overuse-shoulder-injuries-among-throwing-athletes.pdf)
  Pair it with a knee/ACL programme (Sportsmetrics or PEP, section 5) given
  the jumping and cutting load.
- **Primary lifts.** Trap bar deadlift, front squat, split squat, hip thrust,
  single-arm row, landmine or med ball rotational throw.
- **Accessory.** The OSTRC cuff and scapular circuit itself, Nordic curl for
  the jumping and cutting demand, anti-rotation core.
- **Conditioning.** The sport provides most of it. Add short high-intensity
  intervals only if match minutes are low.
- **Avoid.** Skipping the OSTRC warm-up block. Compliance is the lever: the
  programme only works if it runs 3x/week, not sporadically. Adding gym
  throwing-volume drills on top of practice and match throwing.
- **In-season week.** 1 to 2 gym sessions, plus the OSTRC programme 3x/week
  built into the warm-up on practice and match days. Trap bar 3x4, split
  squat 2x6/side, cuff and scapular circuit.
- **Off-season week.** 3 to 4 sessions: max strength and jump-capacity block,
  rotational throwing power added progressively. Keep the OSTRC programme
  running year-round, not just in season.
