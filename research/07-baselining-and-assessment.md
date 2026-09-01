# Baselining a new client: intake, screening, and assessment

Research slice 07. Written 2026-08-31.

Sibling slices: 08 goal-specific programming, 09 sport-specific, 10 medical and
special populations, 11 transgender athletes, 12 trainer practice and ethics.
This file covers only what happens before the first program is written.

The user's framing: "You need to make sure that you can meet people where
they're at and what their abilities at the moment are. You probably want to do
some base lining before you make their program."

---

## TL;DR

The minimum viable baseline for a chat-based agent, in order:

1. PAR-Q+ 2025, all 7 questions, verbatim. Any YES routes to follow-ups or a clinician.
2. Intake interview: goal, training history, schedule, equipment, injuries, sleep, stress, preferences, readiness stage.
3. Resting HR and blood pressure if the person has a cuff. Bodyweight and waist. That is the whole "body" panel.
4. Strength: rep-max on 2 to 4 lifts they can already do safely, plus push-ups, a plank, and a hang or pull-up count. Estimate 1RM, never test it on a novice.
5. Cardio: talk test during any easy session, plus one field test (Cooper 12-min or Rockport 1-mile walk) only if they want a cardio goal.
6. Mobility: ankle knee-to-wall, shoulder overhead reach, and a filmed bodyweight squat. Everything else needs a human.
7. Skip: FMS scoring, body fat percentage, VO2max lab equivalence, and anything requiring hands on the client.
8. Re-test strength every 8 to 12 weeks, cardio every 8 to 12 weeks, mobility every 12 weeks, intake questions every 12 weeks or on any life change.
9. Store the answers as a versioned profile with a timestamp per field. Baselines rot.
10. The agent's job is triage and a starting load, not diagnosis. Every red flag exits to a human.

---

## 1. Safety gate: pre-participation screening

This runs first. Nothing else happens until it clears.

### 1.1 PAR-Q+ 2025, the seven general health questions

The current version is dated 01-11-2024, copyright 2025 PAR-Q+ Collaboration.
Source PDF: https://eparmedx.com/wp-content/uploads/2025/01/PARQPlus2025Fillable.pdf
Home: https://eparmedx.com/

Quoted verbatim from the 2025 form:

1. "Has your doctor ever said that you have a heart condition OR high blood pressure?"
2. "Do you feel pain in your chest at rest, during your daily activities of living, OR when you do physical activity?"
3. "Do you lose balance because of dizziness OR have you lost consciousness in the last 12 months? Please answer NO if your dizziness was associated with over-breathing (including during vigorous exercise)."
4. "Have you ever been diagnosed with another chronic medical condition (other than heart disease or high blood pressure)?" (list conditions)
5. "Are you currently taking prescribed medications for a chronic medical condition?" (list conditions and medications)
6. "Do you currently have (or have had within the past 12 months) a bone, joint, or soft tissue (muscle, ligament, or tendon) problem that could be made worse by becoming more physically active? Please answer NO if you had a problem in the past, but it does not limit your current ability to be physically active."
7. "Has your doctor ever said that you should only do medically supervised physical activity?"

What each answer triggers, quoted from the form:

- All NO: "you are cleared for physical activity... Start becoming much more physically active - start slowly and build up gradually." Also: "If you are over the age of 45 yr and NOT accustomed to regular vigorous to maximal effort exercise, consult a qualified exercise professional before engaging in this intensity of exercise."
- One or more YES: "COMPLETE PAGES 2 AND 3." Pages 2 and 3 are condition-specific follow-ups covering arthritis/osteoporosis/back problems, cancer, heart or cardiovascular condition, high blood pressure, metabolic conditions, mental health or learning difficulty, respiratory disease, spinal cord injury, stroke, and "any other medical condition... or two or more medical conditions."
- All follow-ups NO: "you are ready to become more physically active" with the advice to "consult a qualified exercise professional" and to build to "150 minutes or more of moderate intensity physical activity per week."
- Any follow-up YES: "You should seek further information before becoming more physically active or engaging in a fitness appraisal. You should complete the specially designed online screening and exercise recommendations program - the ePARmed-X+ at www.eparmedx.com and/or visit a qualified exercise professional."

Three hard "delay" conditions, quoted:

- "You are currently experiencing a temporary illness, such as a cold or fever. It is best to wait until you feel better."
- "You are pregnant. In this case, talk with your health care practitioner, physician, qualified exercise professional, and/or complete the ePARmed-X+ at www.eparmedx.com before becoming more physically active."
- "Your health changes."

Two licensing facts that constrain the agent:

- "You are encouraged to photocopy the PAR-Q+. You must use the entire questionnaire and NO changes are permitted." So the agent must present all seven questions in the original wording. It may not paraphrase them or drop question 5 because it feels intrusive.
- The participant declaration says the clearance "is valid for a maximum of 12 months from the date it is completed and becomes invalid if my condition changes." So the stored screening has a 12-month expiry and a manual invalidation trigger.

Citation for the instrument: Warburton DER, Jamnik VK, Bredin SSD, Gledhill N.
Health & Fitness Journal of Canada 4(2):3-23, 2011.
https://hfjc.library.ubc.ca/index.php/HFJC/article/view/863

### 1.2 ACSM pre-participation algorithm (2015 update)

The 2015 update replaced risk-factor counting with a three-input decision.
Primary paper: Riebe D et al., "Updating ACSM's Recommendations for Exercise
Preparticipation Health Screening," Med Sci Sports Exerc 2015;47(11):2473-9.
https://pubmed.ncbi.nlm.nih.gov/26473759/

The three inputs, per the published summary of the algorithm:

1. Current physical activity level.
2. Presence of signs or symptoms, and known cardiovascular, metabolic, or renal disease.
3. Desired exercise intensity.

Key change, quoted from the literature summarising the update: "The
classification of individuals as having low, moderate, or high risk of CVD is no
longer included in the new ACSM exercise preparticipation health screening
process." Instead, "individuals are referred to their health care provider for
medical clearance, defined as approval from a health care professional to engage
in exercise."
https://pubmed.ncbi.nlm.nih.gov/28557860/

Routing, as described by ACE's summary of the algorithm
(https://www.acefitness.org/continuing-education/certified/february-2018/6898/new-preparticipation-guidelines-remove-barriers-to-exercise/):

| Currently exercising? | Known CV / metabolic / renal disease or signs and symptoms? | Action |
|---|---|---|
| No | No | Start light to moderate. No clearance needed. |
| No | Yes | Medical clearance before starting. |
| Yes | No | Continue. Clearance needed only when progressing to vigorous. |
| Yes | Yes, symptoms appear | Stop exercise, get medical clearance. |
| Yes | Yes, known disease, no symptoms | Clearance before progressing to vigorous aerobic exercise. |

Effect size of the change: applying the ACSM algorithm to NHANES 2001-2004,
"2.6% of adults would be referred only before beginning vigorous exercise and
54.2% of respondents would be referred before beginning any exercise," and the
algorithm "referred a smaller proportion of adults for preparticipation medical
clearance than the previously examined questionnaires."
https://pubmed.ncbi.nlm.nih.gov/28557860/

UNVERIFIED: I could not reach a primary, quotable copy of the ACSM flowchart
figure or the exact ACSM definition of "regular exercise" (commonly cited as at
least 30 min of moderate intensity, at least 3 days/week, for at least the last
3 months) or the exact light/moderate/vigorous MET bands. The ACSM Exercise is
Medicine PDF now 301-redirects to https://acsm.org/EIM with no document. Buy or
borrow ACSM's Guidelines for Exercise Testing and Prescription (11th ed.,
Wolters Kluwer) and quote Table 2.1 and Figure 2.1 directly before shipping
these numbers.

### 1.3 Blood pressure thresholds

2017 ACC/AHA categories (the guideline is the primary source:
https://www.ahajournals.org/doi/10.1161/hyp.0000000000000065, summarised at
https://www.acc.org/Latest-in-Cardiology/ten-points-to-remember/2017/11/09/11/41/2017-Guideline-for-High-Blood-Pressure-in-Adults):

| Category | Systolic | | Diastolic |
|---|---|---|---|
| Normal | <120 mm Hg | and | <80 mm Hg |
| Elevated | 120-129 | and | <80 |
| Hypertension stage 1 | 130-139 | or | 80-89 |
| Hypertension stage 2 | >=140 | or | >=90 |

UNVERIFIED: The "hypertensive crisis" threshold (commonly cited as >180 and/or
>120 with immediate medical attention) did not appear in the sources I could
retrieve. Confirm against the guideline text before the agent uses it as a stop
rule.

### 1.4 Absolute contraindications to exercise testing

From ACSM's list of absolute contraindications to symptom-limited exercise
testing, as reproduced in clinical teaching material
(https://pressbooks.gvsu.edu/cardiacrehab/chapter/common-graded-exercise-test-protocols/):

- Acute myocardial infarction within 2 days
- Ongoing unstable angina
- Uncontrolled cardiac arrhythmia with hemodynamic compromise
- Active endocarditis
- Symptomatic severe aortic stenosis
- Decompensated heart failure
- Acute pulmonary embolism, pulmonary infarction, or deep venous thrombosis
- Acute myocarditis or pericarditis
- Acute aortic dissection
- Physical disability that precludes safe and adequate testing

UNVERIFIED: this list is reproduced from secondary teaching material, not from
ACSM GETP directly. It matches the widely taught list but should be quoted from
GETP 11th ed. Box 5.1 before shipping. It is also a list about *maximal graded
exercise testing*, not about all exercise, and the agent should never be running
a graded exercise test anyway. Its use here is as a red-flag vocabulary.

---

## 2. Intake script

Ask in this order. The order matters: safety first, then goal (people are
motivated to answer once they have said what they want), then constraints, then
the soft stuff. Do not ask all of it in one message. Batch 2 to 4 questions per
turn.

Field names are snake_case, intended for a single `athlete_profile` record with
a `measured_at` timestamp per group.

### Block A: safety (blocking, must complete)

| # | Question | Why | Field |
|---|---|---|---|
| A1 | PAR-Q+ Q1-Q7 verbatim | Legal and clinical gate. Wording may not be changed. | `parq.q1` .. `parq.q7`, `parq.completed_at` |
| A2 | Follow-ups if any YES | Routes to ePARmed-X+ or a clinician. | `parq.followups`, `parq.outcome` |
| A3 | Are you pregnant, or pregnant in the last 12 weeks? | PAR-Q+ names pregnancy as a delay condition. | `pregnancy_status` |
| A4 | Are you ill right now (cold, fever)? | PAR-Q+ delay condition. Re-asked per session, not just at intake. | `acute_illness` |
| A5 | Do you have a blood pressure cuff? If yes, seated resting BP after 5 min. | Sets the stage-1/stage-2 flag. Optional, not blocking. | `bp_systolic`, `bp_diastolic`, `bp_measured_at` |
| A6 | Any medication that affects heart rate (beta blockers) or balance? | HR-based prescription breaks under beta blockade. | `hr_affecting_meds` |

### Block B: goal and motivation

| # | Question | Why | Field |
|---|---|---|---|
| B1 | What do you want to be able to do in 6 months? | Free text first, before offering categories. Gives the agent the client's own words to mirror back. | `goal_statement` |
| B2 | Pick the closest: get stronger / build muscle / lose fat / run or ride further / sport-specific / general health / rehab-adjacent | Routes to slice 08 or 09. | `goal_primary`, `goal_secondary` |
| B3 | What made now the time? | Distinguishes an external deadline from an internal one. Changes adherence tactics. | `goal_trigger` |
| B4 | Which is true: not thinking about starting / thinking about it / planning to start in the next month / started in the last 6 months / been at it over 6 months | Maps to the transtheoretical model stages: precontemplation, contemplation, preparation, action, maintenance. Prochaska and DiClemente. https://www.ncbi.nlm.nih.gov/books/NBK556005/ | `ttm_stage` |
| B5 | On a 0-10, how confident are you that you'll still be doing this in 3 months? | Self-efficacy. A low number means shrink the plan, not motivate harder. | `confidence_0_10` |

Note on B4: the TTM stages are precontemplation (no intention to change within
6 months), contemplation, preparation, action, maintenance, and a debated sixth
stage, termination. Progress is cyclical, not linear, so the field must be
re-askable and must accept regression.
https://www.ncbi.nlm.nih.gov/books/NBK556005/

### Block C: training history and training age

| # | Question | Why | Field |
|---|---|---|---|
| C1 | Have you lifted weights before? For how long, and how consistently? | Training age drives everything in section 5. "Consistently" is the load-bearing word. | `lifting_months`, `lifting_consistency` |
| C2 | In the last 3 months, how many days a week did you do structured exercise, and at what intensity? | This is the ACSM algorithm's "regular exercise" input. | `current_days_per_week`, `current_intensity` |
| C3 | Best lifts you know, and when | Seeds the strength baseline without a test. | `known_lifts[]` |
| C4 | Which lifts do you already know how to do safely? Squat, deadlift, bench, overhead press, row, pull-up | Determines what can be rep-max tested versus what must be taught first. | `competent_lifts[]` |
| C5 | Longest run/ride/swim in the last 3 months | Cardio baseline without a test. | `cardio_recent_max` |
| C6 | Have you ever followed a written program? Which? | Tells you whether "program" means anything to them. | `program_history` |

### Block D: constraints

| # | Question | Why | Field |
|---|---|---|---|
| D1 | Which days can you train, and for how long per session? | Hard constraint on the split. | `available_days[]`, `session_minutes` |
| D2 | Where do you train? Commercial gym, home, garage, bodyweight only | Equipment gate. | `training_location` |
| D3 | What equipment do you have access to? Barbell, rack, plates, dumbbells (range), machines, bands, pull-up bar, cardio machines | Every exercise selection depends on this. Ask for a list or a photo. | `equipment[]`, `dumbbell_max_kg` |
| D4 | Any hard scheduling constraints? Shift work, kids, travel | Predicts the missed-session pattern. | `schedule_constraints` |

### Block E: pain, injury, and body

| # | Question | Why | Field |
|---|---|---|---|
| E1 | Any current pain? Where, how long, what makes it worse or better, 0-10 at worst | This is triage, not diagnosis. Red flags exit to a clinician. | `pain_sites[]` |
| E2 | Past injuries or surgeries, and whether they still limit you | PAR-Q+ Q6 covers the last 12 months. This one goes further back. | `injury_history[]` |
| E3 | Movements you already know hurt | Direct exercise exclusions. | `excluded_movements[]` |
| E4 | Bodyweight, and how it has moved over the last 6 months | Trend matters more than the number. | `bodyweight_kg`, `weight_trend` |
| E5 | Height | Needed for load norms per bodyweight and for BMI if you want it. | `height_cm` |
| E6 | Waist circumference at the navel, if they have a tape | Better risk signal than BMI. Thresholds in section 4.6. | `waist_cm` |

### Block F: recovery and lifestyle

| # | Question | Why | Field |
|---|---|---|---|
| F1 | Typical sleep, hours and quality 1-5 | The single biggest modifier of what volume they tolerate. | `sleep_hours`, `sleep_quality_1_5` |
| F2 | Stress right now, 1-5 | Same. | `stress_1_5` |
| F3 | Do you wear anything that tracks HR or HRV? | Decides whether readiness data exists at all. | `wearable` |
| F4 | Resting HR on waking, if known | Cheapest longitudinal marker there is. | `resting_hr` |
| F5 | Anything about food or alcohol you want factored in? | Stay in lane. Note it, do not prescribe. Slice 12 owns the boundary. | `nutrition_notes` |

### Block G: preferences

| # | Question | Why | Field |
|---|---|---|---|
| G1 | What kind of training do you actually enjoy? | Adherence beats optimality. | `likes[]` |
| G2 | What will you refuse to do? | Prevents writing a program they will abandon in week 2. | `dislikes[]` |
| G3 | How much detail do you want from me? Just the plan / plan plus reasoning / full nerd | Sets the agent's verbosity. | `verbosity_pref` |
| G4 | Do you want me to push you, or to be gentle when you miss? | Sets the adherence tone. | `coaching_tone` |

---

## 3. Movement and mobility screens

### 3.1 What the evidence says about screening in general

The Functional Movement Screen is the most popular battery and the most
criticised. The seven tests are deep squat, hurdle step, inline lunge, shoulder
mobility, active straight leg raise, trunk stability push-up, and rotary
stability. Each is scored 0 to 3 (3 = performed as intended with no
compensation, 2 = completed with compensation, 1 = unable to complete the
pattern, 0 = pain during the movement), summing to 0-21.
https://www.functionalmovement.com/files/Articles/572a_FMS_Article_NoBleed_Digital.pdf
https://www.physio-pedia.com/Functional_Movement_Screen_(FMS)

The injury-prediction claim does not hold up. Moran et al., systematic review
with meta-analysis, Br J Sports Med:

- In male military personnel, "strong" evidence that the association between an
  FMS composite score cut-point of <=14/21 and subsequent injury was "small"
  (pooled risk ratio 1.47, 95% CI 1.22 to 1.77, p<0.0001, I2=57%).
- "Moderate" evidence to recommend *against* using the composite score as an
  injury prediction test in football (soccer).
- "Limited" or "conflicting" evidence in American football, college athletes,
  basketball, ice hockey, running, police, and firefighters.
- Conclusion: the strength of association "does not support its use as an injury
  prediction tool."

https://pubmed.ncbi.nlm.nih.gov/28360142/
A second review reached the same conclusion:
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6797344/

Practical read for the agent: use movement screening to pick exercises and set
starting positions, never to issue an injury-risk score. The one FMS element
worth keeping is the pain rule. A 0 (pain during the movement) is a referral
signal regardless of the composite. There is evidence that pain during the
screen, rather than the composite score, carries the injury association.
https://www.sciencedirect.com/science/article/abs/pii/S1440244017309891

### 3.2 The screen menu

| Test | Protocol | Equipment | Norms / interpretation | Self-administrable over chat? |
|---|---|---|---|---|
| Bodyweight squat (NASM overhead squat assessment) | Feet shoulder-width, toes forward, arms overhead, squat to chair height, 5 reps. View from front and side. Look for feet turning out, knees moving inward, low back arching, arms falling forward. | None | NASM maps each compensation to overactive and underactive muscles. Arms fall forward: overactive lats, teres major, pec major/minor; underactive mid/lower trap, rhomboids, rotator cuff. Low back arches: overactive hip flexor complex, erector spinae, lats; underactive glute max, hamstrings, intrinsic core. https://support.nasm.org/how-do-i-perform-an-overhead-squat-assessment https://www.physio-pedia.com/images/d/d9/Nasm_overhead_squat_solutions_table_cptpes(pdf-32k).pdf | With video. Needs two camera angles. Not by text description. |
| Knees-in differential test | Repeat the squat with heels raised on plates or a 2x4. If knees track better, suspect ankle. If not, suspect hip. | Plates or board | NASM's own disambiguation step. https://support.nasm.org/how-do-i-perform-an-overhead-squat-assessment | With video |
| Ankle dorsiflexion, weight-bearing lunge (knee-to-wall) | Foot perpendicular to wall, drive knee to wall keeping heel down, find max distance where knee still touches. Measure toe-to-wall in cm. | Tape measure, wall | Typical 10-15 cm. Under 10 cm suggests a meaningful restriction. Declines with age, notably from 60-69. Males slightly greater than females. Interrater ICC 0.95 (95% CI 0.92-0.97); intra-rater ICC 0.65-0.99, minimal detectable change 1.9 cm / 4.7 degrees. https://pubmed.ncbi.nlm.nih.gov/41723909/ https://www.sciencedirect.com/science/article/pii/S2468781226000408 | Yes. Self-measurable with a tape. One of the few genuinely chat-friendly tests. |
| Shoulder mobility (FMS reach, Apley scratch) | Hands in fists, thumbs inside, reach one over the shoulder and one up the back, measure the gap between fists. FMS scores it against hand length. | Tape measure | FMS 3/2/1 bands relative to hand length. Pain clearing test scores 0. https://www.physio-pedia.com/Functional_Movement_Screen_(FMS)| With video or a photo. Self-measuring the gap is error-prone. |
| Single-leg squat / step-down | Stand on one leg, squat to a controlled depth, watch knee valgus and pelvic drop. | None | Interpreted qualitatively, not scored against a norm. | With video |
| Thoracic rotation (seated or quadruped) | Seated, arms crossed, rotate. Compare left and right. | None | UNVERIFIED: I did not find a norm table I would quote. Use left-versus-right asymmetry, not an absolute number. | With video |
| Hip internal and external rotation | Seated or prone, measure rotation with a goniometer or phone inclinometer. | Goniometer or phone app | UNVERIFIED: no primary norm table retrieved. Compare sides. | No. Needs a second person for reliable measurement. |
| Modified Thomas test | Supine on a bench edge, hug one knee to chest, let the other leg hang. Observe the hanging thigh and shin. | Bench or table edge | Mixed reliability: "very good" inter-rater in one study, only moderate in another. Sensitivity 31%, specificity 57%. Considerable methodological variability between studies. https://www.physio-pedia.com/Thomas_Test https://ijspt.scholasticahq.com/article/120899-reliability-of-goniometric-techniques-for-measuring-hip-flexor-length-using-the-modified-thomas-test | With video, but the poor sensitivity and specificity means the agent should treat it as a conversation starter, not a finding. |
| Sit-and-reach | Standard box protocol, three trials, record best. | Sit-and-reach box | Reliable but not valid as an isolated measure. Reach is confounded by lumbar and thoracic range, arm and leg length ratios, and scapular abduction. Jackson and Langford: "the sit and reach test does not possess criterion-related validity as a field test for hamstring and low back flexibility." https://musculoskeletalkey.com/muscle-length-testing-of-the-lower-extremity/ | Yes, but I would drop it. It measures something, just not the thing it claims. |
| Full FMS (7 tests, 0-21) | The standard FMS protocol with a kit. | FMS kit | See 3.1. Reliable and clinically usable, not an injury predictor. | No. Requires a trained rater and the kit. |

### 3.3 Remote assessment: how far video actually gets you

Telehealth physiotherapy assessment is valid and reliable for range of movement,
muscle strength and endurance, pain intensity, several shoulder and elbow
orthopaedic tests, Berg Balance Scale, timed up and go, and other functional
measures. But concurrent validity is only "low to moderate" for several special
orthopaedic tests, neurodynamic tests, and lumbar posture, and diagnostic
agreement with in-person assessment ranged from 59.7% to 93.3%.

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8684795/
https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0283013

Read for the agent: video is good enough to pick a squat variation and a
starting depth. It is not good enough to conclude anything about a structure.

---

## 4. Test menu

### 4.1 Strength: rep-max and estimated 1RM

Do not have a novice test a true 1RM. The estimation route is accurate enough
and much safer.

Formulas:

- Epley: 1RM = w x (1 + reps/30)
- Brzycki: 1RM = w x 36 / (37 - reps)

https://opensiuc.lib.siu.edu/cgi/viewcontent.cgi?article=1744&context=gs_rp

Accuracy, from the validation literature:

- "Relative accuracy, similarity, and average error improved significantly when
  repetitions to fatigue (RTF) were 10 or fewer." Accuracy falls off above 10
  reps because fatigue, technique breakdown, and individual variation dominate.
  https://paulogentil.com/pdf/TREINO%20DE%20FORC%CC%A7A/Avaliac%CC%A7a%CC%83o/Validation%20of%20Submaximal%20Prediction%20Equations%20for%20the%201RM%20Bench%20Press%20Test.pdf
- In Division I football back squat, Epley was most accurate at 3RM loads
  (+2.7 kg), Brzycki best at 5RM (-3.1 kg), and Epley significantly
  overestimated 1RM when applied to 5RM loads.
  https://opensiuc.lib.siu.edu/cgi/viewcontent.cgi?article=1744&context=gs_rp

Agent protocol: pick a load the client can do for 3 to 6 clean reps, stop 1 to
2 reps short of failure, apply both formulas, store the pair and the rep count,
not just the estimate. Never estimate off a set above 10 reps.

| Test | Protocol | Equipment | Norms | Self-administrable? |
|---|---|---|---|---|
| Estimated 1RM (squat, bench, deadlift, press, row) | Warm up, one set of 3-6 reps at RPE 8, apply Epley and Brzycki | Barbell or dumbbells | ExRx strength standards, untrained to elite, by bodyweight and sex, "based on nearly 70 years of accumulated performance data and are not predicted or regression derived" https://exrx.net/WorkoutTools/StrengthStandards | Yes, if the lift is already competent and there are safety bars or dumbbells. No for a barbell squat or bench with no spotter and no rack. |
| True 1RM | Progressive singles to failure | Rack, spotter | Same standards tables | No. Never over chat for a novice. |
| Push-up test | Cadence 20 per minute (one every 3 s), lower to 90 degrees elbow, to failure or cadence loss | None | CSEP-PATH norms by age and sex, validated against the Canada Fitness Survey (n=23,400). For ages 20-29, roughly 22-28 reps is "good" for men, 15-20 for women in the modified knee position. https://sportscienceinsider.com/push-up-test/ | Yes. Best chat-friendly upper body test there is. |
| Pull-up / dead hang | Max strict reps, or max hang time if zero reps | Bar | UNVERIFIED: I did not retrieve a primary norm table for adult pull-ups. Use it as a within-person tracker, not a percentile. | Yes |
| Front plank | Hold with straight body until form breaks | None | McGill torso endurance reference values around 144 s flexor and 146 s extensor. In college-aged students, non-athletes averaged 83 +/- 63 s and athletes 123 +/- 69 s. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4096102/ | Yes |
| Wall sit | 90 degree knees, hold to failure | Wall | UNVERIFIED: no primary norm table retrieved. Within-person tracker only. | Yes |
| Grip strength (dynamometer) | Standard seated protocol, best of 3 per hand | Hand dynamometer | International norms from 2,405,863 adults, 69 countries: peak at age 30-39, 47.8 kg male and 29.7 kg female (absolute HGS). https://eprints.gla.ac.uk/339600/ China National Health Survey median 39 kg (33-44) men, 24 kg (20-27) women. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10235885/ | Only if they own a dynamometer. Most do not. |

On strength standards tables: ExRx says its tables are observed performance
data, not regression-derived
(https://exrx.net/WorkoutTools/StrengthStandards). Symmetric Strength and
StrengthLevel aggregate user-submitted training logs and competition results
(https://symmetricstrength.com/standards). The crowd-sourced sites have vastly
more data but a selection bias: people who log lifts on a strength website are
not the general population. Use ExRx for "is this normal for a human," and
Symmetric Strength or StrengthLevel for "is this normal for a lifter," and label
which one you used.

### 4.2 Cardio

| Test | Protocol | Equipment | Norms / equation | Self-administrable? |
|---|---|---|---|---|
| Talk test | During steady exercise, ask them to speak a sentence. The point where speech first becomes uncomfortable approximates ventilatory threshold. | None | "At the point where speech first became difficult, exercise intensity was almost exactly equivalent to ventilatory threshold on both treadmill and cycle." When speech was not comfortable, intensity was consistently above VT. https://pubmed.ncbi.nlm.nih.gov/15354048/ | Yes. Free, needs no equipment, and validated. The agent's default intensity anchor. |
| Cooper 12-minute run | Run/walk as far as possible in 12 min, record distance | Track or GPS | VO2max = (distance_m - 504.9) / 44.73. Developed by Kenneth Cooper in 1968 for the US Air Force. Correlates with lab VO2max within about +/-10% in trained runners; weaker in untrained or older people because pacing inexperience adds noise. https://www.topendsports.com/testing/tests/cooper.htm | Yes, if screening cleared vigorous exercise. Hard maximal effort, so gate it on the ACSM algorithm. |
| Rockport 1-mile walk | Walk 1 mile as fast as possible, take HR immediately at the finish | Measured mile, HR monitor, scale | VO2max = 132.853 - (0.0769 x weight_lb) - (0.3877 x age) + (6.315 x sex) - (3.2649 x time_min) - (0.1565 x HR), sex = 1 male, 0 female. Kline et al. 1987, n=343 adults aged 30-69, r = 0.88 with measured VO2max. https://pubmed.ncbi.nlm.nih.gov/3600239/ | Yes. The right first cardio test for a deconditioned adult. Submaximal. |
| 1.5-mile run | Run 1.5 miles for time | Track or GPS | UNVERIFIED: no primary norm table retrieved. Widely used in military and public safety testing. | Yes, maximal, same gating as Cooper. |
| YMCA 3-minute step test | Step up and down a 12-inch bench at 24 steps/min (metronome 96 bpm) for 3 min, then count HR for a full minute starting within 5 s of stopping | 12-inch bench, metronome, timer | Score is the 1-minute recovery HR. "Excellent" is under 81 bpm for men and under 85 for women per the YMCA manual classifications. https://www.topendsports.com/testing/tests/step-ymca.htm | With care. Needs an exact 12-inch step and a metronome. Cadence errors wreck it. |
| Submaximal cycle (Astrand-Rhyming, YMCA bike) | Fixed workloads with steady-state HR at each stage | Cycle ergometer with known watts | UNVERIFIED: I did not retrieve the nomogram or the YMCA multi-stage protocol from a primary source. | No. Needs a calibrated ergometer and a supervisor. |
| Resting HR | On waking, before getting up, 60 s count or wearable | Optional wearable | Track the trend, not the absolute. | Yes |
| HR max | Do not test it. Estimate. | None | Tanaka: HRmax = 208 - 0.7 x age, from group means across 351 studies (n=18,712), cross-validated in 514 healthy adults aged 18-81. HRmax "is predicted, to a large extent, by age alone and is independent of gender and habitual physical activity status." Tanaka has a smaller standard error than 220-age across most adult ages, and 220-age underestimates in over-50s. https://www.sciencedirect.com/science/article/pii/S0735109700010548 | Yes, it is arithmetic. |
| Heart rate recovery | HR at 1 min after stopping a hard effort, subtracted from peak HR | HR monitor | UNVERIFIED: I did not retrieve the primary source for the commonly cited <=12 bpm abnormal threshold (Cole et al., NEJM 1999). Verify before use. | Yes |

Note: any age-predicted HRmax has a standard deviation of roughly 10 to 12 bpm
around the estimate, so HR zones built from it are approximate for any one
person. The talk test is more individualised and costs nothing. UNVERIFIED on
the exact SD figure.

### 4.3 Power and athleticism (brief)

| Test | Protocol | Equipment | Norms | Self-administrable? |
|---|---|---|---|---|
| Countermovement vertical jump | Standing reach, then max jump with arm swing, difference is the jump | Wall and chalk, or an app | Adult men average 41-50 cm, women 31-40 cm, off two legs with full arm swing. https://www.topendsports.com/testing/norms/vertical-jump.htm | Yes, roughly. Phone flight-time apps introduce error. |
| Standing broad jump | Two-foot take-off and landing, measure heel to line | Tape measure | UNVERIFIED: no primary norm table retrieved. | Yes |
| Sprint splits (10 m, 20 m, 40 m) | Timed sprints from a static start | Timing gates, or video at known frame rate | UNVERIFIED: hand timing adds roughly 0.2 s bias versus gates. Verify. | Poorly. Hand timing is not comparable to gate timing, so do not mix them across re-tests. |

Only test power if the goal calls for it. Slice 09 owns the sport-specific case.

### 4.4 Body measurements

| Measure | Protocol | Interpretation | Self-administrable? |
|---|---|---|---|
| Bodyweight | Same scale, same time of day, ideally on waking after the toilet | Use a 7-day rolling average, never a single reading. Daily swings of 1-2 kg from water and gut content are normal. | Yes |
| Waist circumference | At the navel, at the end of a normal exhale, tape snug not tight | WHO: men <94 cm low risk, 94-102 high, >102 very high. Women <80 low, 80-88 high, >88 very high. https://www.iarc.who.int/news-events/who-guidelines-on-waist-circumference-and-physical-activity-and-their-joint-association-with-cancer-risk/ | Yes |
| Other circumferences (arm, thigh, chest, hips) | Same landmark each time, note the landmark | No norms needed. Useful because they move when scale weight does not. | Yes, though the tape angle is a real error source. |

### 4.5 Body composition and its error

Every field method disagrees with DXA, and DXA itself is not a criterion.

- BIA "has poor accuracy in estimating body fatness or body water content, with
  studies reporting large errors in estimates of up to ~5%," and results are
  heavily influenced by hydration status.
  https://www.mysportscience.com/post/body-composition-methods-validity-and-reliability
- Against DXA, "BIA, ADP, and skinfold equations exhibited poor agreement with
  DXA and significantly underestimated %FM_DXA, with systematic biases ranging
  from -1.8% to -10.7% in both men and women." BIA overestimated fat-free mass
  by 3.1 kg (SD 2.4, +7.2%) and underestimated fat mass by 2.9 kg (2.3, -13.0%).
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12821461/
- Skinfolds can be reliable "if the same measurer is used each time and a
  standard protocol is adhered by," with adequate training. That condition is
  exactly what a chat agent cannot supply.
  https://www.mysportscience.com/post/body-composition-methods-validity-and-reliability

Agent policy: do not report a body fat percentage. Track the sum of skinfolds or
the circumferences as raw numbers if the client wants a composition proxy. A
number that is wrong by 5 to 10 percentage points but delivered with two decimal
places is worse than no number, and for some clients it is actively harmful.

### 4.6 Readiness and recovery baselines

| Marker | How to baseline | Interpretation | Self-administrable? |
|---|---|---|---|
| HRV (lnRMSSD) | Daily or 4-5 readings per week, same time on waking. Establish a rolling 7-day average. "You need at least 14 days, ideally 28, to establish a reliable personal baseline." | Compare today's reading to the 7-day rolling average against a smallest worthwhile change, commonly the baseline mean +/- 0.5 x SD, or 0.5-1.0 x the within-athlete coefficient of variation. Popularised by Buchheit and Plews. https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2025.1578478/full https://marcoaltini.substack.com/p/a-brief-history-of-heart-rate-variability | Yes, with a chest strap or a phone camera app. Wrist optical HRV is noisier. |
| Session RPE | Ask for a single 0-10 rating of the whole session, 20-30 min after it ends. Multiply by session minutes for load. | Foster's modified CR-10, with verbal anchors changed to American idiomatic English. Validity and reliability confirmed across sports, ages, and expertise levels in 36 studies. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5673663/ | Yes. The single highest value-per-token question in the whole system. |
| Sleep | Hours and a 1-5 quality rating, daily | Trend against their own baseline | Yes |
| Soreness | 0-10 per body region, pre-session | UNVERIFIED: I did not retrieve a primary validated DOMS scale. A 0-10 numeric rating is standard practice but I would not claim published validation for it. | Yes |
| Readiness / RPE of the day | "0-10, how ready do you feel to train today?" pre-session | Combine with soreness and sleep. Any two of three flagged means cut volume before cutting intensity. | Yes |

---

## 5. Training age classification

Rippetoe's definition is about adaptation rate, not years in the gym. That is
the right axis, because it maps directly onto how often you can add load.

| Class | Definition | Adds weight | Programming consequence |
|---|---|---|---|
| Novice | "A trainee for whom the stress applied during a single workout and the recovery from that single stress is sufficient to cause an adaptation by the next workout." | Session to session | Linear progression. No periodisation. Test nothing beyond a working set, because every session is a PR. Plateau typically arrives between month 3 and month 9. |
| Intermediate | "One for whom the stress-recovery-adaptation cycle takes a full week," because the loads needed to force adaptation require recovery "substantially longer than 48-72hrs." | Week to week | Weekly organisation, light/medium/heavy days, or wave loading. |
| Advanced | Adaptation requires accumulating stress over months. | Month to month or longer | Block or conjugate periodisation, planned peaks. |

Sources: https://startingstrength.com/article/intermediate-and-advanced-training-a-few-ideas
https://www.barbellmedicine.com/blog/novice-intermediate-advanced-strength-training/

Helms uses the same three tiers and attaches expected rates of gain in
bodyweight: roughly 1-1.5% of bodyweight per month for beginners, 0.5-1% for
intermediates, and up to 0.5% for advanced lifters, who should judge progress by
strength in the gym rather than by scale weight.
https://www.amazon.com/Muscle-Strength-Pyramid-Training/dp/109091282X (The
Muscle and Strength Pyramid: Training, 2nd ed., Helms, Morgan, Valdez)

How the agent classifies without a test: ask C1, C2, and C3. Someone who has
been lifting under 3 months, or who has been away over 6 months, gets treated as
a novice regardless of their history. Someone who reports that their lifts
stopped moving every session goes to intermediate. Advanced classification
should require both the training history and a strength standard in the advanced
band on the ExRx table. Do not let people self-declare advanced.

UNVERIFIED: I did not retrieve NSCA Essentials of Strength Training and
Conditioning's own training-status classification (it uses a beginner /
intermediate / advanced framing tied to training experience in months plus
technique proficiency). Quote it from the book's chapter on program design
before shipping.

---

## 6. Re-test cadence

| Category | Cadence | What to re-test | Trigger for an off-cycle re-test |
|---|---|---|---|
| PAR-Q+ | 12 months | All of it. The form's own declaration caps validity at 12 months. | Any health change, any new diagnosis, any new medication, pregnancy, injury |
| Intake questions (blocks C-G) | 12 weeks | Schedule, equipment, goals, preferences | Job change, move, new gym, life event |
| Strength (estimated 1RM) | 8-12 weeks, at a block boundary | The same lifts, same rep count, same conditions | Plateau, or a big change in bodyweight |
| Bodyweight strength (push-up, plank, hang) | 8-12 weeks | Same | Same |
| Cardio field test | 8-12 weeks | Same test, same route, same conditions | Goal change |
| Mobility screens | 12 weeks | Only the ones you are actively addressing | New pain, new movement restriction |
| Body measures | Weekly for weight (7-day average), 4 weeks for circumferences | Same landmarks | Nothing |
| Blood pressure | 12 weeks if normal, more often if stage 1 or above | Same conditions, seated, after 5 min rest | Symptoms |
| HRV / sleep / RPE | Continuous | These are not tests, they are inputs | Nothing |

Rule: re-test at block boundaries, not mid-block. Testing costs a session and
adds fatigue. If the answer will not change the program, do not run the test.

---

## 7. What the agent can and cannot do

### Can do over chat, no video

- All of PAR-Q+ and the whole intake script.
- Estimated 1RM from a client-reported rep-max on lifts they already do safely.
- Push-ups, plank, dead hang, wall sit, bodyweight squat count.
- Knee-to-wall ankle measurement (tape measure).
- Talk test, resting HR, session RPE, sleep, soreness, HRV, readiness.
- Bodyweight, waist, circumferences.
- Cooper or Rockport, if screening cleared the intensity.
- Blood pressure, if they own a cuff, with the caveat that it is self-reported.
- Training-age classification.

### Needs video

- Squat pattern assessment and its compensations.
- Single-leg squat, step-down.
- Shoulder mobility reach.
- Technique check on any barbell lift before trusting a reported rep-max.
- Modified Thomas test, with the reliability caveat from 3.2.

Video gets you range of movement, strength and endurance, and functional
measures at acceptable validity. It does not get you special orthopaedic tests,
neurodynamic tests, or lumbar posture at better than low-to-moderate validity,
and diagnostic agreement with in-person assessment runs 59.7% to 93.3%.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8684795/

### Must skip

- Any true 1RM attempt in a novice, or any 1RM without a rack or spotter.
- Full FMS scoring. It needs a trained rater and a kit, and it does not predict injury anyway.
- Body fat percentage from any method.
- Skinfolds. The reliability condition is a single trained measurer, which does not exist here.
- Graded exercise testing of any kind.
- Hip internal and external rotation goniometry. Needs a second person.
- Any interpretation of a symptom as a diagnosis.
- Maximal testing of anyone the ACSM algorithm routed to medical clearance.

---

## 8. Safety: what triggers "get cleared by a clinician first"

Hard stops. The agent writes no program until these resolve.

1. Any YES on PAR-Q+ pages 1 through 3 that is not resolved by the follow-ups.
   The form's own instruction: "You should seek further information before
   becoming more physically active or engaging in a fitness appraisal."
2. Chest pain at rest, during daily activity, or on exertion. PAR-Q+ Q2.
3. Loss of balance from dizziness, or loss of consciousness in the last 12
   months. PAR-Q+ Q3.
4. A doctor has said they should only do medically supervised activity.
   PAR-Q+ Q7.
5. Not currently exercising, plus known cardiovascular, metabolic, or renal
   disease, or signs and symptoms of it. ACSM algorithm.
   https://pubmed.ncbi.nlm.nih.gov/26473759/
6. Symptoms appearing during exercise in someone who was exercising. ACSM
   algorithm says stop exercising and get clearance.
7. Known disease and wanting to progress to vigorous intensity. Clearance first.
8. Blood pressure at stage 2 (>=140 systolic or >=90 diastolic) on a reliable
   reading. Refer, and keep training light to moderate in the meantime.
   https://www.ahajournals.org/doi/10.1161/hyp.0000000000000065
9. Pregnancy. PAR-Q+ names it explicitly as a delay condition.
10. Current illness with fever. PAR-Q+ delay condition.
11. Pain during any screening movement, which is an FMS score of 0. Not a
    diagnosis, a referral.
12. Night pain, unexplained weight loss, numbness, tingling, bowel or bladder
    change, or pain that does not change with position or activity. These are
    the standard musculoskeletal red flags. UNVERIFIED: I did not retrieve a
    primary source for this red-flag list in this pass. Cite it properly (for
    instance from a clinical practice guideline for low back pain) before
    shipping. Slice 10 should own it.

Also: the PAR-Q+ clearance is not permanent. It expires at 12 months and
"becomes invalid if my condition changes." The agent must re-ask, and must treat
any newly reported diagnosis or medication as invalidating the stored clearance.

---

## 9. Fields to store

One `athlete_profile` record. Every group carries its own `measured_at`, because
a 6-month-old squat estimate and a yesterday's sleep score are not the same kind
of fact.

```
screening:
  parq: {q1..q7: bool, followups: {...}, outcome: cleared|followup|refer,
         completed_at: date, expires_at: date, invalidated_by: string?}
  acsm: {currently_active: bool, known_disease: bool, signs_symptoms: bool,
         target_intensity: light_mod|vigorous, clearance_required: bool}
  clinician_clearance: {status, obtained_at, notes}

goal:
  goal_statement, goal_primary, goal_secondary, goal_trigger,
  ttm_stage, confidence_0_10

history:
  lifting_months, lifting_consistency, current_days_per_week, current_intensity,
  competent_lifts[], known_lifts[], cardio_recent_max, program_history,
  training_age: novice|intermediate|advanced, training_age_basis

constraints:
  available_days[], session_minutes, training_location, equipment[],
  dumbbell_max_kg, schedule_constraints

health:
  pain_sites[], injury_history[], excluded_movements[], hr_affecting_meds,
  pregnancy_status, acute_illness

body:
  height_cm, bodyweight_kg (series), waist_cm, circumferences{}, 
  bp_systolic, bp_diastolic, bp_measured_at

baseline_strength[]:
  {lift, test_type: rep_max|amrap|max_reps|hold, load_kg, reps, rpe,
   e1rm_epley, e1rm_brzycki, standard_band, standard_source, measured_at}

baseline_cardio[]:
  {test, raw_result, vo2max_estimate, equation, hr_end, measured_at}

baseline_mobility[]:
  {test, side, value, unit, pain: bool, video_reviewed: bool, notes, measured_at}

readiness_daily[]:
  {date, sleep_hours, sleep_quality_1_5, stress_1_5, soreness{}, 
   readiness_0_10, resting_hr, hrv_lnrmssd, hrv_7d_avg}

session_load[]:
  {session_id, srpe_0_10, minutes, load = srpe * minutes}

preferences:
  likes[], dislikes[], verbosity_pref, coaching_tone
```

Two design notes:

- Store the raw inputs alongside the derived value. An estimated 1RM without the
  load, reps, and formula is unauditable and cannot be recomputed when you
  change formulas.
- `standard_source` matters. "Intermediate on ExRx" and "intermediate on
  Symmetric Strength" are different claims about different populations.

---

## 10. Open questions for the user

1. Do you want the agent to insist on the full PAR-Q+ verbatim, including
   question 5 about prescribed medications? It is the correct thing to do and
   the licence requires it, but it is a heavy first interaction. Alternative:
   present it as a one-off form the user fills in themselves, and have the agent
   only read the outcome.
2. How much does the agent test at all? There is a version of this that does no
   baselining beyond intake, starts everyone conservatively, and uses the first
   three weeks of logged sets as the baseline. That is arguably better than a
   test day, and much better for someone with ADHD who will not do a
   test-battery session. Which do you want as the default?
3. Video: is that in scope for this tool at all? A lot of section 3 collapses if
   the answer is no. Section 7 already assumes the answer might be no.
4. Do you want body composition and body fat estimation excluded entirely, as I
   have recommended, or available behind an explicit opt-in?
5. What is the escalation path when the screening says "see a clinician"? Does
   the agent refuse to write anything, write a very conservative walking-only
   plan, or write the plan and gate it behind a user-confirmed clearance flag?
6. Where does the intake output live? Slice 06 named a `config/athlete.md` and a
   `config/limits.md`. Section 9 above is richer than either. Does it become
   structured data, or stay Markdown the agent reads?
7. Do you want the ExRx tables, the Symmetric Strength percentiles, or both
   stored locally, or does the agent look them up each time? Both are
   third-party and could move.

---

## 11. Evidence health check

Strong and directly quotable: PAR-Q+ 2025 (primary PDF), ACC/AHA 2017 blood
pressure categories, FMS injury prediction meta-analyses, Kline 1987 Rockport
equation, Tanaka 2001 HRmax, talk test validation, session RPE validation, grip
strength international norms, telehealth assessment validity, weight-bearing
lunge test norms and reliability, TTM stages.

Weak or unverified, listed in place above and repeated here so nothing hides:

- ACSM algorithm figure, "regular exercise" definition, and intensity bands. The
  ACSM PDF link is dead and the book is paywalled. Everything in section 1.2
  routes through secondary summaries of the Riebe 2015 paper.
- ACSM absolute contraindications list, reproduced from teaching material.
- Hypertensive crisis threshold.
- ACSM and CSEP push-up and sit-and-reach norm tables (paywalled), so the
  push-up numbers in 4.1 come from a secondary summary of CSEP-PATH.
- Cooper test age and sex norm tables. Only the equation is primary-sourced.
- 1.5-mile run norms, broad jump norms, wall sit norms, adult pull-up norms.
- Thoracic rotation and hip rotation norms.
- Heart rate recovery abnormal threshold (Cole 1999).
- Age-predicted HRmax standard deviation.
- Musculoskeletal red flag list.
- NSCA Essentials training-status classification.
- Sprint hand-timing bias.

The cheapest fix for most of this is one copy of ACSM's Guidelines for Exercise
Testing and Prescription, 11th ed., and one copy of NSCA's Essentials of
Strength Training and Conditioning, 4th ed. Roughly half the unverified list
collapses.
