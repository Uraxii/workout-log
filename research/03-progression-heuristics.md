# Progression and regression heuristics for a workout-log agent

Research slice B. Compiled 2026-08-31.

Scope: rules an agent can apply to a training log to decide **increase**, **hold**, **decrease**, or **deload**. Every rule below is written as an IF/THEN plus the log fields it reads.

Sibling slices cover the data model, routines and UX, existing tools, and trainer-agent behaviour. Those are not covered here.

---

## TL;DR: recommended default rule set

For a lifter running preset routines in this app, the default engine should be **double progression, capped by RPE, with failure-triggered deloads**. It is the most forgiving scheme, works on barbells, dumbbells, machines, and bodyweight, and needs only three fields per set.

| # | Rule | Numbers |
|---|---|---|
| 1 | Every exercise has a rep range and a load step | e.g. 6-10 reps, step = 2.5 kg barbell / 2 kg dumbbell pair / 1 pin machine |
| 2 | **Increase** when all prescribed sets hit the top of the range | all sets at top rep count, last set RPE <= 9, then +1 step and drop back to bottom of range |
| 3 | **Hold** while any set is below the top of range | add 1 rep to the weakest set next session |
| 4 | **RPE cap** overrides increase | if last-set RPE >= 9.5 (0-0.5 reps in reserve) two sessions running, hold even if reps qualify |
| 5 | **Decrease** on repeat failure | miss the bottom of the rep range on the same exercise 2 sessions in a row, or 3 non-consecutive in 4, then -10% load, rebuild |
| 6 | **Deload** on stall or schedule | no e1RM PR in 3 weeks on that lift, or every 4-8 weeks preplanned. Cut volume 30-50%, load 10-20%, for 5-7 days |
| 7 | **Time off** adjustment | 1-2 weeks off: resume at 100%, expect a slower session. 3-4 weeks: -10%. Over 4 weeks: -20% and rebuild over 2-3 weeks |
| 8 | **Pain flag** always wins | user marks pain, then stop progressing that exercise, offer a variation, refer to a professional |

Step size guard: if one load step is more than about 5% of the current working weight, prefer adding reps first, or use a smaller step (fractional plates, dumbbell half-steps). This is a derived rule, see [Increment sizing](#increment-sizing-when-the-jump-is-too-big).

Sources for each number are in the sections below.

---

## How to read the rules

Every rule names the log fields it needs. The minimum field set across all schemes:

| Field | Type | Used by |
|---|---|---|
| `exercise_id` | id | everything |
| `date` / `session_id` | timestamp | streaks, time-off, stall windows |
| `set.weight` | kg or lb | everything except pure bodyweight |
| `set.reps` | int | everything |
| `set.target_reps` | int | linear progression, double progression, failure detection |
| `set.rpe` or `set.rir` | 6-10 / 0-4 | autoregulation, RPE cap, e1RM |
| `set.is_amrap` | bool | Greyskull, 5/3/1, nSuns, GZCLP, RP T3 |
| `set.completed` vs prescribed | bool | failure counting |
| `exercise.rep_range` | (min, max) | double progression |
| `exercise.load_step` | number | all increase rules |
| `exercise.training_max` | number | 5/3/1, nSuns |
| `session.flags` | pain, illness, poor sleep | regression, refer to professional |
| `weekly_sets_per_muscle` | int | RP volume landmarks |
| derived `e1RM` | number | plateau detection, RPE autoregulation |

Derived value used repeatedly: **estimated 1RM (e1RM)**. Two common forms.

- Epley: `1RM = w * (1 + reps/30)`.
- From RPE, look up the reps-by-RPE percentage table (Tuchscherer), e.g. 5 reps at RPE 8 is 81.1% of 1RM, so `e1RM = w / 0.811`. Table: <https://fitnessvolt.com/rpe-training/rpe-chart/>

A 2026 preprint fits a weight-dependent 1RM equation on 303,494 near-failure sets across 388 exercises and reports better accuracy than Epley or Brzycki, especially at high rep counts. Worth reading before picking a formula. UNVERIFIED, preprint, not peer reviewed: <https://arxiv.org/pdf/2603.17495>

---

## 1. Linear progression: Starting Strength

Suits: true beginners, first 3-9 months of barbell training.

**Rule.** IF all prescribed sets and reps were completed last session, THEN add the fixed increment for that lift next session.

| Lift | Increment per session |
|---|---|
| Squat | 5 lb |
| Bench press, overhead press, power clean | 2.5 lb |
| Deadlift | 10 lb |

**Reset rule.** IF the lifter misses reps on the same lift in **three consecutive sessions**, THEN that lift is stalled. Drop the load by **10%** and run it back up with the same increments.

Data needed: `exercise_id`, `set.reps`, `set.target_reps`, `set.weight`, consecutive-session failure counter per lift.

Source: Starting Strength official programs page <https://startingstrength.com/get-started/programs>; increments and the three-miss 10% reset as summarised by Barbell Logic (a Starting Strength Coach affiliate) <https://barbell-logic.com/novice-linear-progression-explained/>

Caveat: the exact per-lift increments are stated in the book *Practical Programming for Strength Training*, which is not free online. The numbers above are consistent across Starting Strength affiliate sources but I could not fetch the book text. Treat the per-lift split as **well-corroborated, not primary-verified**.

---

## 2. Linear progression: StrongLifts 5x5

Suits: beginners, slightly more forgiving than Starting Strength because the deload is app-configurable.

**Rule.** IF all 5 sets of 5 reps were completed, THEN add the increment (default **5 lb**) next session.

**Deload rule.** IF the lifter fails to complete all sets on an exercise for **three sessions in a row**, THEN reduce the weight by **10%**.

Both numbers are user-configurable in the app. StrongLifts explicitly documents that you can set, for example, a 15% deload after 2 failed attempts.

Rationale StrongLifts gives for waiting for three failures: a single bad day (sleep, food, focus, form) is not evidence of a real stall.

Data needed: same as Starting Strength, plus per-exercise user settings for `increment` and `deload_pct` and `fail_threshold`.

Sources:
- <https://support.stronglifts.com/article/71-progression>
- <https://stronglifts.com/stronglifts-5x5/failure/>
- <https://stronglifts.com/stronglifts-5x5/plateaus/>

Design note for the app: StrongLifts making the failure threshold and deload percent user-editable is the right call. Hard-coding 3 and 10% will annoy anyone whose lift stalls for a different reason.

---

## 3. Greyskull LP (AMRAP-driven linear progression)

Suits: beginners and early intermediates who want the log to react to how the last set actually went.

Structure: last work set of each main lift is an AMRAP, target minimum 5 reps.

**Increase rules.**

| AMRAP reps on last set | Action next session |
|---|---|
| 5-9 | +1 standard increment |
| 10 or more | +2 standard increments (double jump) |
| below 5 | **reset that lift only**: -10% load, rebuild |

Only the stalled lift resets. Other lifts keep progressing on their own schedule.

Stopping rule for the AMRAP set itself: stop when you are sure the next rep would fail or break form. That is an RPE 9-9.5 stop, not a grinding failure set.

Data needed: `set.is_amrap`, `set.reps` on that set, `exercise.load_step`.

Sources: <https://www.powerliftingtowin.com/greyskull-lp/>, <https://liftvault.com/programs/strength/greyskull-linear-progression-spreadsheet/>

Caveat: the primary text is John Sheaffer's *Greyskull LP* book. Both sources above are secondary but detailed and consistent. Tagged **corroborated secondary**.

Why this one is a good default candidate for an agent: it needs exactly one number per exercise per session and produces a three-way decision with no configuration.

---

## 4. Double progression (rep range then load)

Suits: everyone past the pure-novice stage. The default recommendation in the TL;DR.

**Rule.** Pick a rep range. Hold the load until you can hit the top of the range on all prescribed sets. Then add load and drop back to the bottom of the range.

Nuckols states it as: within a rep range you keep the weight and add reps each week until you have mastered the weight. Training in a 5-8 range, you keep the load until you can do 9 reps, then go heavier next session, confident you can still get at least 5.

Weekly load add when the range is topped out: about **5-10 lb** on compounds, with reps expected to drop back toward the bottom of the range.

Sources:
- Nuckols, via the Muscle and Strength Pyramids site <https://muscleandstrengthpyramids.com/counting-training-volume-greg-nuckols/>
- Nuckols beginner program description <https://www.boostcamp.app/coaches/greg-nuckols/greg-nuckols-beginner-program>

**Variant: sets-across vs top-set.** Two definitions of "hit the top of the range" exist and they behave differently.

| Variant | Increase trigger | Effect |
|---|---|---|
| Strict (all sets) | every prescribed set reaches the top rep | slowest, safest, best for the agent's default |
| Loose (first set) | the first work set reaches the top rep | faster, more stalls |
| Total reps | sum of reps across sets reaches a threshold | good for machines and accessories where set-by-set noise is high |

Recommendation: default to strict, expose the total-reps variant for accessories.

Data needed: `exercise.rep_range`, all `set.reps` in the session, `exercise.load_step`.

Helms' Muscle and Strength Pyramid pairs double progression with an RIR cap so the top of the range is not reached by grinding. See the RPE section below.

---

## 5. 5/3/1 (Wendler)

Suits: intermediates. Needs a training max concept in the data model.

**Training max (TM).** Wendler's own words on his site: "The 90% rule was the recommended starting point, Beyond 5/3/1 may mention 85% or 80% or whatever but the bottom line is you manipulate your TM based on current training goals, current programming, current level of strength." And: "There is no hard rule for your TM. In my opinion the more progress you can achieve out of a low TM the better."

Source, primary: <https://www.jimwendler.com/blogs/jimwendler-com/101082310-the-training-max-what-you-need-to-know>

That is important for the agent. **Do not treat TM = 90% of 1RM as a law.** Treat it as the default seed with a user override, and bias low.

**Per-cycle TM increase.** After each 3-week cycle: **+5 lb** upper body lifts (bench, press), **+10 lb** lower body lifts (squat, deadlift). This is the classic 5/3/1 increment. UNVERIFIED against the book text, but consistent across every secondary source checked, e.g. <https://barbend.com/5-3-1-program/>

**Deload cadence.** Originally week 4 of every 4-week cycle. Wendler revised this in *Beyond 5/3/1* to a deload every **7 weeks**, i.e. after two 3-week cycles. Source: <https://liftvault.com/resources/531-glossary/>

**7th week protocol (5/3/1 Forever).** A dedicated week that is one of three things: a light deload, a PR attempt, or a **TM test**. The TM test checks whether the current TM is still correct. The stated goal is to keep the TM at roughly **85-90%** of true current strength at all times: a 5-rep max is usually about 85% of 1RM and a 3-rep max about 90%.

Practical agent form of the TM test: perform 5 reps at the current TM. If 5 reps move cleanly, the TM is still valid or low. If you cannot get 5, the TM is too high.

Source: <https://liftvault.com/resources/531-glossary/>, <https://t-nation.com/t/training-max-test-7th-week-protocol/272846>

**Reset rules.** Two documented approaches.

| Approach | Rule |
|---|---|
| 5 forward, 3 back | run 5 cycles, then reset the TM to what it was 3 cycles ago |
| 7th week TM test | test, then set TM to 85-90% of the fresh max |
| Stall reset | when a lift stalls (AMRAP set falls to the prescribed minimum reps or below), cut that lift's TM by about **10%** and rebuild |

Wendler also recommends resetting proactively after 5-7 cycles even without a stall. Source: <https://train531.com/blog/breaking-plateaus-when-to-reset-your-531-training-max/> (secondary, tagged **UNVERIFIED** for the "5-7 cycles" number).

Data needed: `exercise.training_max`, cycle counter, week-in-cycle, AMRAP reps per week, per-lift TM history.

---

## 6. GZCLP and the GZCL tier method

Suits: late beginners and early intermediates. The most agent-friendly failure ladder of any scheme here, because failing does not immediately cost you load.

Primary community documentation: <https://thefitness.wiki/routines/gzclp/> (the r/fitness wiki version, closest thing to canonical for GZCLP; Cody Lefever's original GZCL blog is the source of the tier method).

### T1: heavy compound

| Stage | Scheme |
|---|---|
| 1 | 5x3+ (last set AMRAP) |
| 2 | 6x2+ |
| 3 | 10x1+ |

**Increase rule.** IF all prescribed reps completed, THEN add **5 lb** (bench, overhead press) or **10 lb** (squat, deadlift) next session.

**Failure rule.** IF you fail to complete the total prescribed reps, THEN move to the next stage at the same or next load, do not deload yet.

**Reset rule.** IF you fail stage 3 (10x1+), THEN test a new 5-rep max and restart stage 1 at **85%** of that 5RM.

### T2: secondary compound

| Stage | Scheme |
|---|---|
| 1 | 3x10 |
| 2 | 3x8 |
| 3 | 3x6 |

On completing the stage 3 cycle, restart at stage 1 with **+15-20 lb** over the previous stage-1 starting load.

### T3: accessory

Scheme 3x15+ (last set AMRAP). **Increase rule:** add weight when the AMRAP set reaches **25 reps**.

Data needed: `exercise.tier`, `exercise.stage`, all `set.reps`, `set.is_amrap`, a per-exercise 5RM history for the reset.

Why this matters for the app: the stage ladder is a **hold before decrease** mechanism. Most other schemes go straight from "hit reps" to "missed reps, deload". GZCLP inserts two cheap intermediate steps that extract more work from the same bar weight. Worth stealing for the default engine even if you never ship GZCLP itself.

---

## 7. RPE / RIR autoregulation

Suits: intermediate and advanced. Explicitly **not** reliable for novices, see the accuracy caveat.

### The scale

Zourdos et al. 2016 introduced the resistance-training-specific RPE anchored to repetitions in reserve. RPE 10 = 0 RIR, RPE 9 = 1 RIR, RPE 8 = 2 RIR, and so on.

Primary: Zourdos MC et al., "Novel Resistance Training-Specific Rating of Perceived Exertion Scale Measuring Repetitions in Reserve", *J Strength Cond Res* 30(1), 2016. <https://journals.lww.com/nsca-jscr/fulltext/2016/01000/novel_resistance_training_specific_rating_of.31.aspx>

Application paper: Helms ER, Cronin J, Storey A, Zourdos MC, "Application of the Repetitions in Reserve-Based Rating of Perceived Exertion Scale for Resistance Training", *Strength Cond J*, Aug 2016. <https://journals.lww.com/nsca-scj/fulltext/2016/08000/application_of_the_repetitions_in_reserve_based.10.aspx> and open access <https://pmc.ncbi.nlm.nih.gov/articles/PMC4961270/>

### Experience-level caveat, load-bearing for the agent

Zourdos 2016 compared experienced squatters (training age 5.2 +/- 3.5 years, n=15) against novices (0.4 +/- 0.6 years, n=14). Experienced lifters gave more accurate RPE at 1RM (9.80 +/- 0.18 vs 8.96 +/- 0.43, p = 0.023). Novices systematically **under-rate** how hard a maximal set was.

**Agent implication.** IF `user.training_age < 1 year`, THEN do not gate progression on self-reported RPE. Use reps and completion only, and treat RPE as a soft signal for logging, not a decision input. Revisit once the user has 6-12 months of logs.

### Autoregulation rules

**Load selection.** IF the target is "top set of 5 at RPE 8", THEN pick the load so the set finishes with 2 reps left. If the actual RPE comes in above target, the next set or session load comes down.

**Load correction size.** On the Tuchscherer reps-by-RPE table, one RPE point at a fixed rep count is worth roughly **2-3% of 1RM** (e.g. 5 reps at RPE 8 = 81.1% of 1RM). So overshooting the target RPE by 1 means the load was about 2-3% too heavy, and by 2 means about 4-6% too heavy. **DERIVED from the table, not a stated rule.** Table: <https://fitnessvolt.com/rpe-training/rpe-chart/>

The widely repeated "drop 5% per RPE point over target" heuristic is close enough at low rep counts and errs on the safe side. I could not find it stated in a primary RTS source. Tag it **UNVERIFIED** if you ship it.

**RTS fatigue percents (volume autoregulation).** Work up to a top set at the prescribed reps and RPE, compute the daily e1RM, then do back-off sets with a reduced load until e1RM would have dropped by the prescribed fatigue percent. Example given by RTS: if daily e1RM is 100 kg and you want 5% fatigue, you work until your e1RM would read 95 kg, then stop.

Sources: <https://store.reactivetrainingsystems.com/blogs/advanced-concepts/fatigue-percents-revisited>, <https://articles.reactivetrainingsystems.com/2016/12/29/auto-regulating-volume/>, review at <https://www.powerliftingtowin.com/autoregulation/>

**RPE vs percentage loading, does it matter?** Helms et al. 2018 compared RPE-based and %1RM loading in periodized programs matched for sets and reps. Open access: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5877330/> Use it if a source conflict needs arbitration.

Data needed: `set.rpe`, `set.reps`, `set.weight`, `user.training_age`, derived per-session e1RM.

---

## 8. Renaissance Periodization volume landmarks (Israetel)

Suits: hypertrophy-focused intermediates. This is a **volume** progression scheme, not a load progression scheme. It answers "how many sets", not "how much weight".

### Landmarks, per muscle group per week

| Landmark | Meaning |
|---|---|
| MV | maintenance volume, holds size, does not grow |
| MEV | minimum effective volume, the floor that grows |
| MAV | maximum adaptive volume, where growth is fastest |
| MRV | maximum recoverable volume, the ceiling |

**Mesocycle rule.** Start the block at MEV. Add **1-2 sets per muscle per week**. Pass through MAV. Reach near MRV. Then deload back toward MV and start the next block. Typical worked example: 12 sets/week at MEV, 16-18 at MAV, 20-22 near MRV.

Source: <https://arvo.guru/resources/methods/rp-training> (secondary but numerically explicit); Israetel's own MRV guest post <https://propanefitness.com/maximum-recoverable-volume/>

**Deload trigger.** You know you have exceeded MRV when you **underperform in the current microcycle compared to the previous one**. A performance drop from one week to the next is the signal. Same source.

Other stated triggers in RP material: sustained excessive soreness, joint pain, motivation drop, and sleep disruption. Joint pain in particular should route to the pain flag path, not to a load prescription. **Refer to a professional.**

**Deload execution.** Israetel's version: roughly **half of week 1's set count**, all sets taken much further from failure than normal, often with reduced load too. Source: <https://teamfullrom.com/blogs/news/hypertrophy-training-periodization> (secondary, paraphrasing Israetel; the exact "half sets, half load, two thirds reps" formulation is often quoted but I could not find it stated primary. Tag **UNVERIFIED**.)

**Volume evidence base.** Schoenfeld, Ogborn, Krieger 2017 meta-regression: a graded dose-response between weekly sets and hypertrophy, each additional weekly set associated with an effect size increase of 0.023, about 0.37% extra gain. 34 treatment groups from 15 studies. <https://pubmed.ncbi.nlm.nih.gov/27433992/>

**The 2026 update, read 2026-09-01.** Pelland, Remmert, Robinson, Hinson and
Zourdos, "The Resistance Training Dose Response: Meta-Regressions Exploring the
Effects of Weekly Volume and Frequency on Muscle Hypertrophy and Strength
Gains", *Sports Med* 2026;56(2):481-505,
[doi:10.1007/s40279-025-02344-w](https://doi.org/10.1007/s40279-025-02344-w),
[PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/). Captured in `.kb`
(`llmwiki search "resistance training volume dose response meta-regression"`).
67 studies, 2,058 participants, 79.1% male, mean age 25.2 ± 5.2. Bayesian
multi-level meta-regressions adjusted for intervention duration and training
status.

Four findings that matter here:

1. **Volume raises both hypertrophy and strength.** Posterior probability that
   the marginal slope exceeds zero: **100% for both outcomes**. No threshold, no
   inversion, no point where more sets started to hurt.
2. **Diminishing returns, and they bite strength much harder than hypertrophy.**
   Both best-fit models curve over. The paper does not identify a ceiling in
   either, only a flattening.
3. **Frequency is a strength variable, not a hypertrophy variable.** Posterior
   probability for frequency's effect on hypertrophy was below 100%, which the
   authors read as compatible with negligible effects. For strength it was 100%,
   again with diminishing returns. Matching the total-volume argument: spread
   sets across days for strength, and for hypertrophy do whatever gets the sets
   done.
4. **Fractional set counting won.** Sets were classified direct or indirect
   relative to the measured muscle, and indirect sets counted three ways: 1.0
   ('total'), 0.5 ('fractional'), 0.0 ('direct'). **The 0.5 'fractional' method
   had the strongest relative evidence**, so the authors used it for the primary
   models.

**Verdict on the 10-to-20 sets per muscle per week band: it does not move, but
its top end changes meaning.** The floor stays where ACSM 2026 put it, ~10 sets.
The 20 is *not* an evidence-based optimum and this paper gives no ground for
treating it as one — the dose-response is still climbing at the top of the
studied range. Twenty is a **recovery and adherence ceiling**, which is exactly
what RP's MRV vocabulary already says (section 8). Keep the band, keep
progressing upward within it, and stop calling the upper number an optimum.

**Read the fractional finding into `02-data-model.md` §9.** That note derives
`sets per muscle per week` as 1.0 per primary muscle and 0.5 per secondary, and
tags the 0.5 "a convention, UNVERIFIED". Pelland is a source for it: the same
0.5 weighting, chosen on evidence, in the largest meta-regression on the
question. Retire that tag.

Limit: only the abstract was read. *Sports Med* is paywalled at Springer, so
there is no per-set effect size from this paper to set against Schoenfeld's
0.023. Data and code are on OSF (<https://osf.io/6z3xu>) if a number is needed.

Data needed: `weekly_sets_per_muscle` derived from exercise-to-muscle mapping, week-over-week performance comparison per exercise, soreness and joint-pain flags.

Note: mapping exercises to muscle groups is a data-model problem, so this rule depends on slice A landing that mapping.

---

## 9. nSuns 5/3/1 LP

Suits: intermediates with time. Highest-frequency AMRAP-driven progression in common use.

**Rule.** The TM increase for the next week is set by the reps achieved on that day's first AMRAP set.

| AMRAP reps | TM change |
|---|---|
| 0-1 | no increase (consider a decrease) |
| 2-3 | +5 lb |
| 4-5 | +5 to 10 lb |
| 6 or more | +10 to 15 lb |

TM starts at **90% of true 1RM**.

Sources: <https://liftvault.com/programs/powerlifting/n-suns-lifting-spreadsheets/>, <https://muscleevo.net/nsuns-program/>

Data needed: `exercise.training_max`, first `set.is_amrap` reps of the week per lift.

This table is the cleanest existing template for "AMRAP reps map to a load delta". If you build one generic AMRAP progression rule for the app, model it on this shape and let the thresholds be per-exercise config.

---

## 10. Madcow 5x5 and the Texas Method

Suits: intermediates who have exhausted session-to-session linear progression.

**Madcow weekly rule.** Ramping sets to one top set of 5 per week. Every week all working weights increase by **2.5%**. Typically run 8-12 weeks until stall. Heavy / light / medium weekly rotation.

Sources: <https://www.strengthlog.com/madcow-5x5/>, <https://www.powerliftingtowin.com/madcows-5x5/>, <https://powerliftingtechnique.com/texas-method-vs-madcow-5x5/>

**Texas Method weekly rule.** Volume day (5x5 at the same weight, Monday), recovery day (light, Wednesday), intensity day (new 5-rep max, Friday). Progression is a weekly 5RM PR on intensity day rather than a fixed percentage.

Same sources.

**Reset rule.** Both programs: when the weekly PR stalls, reset back roughly 4-6 weeks of progress and run the ramp again. UNVERIFIED as a stated number; Madcow's own writing describes restarting the ramp rather than giving a fixed percentage.

Key data-model consequence: these are the first schemes here where **the progression unit is a week, not a session**. If the log's progression engine only compares session to session, it cannot express Madcow or Texas Method. Flag for slice A.

---

## 11. Bodyweight progression (r/bodyweightfitness Recommended Routine)

Suits: anyone without load, and any exercise where load steps are unavailable.

**Rule.** Perform the hardest variation of each movement you can do for **3 sets of 5-8**. Start at the variation you can do for 3x5 with good form. Add a rep per set each workout.

**Advance rule.** IF you hit **3x8** with good form, THEN move to the next harder progression and restart at **3x5**.

**Hold rule.** IF you cannot manage at least 3x5 at the new variation, THEN spend another **1-2 weeks** at the previous level first.

Sources: <https://redditbwf.github.io/wiki/recommended_routine.html>, mirror <https://gist.github.com/sgup/f10f1d57e54b7876495f4bafb6d697eb>

Data needed: `exercise.progression_chain` (ordered list of variations), `exercise.rep_range`, all `set.reps`.

This is double progression with the load axis replaced by an ordered variation list. If the data model treats "variation index" and "load" as the same abstract difficulty axis, one engine covers both. Worth telling slice A.

For loadable bodyweight movements (pull-ups, dips), the same rule applies with added weight as the third stage: reps to top of range, then add load, then when load steps get awkward, move to a harder variation.

---

## Increment sizing: when the jump is too big

This is where most beginner apps get it wrong, and where the agent can add real value.

**The problem.** The smallest common plate is 2.5 lb (1.25 kg), so the smallest barbell jump is 5 lb (2.5 kg). On a 200 lb squat that is 2.5%. On a 65 lb overhead press it is 7.7%. The same absolute jump is a rounding error on one lift and a wall on another.

**Equipment step sizes.**

| Equipment | Typical smallest step | Notes |
|---|---|---|
| Barbell, standard plates | 5 lb / 2.5 kg | one 2.5 lb / 1.25 kg plate per side |
| Barbell, fractional plates | 0.5-2 lb / 0.25-1 kg per side | 0.25 kg to 0.5 kg plates are the common range |
| Dumbbells, commercial rack | 5 lb / 2 kg per hand, i.e. 10 lb / 4 kg total | the total is what matters for progression |
| Dumbbells, adjustable | 2.5-5 lb per hand | |
| Selectorized machine | 1 pin, often 10-15 lb | some have half-pin add-ons |
| Cable stack | 1 pin, often 5-10 lb | |

Source on fractional plates and where to use them first (overhead press, bench, rows, curls, machines and cables where the fixed jump is disproportionately large): <https://www.serioussteel.com/blogs/news/fractional-plates-platemates-small-weight-increments-big-gains>, <https://www.tworepcave.com/17105/barbell-micro-weight-plate-solutions/>

**Derived rule (no primary source states a percentage threshold, tag DERIVED).**

```
jump_pct = load_step / current_working_weight

IF jump_pct <= 0.025  -> increase load normally
IF 0.025 < jump_pct <= 0.05 -> increase load, but expect reps to drop
                                to the bottom of the range
IF jump_pct > 0.05    -> prefer adding reps. Suggest a smaller step:
                         fractional plates, or hold the load and add a set.
```

Rationale for the 5% line: on the Tuchscherer table one rep is worth roughly 2-3% of 1RM, so a jump over about 5% costs about two reps, which will blow through most rep ranges in one session. **DERIVED, arguable, needs a decision from the user.**

**Agent behaviour this enables.** On a 40 lb dumbbell bench press where the next dumbbell is 45 lb (a 12.5% jump), the agent should say "add reps, you are not ready for the next dumbbell" rather than "increase the weight". That is the single most useful thing a progression engine can do that a paper log cannot.

---

## Cardio progression

Brief, per the brief.

**The 10% rule.** The traditional advice is to increase weekly running volume by no more than 10%. It has no primary research backing. A study of 5,200 runners found the weekly 10% rule predicts injury no better than chance.

**What replaced it.** An 18-month cohort study of over 5,200 runners in the *British Journal of Sports Medicine* found the risk is in **single-run spikes**, not weekly totals. A run exceeding **110% of the longest run in the previous 30 days** raised overuse injury risk by more than 64%. Larger spikes more than doubled it. Week-to-week mileage change and acute:chronic workload ratio predicted injuries poorly.

Sources: <https://runningmagazine.ca/sections/training/the-10-per-cent-mileage-rule-isnt-what-you-think-study-warns/>, <https://run.outsideonline.com/training/getting-started/myth-of-the-10-percent-rule/>. Related earlier work: Nielsen et al., "Excessive Progression in Weekly Running Distance and Risk of Running-Related Injuries", *JOSPT* 2014 <https://www.jospt.org/doi/10.2519/jospt.2014.5164>

**Agent rule.** Track `longest_single_run_last_30_days` per user. IF a planned run exceeds 110% of that, THEN warn. Do **not** gate on weekly mileage percentage, the evidence does not support it.

**Zone 2.** Progress duration first at a fixed intensity, then intensity. No specific numerical rule found from a primary source in the time available. **GAP, not researched.**

---

## Decrease, deload, and time-off rules

### Decrease (load reduction, single exercise)

| Trigger | Action | Source |
|---|---|---|
| Missed target reps on the same lift, 3 consecutive sessions | -10% on that lift | Starting Strength <https://barbell-logic.com/novice-linear-progression-explained/>, StrongLifts <https://support.stronglifts.com/article/71-progression> |
| AMRAP set falls below 5 reps (Greyskull) | -10% on that lift only | <https://www.powerliftingtowin.com/greyskull-lp/> |
| Failed all three GZCLP T1 stages | retest 5RM, restart at 85% of it | <https://thefitness.wiki/routines/gzclp/> |
| 5/3/1 lift stalls | -10% TM, or reset TM to 3 cycles ago | <https://train531.com/blog/breaking-plateaus-when-to-reset-your-531-training-max/> UNVERIFIED |
| Actual RPE exceeds target by >= 1 for 2 sessions running | -2.5% to -5% load | DERIVED from the Tuchscherer table <https://fitnessvolt.com/rpe-training/rpe-chart/> |
| e1RM trending down over 3+ weeks at the same rep target | deload, then rebuild | see plateau section |
| Pain flag on that exercise | stop progressing, swap variation, **refer to a professional** | not a training rule |

### Deload

**Preplanned cadence.** Every **4-8 weeks**. Duration **5-7 days**, extendable.

**Magnitude.** Volume reduction **30-50%**. Intensity reduction **10-20%**. Adjust to individual fatigue.

Source, the best evidence base available: Bell L et al., "A Practical Approach to Deloading: Recommendations and Considerations for Strength and Physique Sports" (Delphi consensus with expert coaches) <https://shura.shu.ac.uk/35313/3/Bell-APracticalApproach(AM).pdf>

Definition, from the same group's qualitative study: "A deload is a period of reduced training stress designed to mitigate physiological and psychological fatigue, promote recovery, and enhance preparedness for subsequent training." Bell et al. 2022, *Frontiers in Sports and Active Living* <https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.1073223/full>

Important honesty note from that paper: deloading is **underrepresented in the published literature** and lacked a clear operational definition until this work. Nobody has a randomized trial telling you 4 weeks beats 8. Present deload cadence to the user as a default, not a fact.

Counter-evidence worth knowing: a supervised trial found a one-week deload during a resistance training block did not meaningfully improve muscular adaptations. Coleman et al., *PeerJ* 2024 <https://peerj.com/articles/16777/>. So scheduled deloads may be more about sustainability than about extra growth.

**Autoregulated deload triggers (use instead of, or alongside, the calendar).**

| Signal | Threshold |
|---|---|
| Week-over-week performance drop | reps at the same load fall vs the previous microcycle (RP) |
| Repeat failure | any -10% decrease rule fires twice within 3 weeks |
| RPE inflation | same load, RPE up by >= 1 for 2 consecutive weeks |
| Stall | no e1RM PR in 3 weeks on that lift |
| Subjective | sleep disruption, motivation drop, persistent soreness |
| Joint pain | deload and **refer to a professional** |

### Time off

The evidence is more forgiving than gym folklore suggests.

| Time off | What the evidence says | Suggested agent action |
|---|---|---|
| Under 2 weeks | Strength and volitional drive maintained | Resume at 100%. Warn the first session may feel harder |
| 2-4 weeks | Short-term detraining (< 4 weeks) generally shows strength and size well maintained | Resume at 90-95%, rebuild over 1-2 sessions |
| Over 4 weeks | Decrements typically reported beyond 4 weeks | Resume at 80%, rebuild over 2-3 weeks |
| Long layoff, returning | A 3-week mid-program break did not stop untrained subjects finishing at the same strength as continuous trainees | Reassure the user, do not restart from zero |

Sources: <https://www.mdpi.com/2813-0413/1/1/1> (systematic review of detraining effects), <https://onlinelibrary.wiley.com/doi/10.1111/sms.14739> (Halonen 2024, continuous vs periodic training), <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5293799/> (strength maintained at 2 weeks), summary at <https://sci-fit.net/detraining/>

The specific percentages in the "suggested action" column are **DERIVED**. The literature says "maintained" and "decrements" without giving a return-to-training load formula. Do not present these as evidence-based numbers to the user.

### Readiness (sleep)

Acute single-night sleep loss appears to have little effect on maximal strength. **Consecutive** nights of restriction do. Three nights at 3 hours significantly reduced maximal strength and submaximal lift capacity in bench press, leg press, and deadlift. A meta-analysis found acute sleep loss impaired maximum force with SMD = -0.35.

Sources: <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12263768/>, <https://pubmed.ncbi.nlm.nih.gov/29422383/>, <https://link.springer.com/article/10.1007/s40279-022-01706-y>

**Agent rule.** IF the user logs poor sleep for a single night, THEN do not change the prescription, just note it when interpreting a missed target. IF poor sleep for **3 or more consecutive nights**, THEN hold rather than increase, and do not count a missed session against the failure counter.

That last clause matters. Without it, a bad sleep week fires a spurious deload.

---

## Plateau detection

No source defines a plateau statistically. Every one of them uses "you missed reps N times". Here is a practical definition an agent can compute.

**Practical definition.** For a given exercise and rep target, compute e1RM per session. A plateau exists when:

```
no new e1RM personal record in the last N sessions at the same rep target
```

with N = **6 sessions** or **3 weeks**, whichever comes first, and at least 4 sessions of data in the window.

**Statistical version (more robust to noise).** Fit a linear regression of e1RM against session index over a trailing 8-session window. A plateau exists when the slope's 95% confidence interval includes zero. A regression exists when the upper bound of the CI is below zero.

Both are **DERIVED**. I found no source that defines plateau statistically. This is the right thing to prototype, not the right thing to assert.

**Practical fallbacks that are sourced.**

- StrongLifts: three consecutive failures on an exercise. <https://stronglifts.com/stronglifts-5x5/plateaus/>
- RP: this microcycle's performance is worse than last microcycle's. <https://arvo.guru/resources/methods/rp-training>
- Madcow: the weekly ramp stops producing a PR. <https://www.powerliftingtowin.com/madcows-5x5/>

**Noise warning.** e1RM computed from a single top set is noisy. Day-to-day variation of 5% is normal. Do not fire a plateau or regression alert off a single session. Require 2 consecutive sessions or a trailing-window trend.

---

## Conflicts between sources and how to resolve them

| Conflict | Sides | Resolution |
|---|---|---|
| How many failures before a decrease | Starting Strength and StrongLifts say 3 consecutive. Greyskull decreases after 1 bad AMRAP. GZCLP takes 3 stage failures, effectively many sessions | Depends on how expensive a decrease is. When a decrease costs 3-4 sessions of rebuilding, wait for 3. When the scheme rebuilds fast, act sooner. Ship 2 consecutive as the default with a user override |
| Deload cadence | Wendler original: every 4th week. Wendler *Beyond*: every 7th week. Bell consensus: every 4-8 weeks. PeerJ trial: a scheduled deload showed no adaptation benefit | The range 4-8 weeks is the honest answer. Prefer autoregulated triggers over the calendar, and let the calendar be the backstop |
| Is the 5/3/1 training max 90% of 1RM | Every secondary source says 90%. Wendler himself says there is no hard rule and lower is often better | **Wendler wins, he wrote it.** Seed at 85-90%, bias low, always user-editable |
| The 10% rule for running | Universally repeated. Not supported by the 5,200-runner cohort | Drop it. Use the 110%-of-longest-recent-run single-session rule instead |
| RPE-based vs percentage-based load | RTS and Helms favour RPE. Helms 2018 found the two comparable when sets and reps are matched | Not a real conflict for the app. Use reps for the decision and RPE as a cap. Do not require RPE from novices |
| Is the deload a load cut or a volume cut | Bell consensus: volume 30-50%, intensity 10-20%, so mostly volume. Israetel: half the sets, further from failure, sometimes lighter | They agree in substance. Cut volume first, load second |
| Volume: more is better vs MRV exists | Schoenfeld meta shows a graded dose-response with more sets. RP says there is a recoverable ceiling | Both true at different timescales. Dose-response holds across studies; MRV is an individual weekly ceiling. Progress volume upward until performance drops, then deload |
| Novice RPE accuracy | RPE schemes assume the user can rate accurately. Zourdos 2016 shows novices cannot | Hard gate. Below 1 year training age, RPE is logged but not used for decisions |

---

## Consolidated decision table

Signal to action. Evaluate top to bottom, first match wins. Confidence is my judgment of how well the number is sourced, not the sources' own confidence.

| # | Signal (fields read) | Action | Confidence | Source |
|---|---|---|---|---|
| 1 | `session.flags` contains pain on this exercise | Stop progressing. Offer a variation. **Refer to a professional** | High (policy, not evidence) | not a training rule |
| 2 | Days since last session on this exercise > 28 | Resume at 80% of last load, rebuild over 2-3 weeks | Low, DERIVED | <https://www.mdpi.com/2813-0413/1/1/1> |
| 3 | Days since last session 14-28 | Resume at 90-95% | Low, DERIVED | same |
| 4 | Days since last session 7-14 | Resume at 100%, flag the session as a re-entry | Medium | <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5293799/> |
| 5 | 3+ consecutive nights poor sleep logged | Hold. Do not count a miss against the failure counter | Medium | <https://pubmed.ncbi.nlm.nih.gov/29422383/> |
| 6 | Missed bottom of rep range, 2 consecutive sessions (or 3 of last 4) | **Decrease** 10% | High | <https://support.stronglifts.com/article/71-progression>, see note |
| 7 | Failure-triggered decrease fired twice in 3 weeks | **Deload**: volume -30-50%, load -10-20%, 5-7 days | Medium | <https://shura.shu.ac.uk/35313/3/Bell-APracticalApproach(AM).pdf> |
| 8 | No e1RM PR in 6 sessions / 3 weeks at same rep target | **Deload**, then resume at 95% and rebuild | Low, DERIVED | plateau section |
| 9 | Reps at same load lower than previous microcycle, whole session | **Deload** | Medium | <https://arvo.guru/resources/methods/rp-training> |
| 10 | RPE at same load up >= 1 for 2 consecutive weeks | **Decrease** 2.5-5% | Low, DERIVED | <https://fitnessvolt.com/rpe-training/rpe-chart/> |
| 11 | Weeks since last deload >= 8 | **Deload** (calendar backstop) | Medium | <https://shura.shu.ac.uk/35313/3/Bell-APracticalApproach(AM).pdf> |
| 12 | All sets at top of rep range AND last-set RPE <= 9 AND `jump_pct` <= 0.05 | **Increase** 1 load step, reset to bottom of range | High | <https://muscleandstrengthpyramids.com/counting-training-volume-greg-nuckols/> |
| 13 | All sets at top of rep range AND `jump_pct` > 0.05 | **Hold** load, add a set, or suggest fractional plates | Low, DERIVED | increment section |
| 14 | All sets at top of rep range AND last-set RPE >= 9.5, 2 sessions | **Hold**. Load is right, fatigue is high | Medium | RIR scale, <https://pmc.ncbi.nlm.nih.gov/articles/PMC4961270/> |
| 15 | AMRAP set >= 2x the target reps | **Increase** 2 load steps | Medium | Greyskull <https://www.powerliftingtowin.com/greyskull-lp/>, nSuns <https://liftvault.com/programs/powerlifting/n-suns-lifting-spreadsheets/> |
| 16 | Bodyweight exercise, hit 3x8 on current variation | **Advance** to next variation, restart at 3x5 | High | <https://redditbwf.github.io/wiki/recommended_routine.html> |
| 17 | Any set below top of rep range, no failure streak | **Hold**. Target +1 rep on the weakest set | High | double progression |
| 18 | Weekly sets for this muscle < MEV and no fatigue signals | **Increase volume** by 1-2 sets next week | Medium | <https://arvo.guru/resources/methods/rp-training>, <https://pubmed.ncbi.nlm.nih.gov/27433992/> |
| 19 | Planned run > 110% of longest run in last 30 days | **Warn**, suggest capping at 110% | Medium | <https://runningmagazine.ca/sections/training/the-10-per-cent-mileage-rule-isnt-what-you-think-study-warns/> |
| 20 | User training age < 1 year | Ignore RPE inputs in rules 10 and 14 | High | Zourdos 2016 <https://journals.lww.com/nsca-jscr/fulltext/2016/01000/novel_resistance_training_specific_rating_of.31.aspx> |


---

## Experience level, sex, and age caveats

**Experience level.** This is the biggest single moderator and every source agrees on the direction.

| Level | Progression cadence that works | Scheme fit |
|---|---|---|
| Novice (0-9 months) | Every session | Starting Strength, StrongLifts, Greyskull, GZCLP, bodyweight RR |
| Intermediate (9 months to ~3 years) | Every week | Texas Method, Madcow, 5/3/1, nSuns, double progression |
| Advanced (3+ years) | Every month or block | 5/3/1 with 7th week protocol, RTS autoregulation, RP mesocycles |

If the agent applies session-to-session linear progression to an intermediate, it will manufacture failures and fire deloads that are not warranted. Detecting which bucket the user is in matters more than picking the right scheme within a bucket.

**Sex.** None of the progression schemes above state sex-specific rules. Absolute load increments hit women harder in percentage terms simply because absolute loads tend to be lower, which makes the `jump_pct` guard more important, not less. Beyond that: **GAP, not researched in this slice.**

**Age.** No progression scheme reviewed here states age-specific rules. Recovery capacity and therefore deload frequency plausibly shift with age, but I found nothing prescriptive in the time available. **GAP.**

---

## Open questions for the user

These change which default the app should ship. I cannot ask directly from here.

1. **Training age.** How long have you trained consistently? This picks the entire rule set (session, weekly, or block progression). Everything else is downstream of this.
2. **Primary goal.** Strength or hypertrophy? Strength favours load progression and 5/3/1-style TM management. Hypertrophy favours rep-range progression and RP-style volume landmarks. They give different answers to the same log.
3. **Will you log RPE?** If not, rules 10, 14, and all of the RTS material get dropped and the engine runs on reps alone. That is a legitimate choice and simplifies the app considerably.
4. **Equipment.** Do you have fractional plates? Without them the `jump_pct` guard has no smaller step to suggest and can only say "add reps".
5. **Barbell, dumbbell, machine, or bodyweight mix?** Determines how much the increment-sizing logic matters.
6. **Deload preference.** Scheduled every N weeks, or only when the log says so? The evidence does not settle this, so it is a taste call.
7. **Should the agent auto-apply decisions or suggest them?** Auto-applying a 10% decrease on a bad day would be infuriating. Suggesting it with a one-tap accept probably is not.

---

## Gaps in this slice

Flagged honestly rather than papered over.

- **Zone 2 / aerobic base progression**: no numbers gathered. Out of time.
- **Sex and age moderators**: no prescriptive sources found.
- **Primary book texts not read**: *Practical Programming* (Rippetoe), *5/3/1 Forever* (Wendler), *Greyskull LP* (Sheaffer), *The Muscle and Strength Pyramids* (Helms). All paywalled. Their rules are reported here from consistent secondary sources and tagged.
- **Cody Lefever's original GZCL blog** was not fetched directly; the r/fitness wiki version was used instead.
- **RTS fatigue percent tables**: the concept is sourced, the specific per-exercise percentages are behind the RTS paywall.
- **The "-5% per RPE point over target" rule**: widely repeated, no primary source found. Do not ship it as fact.

---

## Source list

Program documentation:
- Starting Strength programs <https://startingstrength.com/get-started/programs>
- Barbell Logic, novice LP explained <https://barbell-logic.com/novice-linear-progression-explained/>
- StrongLifts progression settings <https://support.stronglifts.com/article/71-progression>
- StrongLifts failure <https://stronglifts.com/stronglifts-5x5/failure/>
- StrongLifts plateaus <https://stronglifts.com/stronglifts-5x5/plateaus/>
- Greyskull LP review, PowerliftingToWin <https://www.powerliftingtowin.com/greyskull-lp/>
- Jim Wendler on the training max <https://www.jimwendler.com/blogs/jimwendler-com/101082310-the-training-max-what-you-need-to-know>
- 5/3/1 glossary incl. 7th week protocol <https://liftvault.com/resources/531-glossary/>
- 5/3/1 overview, BarBend <https://barbend.com/5-3-1-program/>
- GZCLP, The Fitness Wiki <https://thefitness.wiki/routines/gzclp/>
- nSuns program guide <https://liftvault.com/programs/powerlifting/n-suns-lifting-spreadsheets/>
- nSuns review <https://muscleevo.net/nsuns-program/>
- Madcow 5x5 <https://www.strengthlog.com/madcow-5x5/> and <https://www.powerliftingtowin.com/madcows-5x5/>
- Texas Method vs Madcow <https://powerliftingtechnique.com/texas-method-vs-madcow-5x5/>
- r/bodyweightfitness Recommended Routine <https://redditbwf.github.io/wiki/recommended_routine.html>
- RTS fatigue percents <https://store.reactivetrainingsystems.com/blogs/advanced-concepts/fatigue-percents-revisited>
- RTS autoregulating volume <https://articles.reactivetrainingsystems.com/2016/12/29/auto-regulating-volume/>
- Autoregulation review, PowerliftingToWin <https://www.powerliftingtowin.com/autoregulation/>
- RP volume landmarks and mesocycles <https://arvo.guru/resources/methods/rp-training>
- Israetel on MRV <https://propanefitness.com/maximum-recoverable-volume/>
- Nuckols on volume, Muscle and Strength Pyramids <https://muscleandstrengthpyramids.com/counting-training-volume-greg-nuckols/>
- RPE to %1RM chart (Tuchscherer-derived) <https://fitnessvolt.com/rpe-training/rpe-chart/>
- Fractional plates <https://www.serioussteel.com/blogs/news/fractional-plates-platemates-small-weight-increments-big-gains>

Peer-reviewed and preprint:
- Zourdos et al. 2016, RIR-based RPE scale, *JSCR* <https://journals.lww.com/nsca-jscr/fulltext/2016/01000/novel_resistance_training_specific_rating_of.31.aspx>
- Helms et al. 2016, application of the RIR-based RPE scale, *SCJ* <https://journals.lww.com/nsca-scj/fulltext/2016/08000/application_of_the_repetitions_in_reserve_based.10.aspx> (open access <https://pmc.ncbi.nlm.nih.gov/articles/PMC4961270/>)
- Helms et al. 2018, RPE vs %1RM loading <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5877330/>
- Schoenfeld, Ogborn, Krieger 2017, volume dose-response meta-analysis <https://pubmed.ncbi.nlm.nih.gov/27433992/>
- Resistance training dose response meta-regressions (2025-26 update) <https://pubmed.ncbi.nlm.nih.gov/41343037/>
- Bell et al., practical approach to deloading (Delphi consensus) <https://shura.shu.ac.uk/35313/3/Bell-APracticalApproach(AM).pdf>
- Bell et al. 2022, coaches' perceptions of deloading, *Front Sports Act Living* <https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.1073223/full>
- Coleman et al. 2024, one-week deload effects, *PeerJ* <https://peerj.com/articles/16777/>
- Detraining systematic review <https://www.mdpi.com/2813-0413/1/1/1>
- Halonen et al. 2024, continuous vs periodic resistance training <https://onlinelibrary.wiley.com/doi/10.1111/sms.14739>
- Strength maintained at 2 weeks detraining <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5293799/>
- Sleep loss and muscle strength, systematic review <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12263768/>
- Inadequate sleep and muscle strength, *JSAMS* 2018 <https://pubmed.ncbi.nlm.nih.gov/29422383/>
- Acute sleep loss and physical performance meta-analysis, *Sports Med* <https://link.springer.com/article/10.1007/s40279-022-01706-y>
- Nielsen et al. 2014, running distance progression and injury, *JOSPT* <https://www.jospt.org/doi/10.2519/jospt.2014.5164>
- Weight-dependent 1RM prediction preprint, UNVERIFIED <https://arxiv.org/pdf/2603.17495>

Reporting:
- 10% rule critique <https://runningmagazine.ca/sections/training/the-10-per-cent-mileage-rule-isnt-what-you-think-study-warns/>
- 10% rule myth <https://run.outsideonline.com/training/getting-started/myth-of-the-10-percent-rule/>
- Detraining summary <https://sci-fit.net/detraining/>

---

**Medical note.** Nothing here is medical advice. Any rule touching pain, injury, or joint symptoms routes the user to a qualified professional. The agent should never prescribe training through pain.
