# Medical conditions and special populations: how programming changes, and when to stop

Research slice 10. Written 2026-08-31.

Sibling slices: 07 baselining, 08 goal-specific programming, 09 sport-specific,
11 transgender athletes (not covered here), 12 trainer practice and ethics.
This file covers medical conditions and special populations only.

Every card below is written to be read by an agent mid-conversation. Same six
fields each time, same order. Numbers are quoted from the source, not rounded
or softened. Where I could not verify a number against a primary source in the
time available it is tagged `UNVERIFIED`.

---

## TL;DR

Global red flags. Any of these: stop the session now, refer, do not resume.

1. Chest pain, pressure, or discomfort at rest or on exertion.
2. Sudden shortness of breath out of proportion to the work.
3. Fainting, near-fainting, unexplained dizziness, new palpitations.
4. New one-sided weakness, facial droop, slurred speech, sudden severe headache.
5. Resting BP 180/110 mmHg or higher, measured and repeated.
6. Calf pain or swelling on one side, or a new hot swollen joint.
7. Saddle numbness, bladder or bowel change, progressive leg weakness.
8. Vaginal bleeding, fluid leak, or reduced fetal movement in pregnancy.
9. Blood glucose at or below 70 mg/dL (3.9 mmol/L), or confusion and sweating in a diabetic client.
10. Symptoms crashing 12 to 72 hours after activity. Stop all progression.
11. Clearance workflow: screen at intake on current activity, known cardiac/metabolic/renal disease, signs and symptoms, and planned intensity (ACSM 2015); get written clearance where indicated; then train only inside what the clinician wrote.

---

## How to use this file

- The agent reads the global red-flag list every session. It is not optional.
- Each card gives: what changes in FITT-VP, what to avoid, what to monitor,
  stop signs, when to refer, evidence quality, sources.
- FITT-VP = Frequency, Intensity, Time, Type, Volume, Progression.
- An agent must never diagnose, never tell anyone to change a medication dose,
  and never treat an injury. See "Scope of practice" below for the exact words.

---

## 1. Medical clearance workflow

### The ACSM 2015 screening algorithm

ACSM replaced risk-factor counting with a four-input decision in 2015. The
inputs are: current exercise participation, known cardiovascular, metabolic, or
renal disease, signs or symptoms of that disease, and the desired exercise
intensity. Referral for medical clearance follows from those four
(https://pubmed.ncbi.nlm.nih.gov/26473759/).

Two changes matter for an agent:

- Pulmonary disease alone no longer triggers automatic referral. A person with
  asthma or COPD and no cardiac, metabolic, or renal disease is not auto-referred
  by the algorithm (https://pubmed.ncbi.nlm.nih.gov/26473759/).
- The new algorithm refers about 41% fewer adults than the old one. That was the
  intent: fewer barriers to starting (https://pubmed.ncbi.nlm.nih.gov/28557860/).

The exact branch wording of the algorithm boxes is `UNVERIFIED`: the ACSM
Exercise is Medicine PDF now redirects to https://acsm.org/EIM and I could not
pull the boxes verbatim. Treat the four inputs as reliable and get the printed
algorithm from ACSM's Guidelines, 11th edition, chapter 2 before shipping it as
a decision tree.

### Agent-usable clearance rule

```
IF known CVD, metabolic (T1D/T2D), or renal disease
   AND currently not exercising regularly     -> clearance before ANY exercise
IF known CVD/metabolic/renal disease
   AND currently exercising regularly
   AND no signs/symptoms                      -> may continue moderate; clearance before vigorous
IF any sign/symptom of CVD/metabolic/renal disease (at rest or exertion)
   -> STOP. Clearance before continuing, at any intensity.
IF no known disease and no signs/symptoms     -> no clearance needed
```

Source for the shape of this: ACSM 2015 update
(https://pubmed.ncbi.nlm.nih.gov/26473759/). Exact wording `UNVERIFIED`.

### Absolute contraindications to exercise testing (and, by extension, to a
hard training session)

Acute MI within 2 days, ongoing unstable angina, uncontrolled arrhythmia with
haemodynamic compromise, active endocarditis, symptomatic severe aortic
stenosis, decompensated heart failure, acute pulmonary embolism, acute aortic
dissection, acute myocarditis or pericarditis, and recent stroke or TIA. Resting
systolic above 200 mmHg or diastolic above 110 mmHg is listed as a relative
contraindication in ACSM's table
(https://www.ncbi.nlm.nih.gov/books/NBK499903/,
https://www.utoledo.edu/policies/utmc/heart_station/pdfs/3364-106-S08.pdf).

Note the two different blood-pressure numbers, and do not blur them. 200/110 is
the testing threshold. 180/110 is the ACSM hypertension position-stand threshold
for "see your doctor first" before starting a programme (see card 2). An agent
should use the lower one.

### What a clearance letter must contain before the agent acts on it

Diagnosis or diagnoses considered, intensity ceiling if any, movements or
positions to avoid, monitoring required, date, and clinician name. A letter
that only says "cleared for exercise" is thin: proceed at moderate intensity and
ask the client to get the specifics.

---

## 2. Scope of practice

Quote these, do not paraphrase them, when a client pushes.

**ACE.** "Personal trainers cannot prescribe, diagnose or treat diseases, and
cannot prescribe diets, counsel, or rehabilitate clients."
(https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf)

**ACE, nutrition specifically.** "It is the position of ACE that it is outside
the defined scope of practice of a fitness professional to recommend, prescribe,
or supply nutritional supplements to clients." Also outside scope: "prescribe a
specific diet, conduct a robust dietary analysis (beyond a food log), and/or
provide medical nutrition therapy or nutrition counseling."
(https://www.acefitness.org/resources/pros/expert-articles/6248/nutrition-scope-of-practice-what-you-can-do-as-a-personal-trainer/)

**ACSM.** The ACSM Certified Personal Trainer works with "apparently healthy
clients and those with stable health challenges who have been cleared to
exercise independently"; the CPT "is qualified to plan and implement exercise
programs for healthy individuals or those who have medical clearance to
exercise" (https://acsm.org/certification/get-certified/). The exact current
scope-of-practice page wording is `UNVERIFIED`; the phrasing above comes from
ACSM certification pages and derived summaries.

**NSCA.** NSCA's Essentials of Personal Training notes that "Various states and
countries have different regulations governing whether or not personal trainers
can provide dietary advice, and personal trainers should follow these
guidelines"
(https://www.nsca.com/certification/nsca-cpt/essentials-of-personal-training--3rd-edition/excerpts/personal-trainers-and-nutrition-advice/).

**IDEA.** `UNVERIFIED`. I did not find a current IDEA scope-of-practice
statement in the time available. IDEA's HIPAA guidance for fitness pros exists
(https://www.ideafit.com/the-hipaa-effect/) but is not a scope statement.

### What an AI trainer-agent must refuse

Say no, plainly, to all of these:

- Naming a diagnosis for a symptom. "That sounds like a rotator cuff tear" is a
  diagnosis. So is "that's probably just DOMS" when it might not be.
- Telling anyone to take, skip, split, or change the timing of a medication,
  including insulin, beta blockers, and GLP-1 agonists.
- Interpreting a scan, a blood result, or an ECG.
- Designing rehab for an acute injury, a post-surgical client, or anyone under a
  physio's active care, without that clinician's written plan.
- Overriding a clearance letter, or persuading a client that they do not need one.
- Continuing a session after any global red flag appears.
- Giving meal plans, macro prescriptions, or supplement recommendations to a
  client with a medical condition.

### What the agent should say instead

One sentence, no hedging: "I can't assess that, and guessing would be worse than
useless. Stop the session, and get it looked at by [GP / physio / your diabetes
team / emergency care] before we train again. I'll hold the programme where it
is." Then log it.

---

## 3. Condition and population cards

Card template: **Adjust / Avoid / Monitor / Stop signs / Refer when / Evidence / Sources.**

---

### Hypertension

- **Adjust.** Most days, preferably all days of the week. Moderate intensity,
  defined by ACSM as 40% to below 60% of VO2 Reserve. 30 minutes or more per
  day, continuous or accumulated. Mostly endurance work, supplemented with
  resistance training. The antihypertensive effect is immediate and shows up
  after low-intensity, short-duration aerobic exercise.
- **Avoid.** Breath-holding and Valsalva under load. Heavy isometric holds
  without clearance. Sudden stops after hard work (post-exercise hypotension is
  real; cool down).
- **Monitor.** Resting BP at intake and periodically. Which drug class they are
  on. Beta blockers blunt heart rate, so switch intensity control to RPE (see
  card 25).
- **Stop signs.** Chest pain, severe headache, visual change, dizziness.
- **Refer when.** "Those with a resting blood pressure ≥180/110 mm Hg should be
  encouraged to see their physician for improved blood pressure control prior to
  beginning an exercise program."
- **Evidence.** Strong for aerobic exercise lowering BP. The ACSM position stand
  is 2004 and ACSM has since updated its pronouncement, so check the newer
  version before publishing numbers.
- **Sources.** https://journals.lww.com/acsm-msse/fulltext/2004/03000/exercise_and_hypertension.25.aspx ,
  https://acsm.org/exercise-hypertension/

---

### Type 1 diabetes

- **Adjust.** Exercise is safe but glucose management around it dominates the
  programme. Timing, insulin on board, and food matter more than set and rep
  choice. Carbohydrate guidance from the ADA position statement: "For low- to
  moderate-intensity aerobic activities lasting 30−60 min undertaken when
  circulating insulin levels are low (i.e., fasting or basal conditions),
  approximately 10−15 g of carbohydrate may prevent hypoglycemia." For work done
  after a bolus, "30−60 g of carbohydrate per hour of exercise may be needed."
- **Avoid.** Training alone when hypo-unaware. Training without fast carbs
  within arm's reach. Long endurance work at the peak of a bolus without a plan
  from their diabetes team.
- **Monitor.** Glucose before, during long sessions, and after. Hypo can arrive
  hours later, including overnight. Ask about hypoglycaemia unawareness at
  intake. Resistance work and high-intensity intervals often raise glucose
  acutely while steady aerobic work lowers it, so the same client can need
  opposite handling on different days.
- **Stop signs.** Glucose at or below 70 mg/dL (3.9 mmol/L) is the ADA's
  hypoglycaemia alert value and is treated with fast-acting carbohydrate. Shaking,
  sweating, confusion, blurred vision, sudden mood change: stop, treat, do not
  restart that session.
- **Refer when.** Any hypo needing another person's help. Repeated unexplained
  hypos. Hypo unawareness. Ketones present. New retinopathy, neuropathy, or
  nephropathy. The agent never sets insulin doses; that is the diabetes team.
- **Evidence.** Strong for benefit, strong consensus on carbohydrate handling,
  high individual variability. The ADA statement itself says variable glycaemic
  responses "make uniform recommendations for management of food intake and
  insulin dosing difficult".
- **Sources.** https://diabetesjournals.org/care/article/39/11/2065/37249/Physical-Activity-Exercise-and-Diabetes-A-Position ,
  https://diabetes.org/health-wellness/fitness/exercise-and-type-1 ,
  https://diabetesjournals.org/care/article/48/Supplement_1/S128/157561/6-Glycemic-Goals-and-Hypoglycemia-Standards-of

Common thresholds an agent will see quoted (avoid exercise above 250 mg/dL with
ketones; take carbs below 90 mg/dL before starting) are `UNVERIFIED` against the
2016 position statement full text. The PDF I fetched did not parse. Verify from
Diabetes Care 39(11):2065 before hard-coding them.

---

### Type 2 diabetes

- **Adjust.** Aerobic plus resistance, both. Combined training beats either alone
  for glycaemic control. Do not go more than two consecutive days without
  activity; the glucose-lowering effect of a session fades. Reducing sitting
  time matters on its own.
- **Avoid.** Nothing categorical for most clients. Where retinopathy, neuropathy,
  or nephropathy is present, see those cards and get clearance.
- **Monitor.** Glucose if on insulin or a sulfonylurea, because those are the
  drugs that cause hypos. Metformin alone rarely does. Feet, always (see
  peripheral neuropathy). Blood pressure.
- **Stop signs.** Same as type 1 for hypo symptoms. Chest pain: type 2 diabetes
  raises silent ischaemia risk, so treat unusual breathlessness or jaw/arm
  discomfort as cardiac until proven otherwise.
- **Refer when.** Starting vigorous exercise while sedentary with known diabetes
  (per the 2015 ACSM algorithm). Any foot wound. Unexplained exertional symptoms.
- **Evidence.** Strong.
- **Sources.** https://diabetesjournals.org/care/article/39/11/2065/37249/Physical-Activity-Exercise-and-Diabetes-A-Position

---

### Obesity

- **Adjust.** The dose for weight loss is higher than the dose for health. ACSM's
  2009 position stand: 150 to 250 min/week of moderate-to-vigorous activity
  prevents weight gain and produces modest loss; "greater weight loss and
  enhanced prevention of weight regain" comes at "250 to 300 min/wk
  (approximately 2000 kcal/wk) of moderate intensity physical activity", and
  programmes need to exceed 225 min/week to produce clinically significant loss.
  Resistance training preserves lean mass but does not add much to weight loss
  on its own.
- **Avoid.** Framing every session as a calorie burn. High-impact plyometrics as
  a starting point (joint load, and it fails on adherence). Weighing every
  session by default.
- **Monitor.** Joint symptoms, especially knees. Skin chafing and heat tolerance.
  Perceived exertion rather than absolute pace. Adherence, which is the actual
  constraint.
- **Stop signs.** Exertional chest pain or breathlessness at low workloads.
- **Refer when.** Comorbid CVD, T2D, or sleep apnoea plus vigorous intent.
  Suspected eating disorder (see that card; restriction and bingeing occur across
  all body sizes).
- **Evidence.** Strong for the dose-response, weak for exercise alone as a
  weight-loss method.
- **Sources.** https://www.medscape.com/viewarticle/717049 ,
  https://obesitymedicine.org/blog/how-much-physical-activity-is-needed-for-weight-loss-weight-loss-maintenance-and-weight-gain-prevention/

---

### Cardiovascular disease and post-cardiac event

- **Adjust.** Cardiac rehab first, personal training second. A trainer's job
  starts when the client is discharged from a supervised programme with a
  prescription. Post-sternotomy, upper-limb resistance training has traditionally
  been delayed "for a minimum of 6–8 weeks following cardiac surgeries such as
  median sternotomy to prevent sternal instability", though recent work suggests
  early resistance training is no riskier than coughing. Sternal stability must
  be assessed by a clinician before upper-body loading.
- **Avoid.** Progressing without the rehab team's ceiling. Maximal testing.
  Valsalva. Cold-weather high-intensity work in angina-prone clients.
- **Monitor.** RPE (heart rate is unreliable on beta blockers), symptoms, and
  the clinician's prescribed heart-rate or workload ceiling. Whether GTN spray is
  present and in date.
- **Stop signs.** Any angina. New or worsening breathlessness. Palpitations.
  Light-headedness. An ICD shock.
- **Refer when.** Anything new. Post-MI, post-stent, post-CABG clients are
  referral-first, programme-second.
- **Evidence.** Strong for supervised cardiac rehab. Moderate for early
  resistance training post-sternotomy, and it is an active argument.
- **Sources.** https://www.ahajournals.org/doi/10.1161/CIR.0000000000001289 ,
  https://www.ahajournals.org/doi/10.1161/01.cir.101.7.828 ,
  https://academic.oup.com/eurjcn/article/25/1/198/8443015

---

### Asthma and exercise-induced bronchoconstriction

- **Adjust.** Warm up properly. The ATS guideline recommends "interval or
  combination warm-up exercise before planned exercise for all patients with
  exercise-induced bronchoconstriction". Longer, gradual warm-ups reduce the
  bronchoconstriction response.
- **Avoid.** Training without the reliever inhaler present. Cold dry air and high
  pollen or chlorine exposure in symptomatic clients.
- **Monitor.** Inhaler present and in date. Symptom pattern by environment.
  Whether they needed the reliever, and how often.
- **Stop signs.** Wheeze, chest tightness, or cough not relieved by their
  reliever. Any reliever use that does not work within minutes is an emergency.
- **Refer when.** Reliever needed more than usual, symptoms waking them at night,
  or worsening exercise tolerance. The trainer does not adjust asthma medication.
  The ATS makes "a strong recommendation ... for using a short-acting β2-agonist
  before exercise in all patients with EIB", typically 15 minutes before, but
  that is the prescriber's call, not the trainer's.
- **Evidence.** Strong (ATS clinical practice guideline, 2013).
- **Sources.** https://www.thoracic.org/statements/resources/allergy-asthma/exercise-induced-bronchoconstriction.pdf ,
  https://pubmed.ncbi.nlm.nih.gov/23634861/

---

### COPD

- **Adjust.** Pulmonary rehabilitation is the evidence base. "Patients should
  perform exercise at least three times per week, and regular supervision of
  exercise sessions is necessary to achieve optimal physiologic benefits."
  Longer programmes beat shorter ones: 7 weeks beat 4, and 20 sessions beat 10.
  Interval work lets a breathless client accumulate more total work than
  continuous work does.
- **Avoid.** Intensity set by heart rate alone. In COPD, ventilation limits the
  session before the heart does.
- **Monitor.** Dyspnoea rating (modified Borg CR10), oxygen saturation if the
  client has a pulse oximeter and their clinician asked for it, recovery between
  intervals.
- **Stop signs.** Desaturation below the clinician's stated floor. Distress that
  does not settle within a couple of minutes of stopping. Chest pain.
- **Refer when.** Exacerbation (increased sputum, colour change, more
  breathlessness). Any client not yet through pulmonary rehab.
- **Evidence.** Strong (ATS/ERS statements 2006 and 2013).
- **Sources.** https://www.thoracic.org/statements/resources/respiratory-disease-adults/atserspr0606.pdf ,
  https://www.thoracic.org/statements/resources/copd/PRStatementrccm-2E201309-1634st.pdf

---

### Osteoporosis and osteopenia

- **Adjust.** Load the bone. ESSA's position statement: "bone responds positively
  to impact activities and high intensity progressive resistance training." Add
  balance and mobility work, because "optimisation of muscle strength, balance
  and mobility minimises the risk of falls (and thereby fracture)". Programmes
  should be accompanied by sufficient calcium and vitamin D.
- **Avoid.** "loaded spine flexion is not recommended." That rules out weighted
  sit-ups, loaded toe-touches, heavy rounded-back lifting, and machine trunk
  flexion. Impact work "may require modification in the presence of
  osteoarthritis or frailty".
- **Monitor.** Fracture history, height loss, back pain of new onset, falls.
- **Stop signs.** Sudden localised back pain after a lift or a fall: possible
  vertebral fracture, stop and refer same day.
- **Refer when.** Recent fracture, unexplained new back pain, high fracture risk
  with no prior supervised programme.
- **Evidence.** Strong and, importantly, the modern position is the opposite of
  the old "be careful, stay light" advice. High-intensity loading is the point.
- **Sources.** https://pubmed.ncbi.nlm.nih.gov/27840033/ ,
  https://ro.ecu.edu.au/ecuworkspost2013/2797/

---

### Osteoarthritis

- **Adjust.** Exercise is first-line treatment, not an adjunct. OARSI 2019 core
  treatments for knee OA: arthritis education plus structured land-based exercise,
  with or without dietary weight management. ACR strongly recommends aquatic
  exercise and land-based aerobic and resistance exercise for knee OA, and
  includes tai chi.
- **Avoid.** Waiting for pain to be zero before loading. Long rest. Telling the
  client their joint is "bone on bone" (that framing worsens outcomes).
- **Monitor.** Pain during and 24 hours after. A short-lived rise that settles by
  the next day is acceptable; a sustained rise means the dose was too big.
- **Stop signs.** Joint locking, giving way, hot swollen joint, or fever.
- **Refer when.** Locking or true instability, rapid deterioration, or a red hot
  joint (septic arthritis is an emergency).
- **Evidence.** Strong.
- **Sources.** https://pubmed.ncbi.nlm.nih.gov/31278997/ ,
  https://www.esceo.org/sites/esceo/files/pdf/Bannuru_O&C_OARSIguidelines_2019.pdf ,
  https://www.the-rheumatologist.org/article/updated-oarsi-guideline-for-the-non-surgical-management-of-osteoarthritis/

---

### Rheumatoid arthritis

- **Adjust.** Regular aerobic and resistance training is recommended and does not
  damage joints. During a flare, reduce load and keep range of motion; do not
  stop moving entirely.
- **Avoid.** Heavy loading of an actively inflamed joint. High-impact work in
  clients with joint erosion or prosthesis, unless cleared.
- **Monitor.** Flare status, morning stiffness duration, fatigue, medication
  changes (steroids affect tendon and bone).
- **Stop signs.** Hot swollen joint with fever. Sudden loss of function.
- **Refer when.** Flares that keep recurring, new joint deformity, suspected
  cervical spine involvement (a real risk in longstanding RA and a reason to
  avoid loaded neck positions without clearance).
- **Evidence.** Moderate. `UNVERIFIED`: I did not retrieve the EULAR
  recommendations text on flares in the time available. Get EULAR's physical
  activity recommendations for inflammatory arthritis before publishing specifics.
- **Sources.** https://www.sciencedirect.com/science/article/pii/S1063458423008324

---

### Chronic low back pain

- **Adjust.** Exercise is first-line. NICE NG59: "Consider a group exercise
  programme (biomechanical, aerobic, mind–body or a combination of approaches)
  within the NHS for people with a specific episode or flare-up of low back pain
  with or without sciatica", and clinicians should "take people's specific needs,
  preferences and capabilities into account when choosing the type of exercise".
  No single exercise type wins. Pick what the person will do.
- **Avoid.** Bed rest. Fear-based cueing about "fragile" spines. Insisting on one
  posture as correct.
- **Monitor.** Function, not just pain. Sleep. Whether pain is centralising or
  spreading down the leg.
- **Stop signs.** These are the red flags NICE and the guideline reviews name:
  saddle anaesthesia, bladder or bowel dysfunction, progressive neurological
  deficit (cauda equina, an emergency), fever with back pain (possible spinal
  infection), unexplained weight loss (possible malignancy), pain worse at night
  or at rest, new lump or swelling, and thoracic pain between the shoulders.
- **Refer when.** Any of the above. Also refer if pain is not improving over
  weeks despite sensible loading.
- **Evidence.** Strong for exercise as first-line, weak for any specific method
  being superior.
- **Sources.** https://www.nice.org.uk/guidance/ng59/resources/low-back-pain-and-sciatica-in-over-16s-assessment-and-management-pdf-1837521693637 ,
  https://www.ncbi.nlm.nih.gov/books/NBK562933/

---

### Hypermobility spectrum disorder and hEDS

- **Adjust.** Low to moderate impact aerobic work plus low-load strengthening and
  proprioceptive training. Progress slowly. Closed-chain and proprioceptive work
  over eight weeks improved proprioception and pain in hEDS clients aged 16 to 49.
- **Avoid.** The old blanket advice to never move into end range has been
  superseded. Physiotherapy management "has shifted from advice to not move
  hypermobile joints into end-range, to advice to progress exercises so as to
  develop joint control in the hypermobile range". So: build control in range
  rather than fencing it off. Still avoid passive stretching into hypermobile
  range and ballistic end-range loading.
- **Monitor.** Subluxations and dislocations. Fatigue and delayed soreness, which
  is often disproportionate. Autonomic symptoms (POTS overlaps heavily with hEDS,
  see next card). Skin and wound healing if relevant.
- **Stop signs.** Joint subluxation during a session. Sharp new pain. Presyncope.
- **Refer when.** Recurrent dislocations, suspected but undiagnosed hEDS,
  significant autonomic or gastrointestinal symptoms. Also flag the vascular EDS
  subtype: it is a different disease with vascular rupture risk and needs
  specialist clearance before any loading.
- **Evidence.** Weak to moderate. Small studies, heterogeneous populations, no
  large trial. Practice is ahead of the evidence.
- **Sources.** https://www.ehlers-danlos.org/information/exercise-and-movement-for-adults-with-hypermobile-ehlers-danlos-syndrome-and-hypermobility-spectrum-disorders/ ,
  https://www.ehlers-danlos.org/information/physical-therapy-for-hypermobility/

---

### POTS and dysautonomia

- **Adjust.** Start horizontal. The Levine (Dallas) protocol is a structured
  progressive programme built at UT Southwestern that begins with recumbent-only
  work (recumbent bike, rowing, swimming) and moves to upright work as tolerance
  improves, over roughly three to seven months. Recumbent-first exists because
  standing itself is the trigger. Add lower-body and core strength work.
- **Avoid.** Prolonged standing, hot rooms, hot showers immediately after,
  overhead work early, and rapid position changes. Vigorous upright cardio at the
  start.
- **Monitor.** Heart rate on position change. Hydration and salt (their clinician
  sets the target, not the trainer). Symptoms in the 24 hours after, since some
  POTS clients also have post-exertional malaise, which changes the whole plan
  (see long COVID / ME-CFS card).
- **Stop signs.** Presyncope, syncope, chest pain, vision greying.
- **Refer when.** Undiagnosed orthostatic symptoms. Syncope. Rapid deterioration.
  A POTS diagnosis needs a clinician, not a heart-rate monitor.
- **Evidence.** Moderate for exercise training in POTS, weak on the exact
  protocol version. The 2015 Heart Rhythm Society expert consensus statement on
  POTS is the standard clinical reference; I did not verify its exercise wording
  and mark it `UNVERIFIED`.
- **Sources.** https://www.eds.clinic/articles/exercise-pots-dallas-levine--chop-protocols ,
  https://www.jimharrismd.com/articles/exercise-for-pots-chop-protocol-dallas-protocol-and-levine-protocol
  (both secondary; get Fu & Levine's primary papers before shipping)

---

### Long COVID and ME/CFS

This is the card most likely to cause harm if the agent applies a normal
progression rule. Read it twice.

- **Adjust.** Pacing, not progression. Post-exertional malaise or PESE means
  symptoms worsen after activity that exceeds capacity, "including fatigue, pain
  and cognitive impairment that often occur between 24 and 72 hours after the
  activity", with reported prevalence around 86% in long COVID cohorts. The
  planning unit is an energy budget, not a training load. Stay below the
  threshold that triggers a crash. Some clients can strength train in very short
  bouts with long rests; others cannot leave bed.
- **Avoid.** Fixed incremental increases. NICE NG206 is unambiguous: any
  programme "based on fixed incremental increases in physical activity or
  exercise, for example, graded exercise therapy (GET), should not be offered as
  a treatment for ME/CFS". Also avoid "push through it" language, and avoid
  treating a good day as evidence of new capacity.
- **Monitor.** Symptoms at 24, 48, and 72 hours after activity, not during it.
  Heart rate and step count as a ceiling rather than a target.
- **Stop signs.** Any post-exertional crash means the previous dose was too big.
  Reduce, do not hold.
- **Refer when.** Undiagnosed persistent fatigue. Chest pain, syncope, or
  breathlessness at low workload (myocarditis and dysautonomia both occur post
  COVID). Any client whose function is declining.
- **Evidence and the argument.** Both sides, since the brief asks:
  - Against graded exercise: NICE reviewed the evidence in 2021 and withdrew GET
    (https://www.nice.org.uk/guidance/ng206/chapter/recommendations). Patient-survey
    and re-analysis work argues the PACE trial's GET manual was fixed-incremental
    and that reported benefits do not survive reanalysis
    (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12028393/).
  - For structured rehabilitation: symptom-titrated rehabilitation and pacing
    programmes show fatigue improvements in long COVID cohorts
    (https://publications.ersnet.org/content/erjor/10/4/00089-2024 ,
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11722468/). Note the distinction
    those authors draw: symptom-titrated and pacing-based, not fixed-increment.
  - The disagreement is narrower than it looks. Nobody credible defends fixed
    increments for a client with PEM. The argument is over whether carefully
    titrated activity helps or merely does not harm.
- **Agent rule.** If a client reports symptoms worsening 12 to 72 hours after
  activity, the agent switches off every automatic progression rule and says so
  out loud.
- **Sources.** https://www.nice.org.uk/guidance/ng206/chapter/recommendations ,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9778354/ ,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11722468/

---

### Pregnancy

- **Adjust.** ACOG Committee Opinion 804: "In the absence of obstetric or medical
  complications or contraindications, physical activity in pregnancy is safe and
  desirable, and pregnant women should be encouraged to continue or to initiate
  safe physical activities." Keep training. Reduce intensity as needed by symptom,
  not by trimester rule.
- **Avoid.** ACOG advises women to "remain well hydrated, avoid long periods of
  lying flat on their backs". Contact sports, activities with fall risk, scuba
  diving, and hot environments are conventionally excluded; the full Box 2
  contraindication list (absolute and relative) is `UNVERIFIED` here because
  ACOG's site returned 402 and the Green Journal full text is paywalled.
- **Monitor.** Symptoms rather than heart rate. Core temperature in hot rooms.
  Pelvic floor symptoms. Diastasis and load tolerance in later pregnancy.
- **Stop signs.** ACOG's warning signs to discontinue exercise: vaginal bleeding
  or amniotic fluid leakage, shortness of breath before exercise, dizziness,
  feeling faint, or headache that does not resolve with rest, chest pain, muscle
  weakness, calf pain or swelling, decreased fetal movement, and preterm labour.
- **Refer when.** Any warning sign. Any obstetric complication. Any client whose
  clinician has restricted activity.
- **Evidence.** Strong for safety and benefit in uncomplicated pregnancy.
- **Sources.** https://pubmed.ncbi.nlm.nih.gov/32217980/ ,
  https://journals.lww.com/greenjournal/fulltext/10.1097/aog.0000000000003772~physical-activity-and-exercise-during-pregnancy-and-the ,
  https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2020/04/physical-activity-and-exercise-during-pregnancy-and-the-postpartum-period

---

### Postpartum

- **Adjust.** Return is gradual and individual. The six-week check is a clearance
  event, not a starting gun; tissue healing, sleep debt, and feeding load all
  govern the ramp. Pelvic floor and abdominal wall work comes before impact.
- **Avoid.** Running and jumping before the pelvic floor tolerates it. Heavy
  intra-abdominal pressure work with uncontrolled doming. Absolute timelines
  applied to everyone.
- **Monitor.** Leakage, heaviness or bulging, bleeding that restarts or increases,
  abdominal doming, C-section scar pain.
- **Stop signs.** Bleeding increasing with activity, new pelvic pain, fever.
- **Refer when.** Any leakage, prolapse symptoms, persistent diastasis with
  functional loss, or a caesarean scar that hurts under load. That is a pelvic
  health physiotherapist's job.
- **Evidence.** Weak to moderate. Return-to-running guidance in this space is
  expert consensus, not trial evidence. `UNVERIFIED` for specific timelines.
- **Sources.** https://pubmed.ncbi.nlm.nih.gov/32217980/

---

### Older adults

- **Adjust.** WHO 2020: older adults should do "varied multicomponent physical
  activity that emphasizes functional balance and strength training at moderate
  or greater intensity, on 3 or more days a week, to enhance functional capacity
  and to prevent falls", plus muscle-strengthening at moderate or greater
  intensity for all major muscle groups "on 2 or more days a week". Strength
  training for sarcopenia needs real load and real progression, not coloured
  bands.
- **Avoid.** Under-loading. Assuming frailty from age. Balance work without a
  stable support to hand.
- **Monitor.** Falls in the last year (the best single predictor of the next
  one). Medications causing dizziness. Blood pressure on standing. Bone status.
- **Stop signs.** Dizziness, near-fall, new confusion, chest symptoms.
- **Refer when.** Recurrent falls, unexplained weight loss, cognitive decline,
  new unsteadiness.
- **Evidence.** Strong.
- **Sources.** https://www.ncbi.nlm.nih.gov/books/NBK566046/ ,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7719906/

---

### Children and adolescents

- **Adjust.** Supervised, technique-first resistance training is safe and
  effective for youth. The growth-plate myth is wrong: the NSCA position statement
  attributes reported injuries to "inappropriate training techniques, excessive
  loading, poorly designed equipment, ready access to the equipment, or lack of
  qualified adult supervision", not to resistance training itself. Qualified
  supervision is the load-bearing variable.
- **Avoid.** Maximal singles in untrained youth. Unsupervised access to loaded
  equipment. Adult programmes scaled down without changing structure. Early
  single-sport specialisation.
- **Monitor.** Technique before load. Growth spurts, which change coordination
  and raise apophyseal injury risk. Total load across school sport, clubs, and
  training.
- **Stop signs.** Pain at a growth plate site (heel, knee, elbow), any pain that
  changes gait.
- **Refer when.** Persistent joint pain in a growing athlete. Suspected apophysitis.
  Disordered eating or growth concerns.
- **Evidence.** Strong. The NSCA statement is 2009, so check for a newer version
  before publishing quotes as current.
- **Sources.** https://www.nsca.com/globalassets/about/position-statements/position_stand_youth_resistance_training---2009.pdf ,
  https://journals.lww.com/nsca-jscr/fulltext/2009/08005/youth_resistance_training__updated_position.2.aspx

---

### Cancer survivors

- **Adjust.** The 2019 international multidisciplinary roundtable convened by
  ACSM sets specific prescriptions per outcome. Broadly: aerobic training at
  least 3 times per week for 20 to 30 minutes at moderate intensity, plus 6 to 10
  resistance exercises 1 to 3 times per week. The roundtable gives dedicated
  prescriptions for anxiety, depression, fatigue, quality of life, lymphoedema,
  and physical function, so the target symptom drives the dose.
- **Avoid.** Blanket avoidance of resistance training in clients with or at risk
  of lymphoedema; that advice is outdated. Training during severe neutropenia or
  acute treatment reactions without clinical guidance. Impact work with bone
  metastases.
- **Monitor.** Treatment schedule and where they are in the cycle. Fatigue,
  neuropathy from chemotherapy, cardiotoxicity risk from anthracyclines and
  trastuzumab. Port and line sites. Bone metastasis status.
- **Stop signs.** New bone pain, unexplained breathlessness, fever during
  treatment, sudden severe fatigue, new neurological symptoms.
- **Refer when.** Any active treatment client without an oncology-informed plan.
  Bone metastases. Cardiotoxic regimens. Severe cachexia.
- **Evidence.** Strong for benefit; moderate for the outcome-specific doses.
- **Sources.** https://escholarship.org/content/qt3db8c1x8/qt3db8c1x8_noSplash_fb31e8df398d31795b65fd87d53c60e5.pdf ,
  https://acsm.org/education-resources/trending-topics-resources/cancer/ ,
  https://bcmj.org/news/new-international-exercise-guidelines-cancer-survivors

---

### Depression and anxiety

- **Adjust.** Exercise works as an adjunct, not a replacement for treatment.
  Pooled effects are medium: median effect size around -0.43 for depression and
  -0.42 for anxiety versus usual care. A 2024 BMJ network meta-analysis compared
  modalities and doses against psychotherapy and antidepressants. Lower the
  activation barrier: shorter sessions, fixed times, social context when it helps.
- **Avoid.** Selling exercise as a cure. Guilt-based motivation. Missing a
  session becoming evidence of failure.
- **Monitor.** Adherence patterns, sleep, medication changes. Whether training is
  becoming compulsive (see eating disorders card).
- **Stop signs.** Any expression of suicidal intent. Stop coaching, respond as a
  person, direct to crisis services.
- **Refer when.** Symptoms worsening, self-harm, or an untreated presentation.
- **Evidence.** Strong for a real effect, moderate for the size of it, since
  blinding is impossible and publication bias is likely.
- **Sources.** https://pubmed.ncbi.nlm.nih.gov/38355154/ ,
  https://pubmed.ncbi.nlm.nih.gov/36796860/

---

### ADHD

- **Adjust.** Design for adherence first, physiology second. Structure that works:
  same time and place, minimal decisions at session start, a plan the client does
  not have to reconstruct, novelty inside a fixed frame, immediate feedback, and
  a visible streak. Body doubling and training partners help. Short sessions that
  actually happen beat long ones that do not.
- **Avoid.** Programmes that need a lot of admin. Long linear blocks with no
  feedback. Shaming missed sessions. Assuming a missed week means low motivation.
- **Monitor.** Medication timing against session timing, since stimulants raise
  resting heart rate and blood pressure. Sleep. Whether the client is
  under-fuelling because they forgot to eat.
- **Stop signs.** Palpitations, chest pain, or heat symptoms in a client on
  stimulants.
- **Refer when.** Cardiac symptoms on stimulant medication, or heat illness.
- **Evidence.** Weak for ADHD-specific exercise effects. Exercise trials in ADHD
  are inconsistent: "findings regarding the efficacy of exercise interventions on
  emotional problems like anxiety and depression in ADHD remain inconsistent".
  The adherence design points above are practitioner consensus, not trial
  evidence, and are tagged `UNVERIFIED`.
- **Medication caution.** Stimulants raise resting heart rate by roughly 5 bpm
  and blood pressure by 2 to 5 mmHg, and they interfere with thermoregulation,
  which raises heat-illness risk during exertion.
- **Sources.** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11747210/ ,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3488604/ ,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11695350/ ,
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5753970/

---

### Autism and sensory considerations

- **Adjust.** Change the environment before changing the programme. Documented
  barriers include sensory sensitivities (noise, lighting, crowds), motor
  coordination difficulty, social communication demands in group settings, and
  disruption to routine. Named facilitators: "sensory accommodations, inclusive
  policies, improved accessibility, personalized coaching, and enhanced autism
  education for staff." Predictability is a feature: same equipment, same order,
  advance notice of change.
- **Avoid.** Surprise changes. Loud busy gyms at peak time as a default. Assuming
  reluctance is a motivation problem when it is a sensory one. Forcing eye contact
  or group formats.
- **Monitor.** What is actually intolerable, in the client's own words. Note that
  post-workout showering and sweating are themselves reported barriers.
- **Stop signs.** Sensory overload or shutdown. Stop, reduce input, do not push.
- **Refer when.** Co-occurring conditions need it. Autism itself is not a medical
  clearance issue.
- **Evidence.** Weak. Mostly qualitative and survey work, small samples, few
  intervention trials.
- **Sources.** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8992823/ ,
  https://acsm.org/hot-topic-autism-and-exercise-participation/ ,
  https://journals.sagepub.com/doi/10.1177/27546330241240648

---

### Chronic kidney disease

- **Adjust.** KDIGO 2024 advises people with CKD to "undertake moderate-intensity
  physical activity for a cumulative duration of at least 150 minutes per week, or
  to a level compatible with their cardiovascular and physical tolerance", plus
  muscle-strengthening on 2 or more days per week. Dialysis clients can meet this
  intradialytically, interdialytically, or both.
- **Avoid.** Loading the arm with an arteriovenous fistula. Training in the hours
  right after dialysis if the client feels washed out. Dehydration and
  overheating.
- **Monitor.** Fatigue pattern around dialysis days. Blood pressure. Fistula site.
  Fluid restriction, which changes hydration advice, so the renal team sets it,
  not the trainer.
- **Stop signs.** Cramping with dizziness, chest pain, severe breathlessness,
  marked hypotension.
- **Refer when.** Any client on dialysis without a renal team-endorsed plan.
  Advanced CKD with cardiac symptoms.
- **Evidence.** Moderate to strong for benefit, moderate for the exact dose.
- **Sources.** https://www.ajkd.org/article/S0272-6386%2824%2900977-6/fulltext ,
  https://www.guidelinecentral.com/guideline/25092/ ,
  https://link.springer.com/article/10.1186/s12882-021-02618-1

---

### Epilepsy

- **Adjust.** Physical activity is generally safe for most people with epilepsy.
  The ILAE 2016 task force sorts sports into three risk groups by what would
  happen if a seizure occurred: "group 1, sports with no significant additional
  risk; group 2, sports with moderate risk to PWEs, but no risk to bystanders;
  and group 3, sports with major risk."
- **Avoid.** Group 3 activities without specialist advice. Swimming falls in group
  2 and needs supervision. Unsupervised free weights overhead, climbing, and
  anything where a seizure means a fall from height or into water.
- **Monitor.** Seizure frequency and control. Known triggers, which for some
  clients include sleep loss, flashing lights, and hyperventilation. Medication
  changes.
- **Stop signs.** Aura. Any seizure. Do not restart that session.
- **Refer when.** New or worsening seizures. Any client wanting group 3 activity.
  Clearance for competitive sport is a neurologist's call.
- **Evidence.** Moderate. Consensus-based, not trial-based.
- **Sources.** https://onlinelibrary.wiley.com/doi/10.1111/epi.13261 ,
  https://www.epilepsyallianceamerica.org/wp-content/uploads/2022/09/Epilepsy-Seizured-and-Phy-Exercise-Special-Report-2016-1.pdf

---

### Peripheral neuropathy

- **Adjust.** The old blanket ban on weight-bearing exercise has softened. ADA and
  ACSM historically "discouraged weight-bearing exercise for people with diabetes
  and peripheral neuropathy due to the risk of exercise-induced foot injury"; the
  current ADA position is that moderate weight-bearing exercise such as walking is
  acceptable once foot ulcers have healed, with appropriate footwear and daily
  foot checks. Add balance training, because sensory loss degrades balance.
- **Avoid.** Barefoot training. Poorly fitted shoes. High-repetition impact on
  insensate feet. Training with an open foot wound.
- **Monitor.** Daily foot inspection, including between toes. Footwear condition.
  Balance and gait. Blisters, hot spots, colour change.
- **Stop signs.** Any new foot wound, blister, or redness. Stop weight-bearing
  work and refer.
- **Refer when.** Any foot ulcer, any wound not healing, new numbness or burning,
  or a Charcot-looking hot swollen foot (emergency).
- **Evidence.** Moderate and shifting. The blanket contraindication looks like it
  was over-cautious, but the evidence base is small.
- **Sources.** https://diabetes.org/health-wellness/fitness/exercising-diabetes-complications ,
  https://link.springer.com/article/10.1186/s40798-025-00863-4 ,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8777697/

---

### Wheelchair users and spinal cord injury

- **Adjust.** The 2018 international guidelines for adults with SCI set a
  cardiometabolic-health floor of at least 20 minutes of moderate to vigorous
  aerobic exercise 2 times per week, plus 3 sets of strength exercises for each
  major functioning muscle group at moderate to vigorous intensity, 2 times per
  week. Note how low that entry dose is: it is deliberately achievable.
- **Avoid.** Overloading the shoulder, which is also the client's mobility joint.
  Pushing-dominant programmes with no pulling. Ignoring pressure care during long
  sessions.
- **Monitor.** Shoulder pain. Skin and pressure areas. Thermoregulation, which is
  impaired above roughly T6 and makes heat a real risk. Autonomic dysreflexia
  triggers in high lesions (full bladder, tight strap, skin irritation).
- **Stop signs.** Autonomic dysreflexia signs: pounding headache, sudden blood
  pressure rise, flushing above the lesion, sweating, blotchy skin. This is a
  medical emergency. Sit the client up, remove the trigger, call for help.
- **Refer when.** New shoulder pain limiting transfers. Any pressure sore. Any
  dysreflexia episode.
- **Evidence.** Moderate. Guideline is systematic-review based with consensus.
- **Sources.** https://www.nature.com/articles/s41393-017-0017-3 ,
  https://community.scireproject.com/topic/exercise-guidelines/ ,
  https://www.apta.org/patient-care/evidence-based-practice-resources/cpgs/evidence-based-scientific-exercise-guidelines-for-adults-with-spinal-cord-injury-an-update-and-a-new-guideline

---

### Amputees

- **Adjust.** Expect a higher metabolic cost of movement. People with below-knee
  amputation "choose a lower self-selected walking speed than able-bodied persons,
  and expend at least 20% more energy to walk at the same speed", and the cost
  rises with more proximal amputation levels. Programme intact-side and trunk
  strength, plus balance. Pre- and post-prosthetic phases differ: pre-prosthetic
  work covers residual limb shaping, skin care, range of motion, strength, and
  cardiovascular training.
- **Avoid.** Training through socket pain. Ignoring asymmetric loading of the
  intact limb over years.
- **Monitor.** Residual limb skin every session and at bedtime, checked
  thoroughly, washed, dried, and inspected for breakdown. Socket fit, which
  changes with limb volume across the day. Intact-limb overuse.
- **Stop signs.** Skin breakdown, blistering, new pain in the residual limb, or a
  socket that has stopped fitting.
- **Refer when.** Any skin breakdown, socket fit problems (prosthetist), phantom
  or residual limb pain change, or intact-limb overuse injury.
- **Evidence.** Weak to moderate. Clinical standards-of-care documents rather
  than trials.
- **Sources.** https://www.brighamandwomens.org/assets/BWH/patients-and-families/rehabilitation-services/pdfs/general-le-amputation-bwh.pdf ,
  https://link.springer.com/content/pdf/10.2165/00007256-199520040-00001.pdf ,
  https://www.merckmanuals.com/home/special-subjects/rehabilitation/rehabilitation-after-limb-amputation

---

### Eating disorders and compulsive exercise

- **Adjust.** Exercise is not automatically removed, but it is staged. The Safe
  Exercise at Every Stage (SEES) guideline sets exercise readiness by physical and
  mental health symptoms and recovery status. Depending on medical and mental
  state, the first stage may be to pause all exercise to stabilise medically and
  behaviourally, then short casual supervised walks, then graded increases once
  medically well. The argument for including exercise rather than banning it is
  that recovery outcomes are better when exercise is addressed rather than removed.
- **Avoid.** Calorie talk, body composition measurement, weigh-ins, before-and-after
  photos, "earning" food framing, and any progression driven by the client's
  anxiety about missing a session.
- **Monitor.** Red flags: training through injury and illness, distress when a
  session is missed, secret or extra sessions, rigid rules, exercising to
  compensate for eating, bradycardia, dizziness, fainting, amenorrhoea, stress
  fractures, cold intolerance.
- **Stop signs.** Fainting, chest pain, bradycardia, or any sign of medical
  instability. Stop and escalate the same day.
- **Refer when.** Suspicion is enough. The trainer does not screen, diagnose, or
  manage. Refer to the GP and an eating disorder service, and say plainly why.
  Medical instability is an emergency.
- **Evidence.** Weak to moderate. SEES is expert consensus. The specific medical
  stability criteria are `UNVERIFIED` here; get the SEES guideline document
  itself before encoding thresholds.
- **Sources.** https://jeatdisord.biomedcentral.com/articles/10.1186/s40337-022-00685-9 ,
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6260729/ ,
  https://equip.health/articles/food-and-fitness/exercise-during-eating-disorder-treatment

---

### Orthopaedic rehab: where the trainer stops and the physio starts

The line: acute injury, post-surgical rehab, and diagnosis belong to the
clinician. Progressive loading of a client already discharged, or working
alongside a written physio plan, belongs to the trainer. When in doubt, the
trainer's job is to keep training everything that is not injured.

**Post-ACL reconstruction.** Return-to-sport criteria in common use are limb
symmetry index of 90% or greater for isokinetic quadriceps strength and for
single-leg hop tests, plus time. Most people do not meet them when they think
they do: at six months only 35% reached 90% symmetry for isokinetic quadriceps
strength and 67% for single-leg hop, with just 19.6% passing all three tests; at
nine months, 46.8% still failed the strength criterion at 60°/s and only 11.3%
passed everything. Patients scoring 90% or above are less likely to reinjure.
The trainer's role: build general strength and conditioning under the surgeon's
and physio's timeline, never clear a return to sport.
(https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6267144/ ,
https://pmc.ncbi.nlm.nih.gov/articles/PMC11887908/)

**Rotator cuff.** `UNVERIFIED` for specific protocol numbers. Post-repair,
loading follows the surgeon's protocol and the trainer follows the physio.
Non-surgical cuff-related shoulder pain responds to progressive loading, which a
trainer can run in coordination with a physio.

**Tendinopathy.** Progressive mechanical loading is the treatment. Isometrics
can reduce pain. Heavy slow resistance, with repetitions taken slowly (over 6
seconds each for both eccentric and concentric phases), matched the Alfredson
eccentric protocol for pain and function with higher patient satisfaction in
Achilles and patellar tendinopathy. Use a pain-monitoring model with a 0 to 10
scale: the 24-hour response is the decision variable, and if pain and morning
stiffness are the same or better 24 hours later, the tendon tolerated the load.
Do not rest a tendon into recovery.
(https://www.physio-network.com/blog/tendinopathy/ ,
https://www.apunts.org/en-load-management-in-tendinopathy-clinical-articulo-S1886658117300580 ,
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7406028/)

**Refer when.** Trauma with immediate swelling, inability to bear weight,
suspected fracture, locking or giving way, neurological symptoms, night pain,
or pain that is worsening across weeks despite sensible loading.

---

### Menstrual cycle

- **Adjust.** Individually, or not at all. The McNulty 2020 meta-analysis rated
  the evidence quality as low (42%) and found performance "might be trivially
  reduced during the early follicular phase" compared with other phases. Its own
  conclusion: "general guidelines on exercise performance across the MC cannot be
  formed; rather, it is recommended that a personalised approach should be taken
  based on each individual's response". A later review found no influence of
  cycle phase on acute strength performance or resistance training adaptation.
- **Avoid.** Selling cycle-phase periodisation as evidence-based. It is not.
- **Monitor.** The client's own logged symptoms and performance, if she wants to
  track them. That is the only defensible basis for adjusting.
- **Stop signs.** None specific.
- **Refer when.** Absent or lost periods in a training client. That is a red flag
  for low energy availability and bone health, not a sign of fitness.
- **Evidence.** Weak, and openly so.
- **Sources.** https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7497427/ ,
  https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2023.1054542/full ,
  https://journals.physiology.org/doi/full/10.1152/japplphysiol.00223.2025

---

### Menopause

- **Adjust.** Prioritise resistance training. Falling oestrogen drives muscle and
  bone loss, and strength work is the direct countermeasure. Combine with impact
  or loading work for bone (see osteoporosis card) and aerobic work for
  cardiovascular risk, which rises after menopause.
- **Avoid.** Treating menopause as a reason to reduce intensity. The opposite
  applies.
- **Monitor.** Sleep, thermoregulation and hot flushes (which change tolerance of
  hot rooms), joint aches, bone status, blood pressure.
- **Stop signs.** None specific beyond the global list.
- **Refer when.** Symptoms materially affecting function, or bone health concerns.
  HRT decisions belong to the client's clinician.
- **Evidence.** Moderate for resistance training benefits, weak for
  menopause-specific programming rules.
- **Sources.** https://www.womens-health-concern.org/wp-content/uploads/2023/06/29-WHC-FACTSHEET-Exercise-in-menopause-JUNE2023-A.pdf ,
  https://news.exeter.ac.uk/faculty-of-health-and-life-sciences/first-of-its-kind-study-shows-resistance-training-can-improve-physical-function-during-menopause/

---

### Medications that change the exercise response

The agent never advises on doses. It adjusts the programme around the drug.

**Beta blockers.** They "blunt the heart rate response to exercise, making target
HR zones unreliable", and reduce contractility and blood flow. RPE is unaffected
by beta blockade, so use RPE for intensity. ACSM recommends RPE 13 and 15 on the
Borg 6 to 20 scale for moderate and vigorous, and RPE 12 to 16 for most adults in
health-promoting aerobic exercise. For cardiac rehab clients recently post-MI on
beta blockers, RPE 13 (or 4 on the CR10 scale) is the recommended training
intensity. Also expect slower heart rate recovery readings to be meaningless.
(https://www.sciencedirect.com/science/article/pii/S1726490115001410 ,
https://pubmed.ncbi.nlm.nih.gov/8776008/ ,
https://pubmed.ncbi.nlm.nih.gov/24778550/)

**Statins.** Muscle symptoms range from "mild weakness, cramps, and muscle pains"
through myositis (CK 10 to 40 times upper limit) to rhabdomyolysis (usually above
40 times ULN, with renal injury). Statins augment CK rises after eccentric or
vigorous exercise, and severe toxicity can occur "especially when systemic statin
exposure is increased by intense unaccustomed exercise". Practical rule:
introduce eccentric and novel high-volume work gradually in statin users, and
treat new persistent muscle pain plus dark urine as an emergency.
(https://doi.org/10.3390/medicina62061134 ,
https://www.sciencedirect.com/science/article/pii/S1109966619302842 ,
https://academic.oup.com/ndt/article/20/1/244/1818578)

**SSRIs.** `UNVERIFIED`. Commonly cited effects include sleep disruption, weight
change, and reduced heat tolerance. I did not verify these against a primary
source. Do not publish specifics without checking.

**GLP-1 agonists (semaglutide, tirzepatide).** Lean soft tissue loss accounted
for 26% to 40% of total weight loss in recent trials. In a prospective series of
200 adults given resistance training and protein education at initiation, weight
was down about 13% at 6 months with only about 3% muscle mass loss. Programme
implication: resistance training becomes non-negotiable, and protein intake
matters, though the trainer refers the protein target to a dietitian. Also expect
reduced appetite and reduced food intake, so fuelling around sessions is a real
problem, and nausea and dehydration are common early.
(https://pmc.ncbi.nlm.nih.gov/articles/PMC12536186/ ,
https://dom-pubs.onlinelibrary.wiley.com/doi/10.1111/dom.15728 ,
https://www.acefitness.org/continuing-education/certified/june-2025/8892/glp-1s-and-lean-mass-what-the-research-shows/)

**Stimulants (ADHD medication).** Increases of roughly 5 bpm resting heart rate
and 2 to 5 mmHg blood pressure, with raised resting, submaximal, and peak heart
rates on acute use. They interfere with thermoregulation by altering
neurotransmitter activity, raising heat illness risk during exertion. Practical
rules: heart-rate zones drift, use RPE as a cross-check; be conservative in heat;
escalate palpitations or chest pain.
(https://pmc.ncbi.nlm.nih.gov/articles/PMC3488604/ ,
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11695350/ ,
https://www.jacc.org/doi/10.1016/j.jacc.2020.05.081)

---

## 4. Handling medical data

### Legal position

HIPAA mostly does not apply. "Personal trainers and non-medical fitness
professionals are generally not considered covered entities under HIPAA", and
most gyms are not either. It can apply when the trainer works with or for a
covered entity, or handles protected health information on its behalf as a
business associate. Where a client tells you something directly and no covered
entity is involved, HIPAA typically does not apply. That is not permission to be
careless: "you still shoulder confidentiality expectations, and state privacy
rules or consumer health data laws may govern how you collect, store, and use
sensitive information." Washington's My Health My Data Act and similar state laws
are the ones to watch, and GDPR treats health data as a special category.
(https://www.paubox.com/blog/does-hipaa-apply-to-personal-trainers ,
https://www.accountablehq.com/post/does-hipaa-protect-your-gym-health-data-what-s-covered-and-what-isn-t ,
https://www.ideafit.com/the-hipaa-effect/)

`UNVERIFIED`: those are secondary compliance-vendor sources. Get a lawyer's read
before relying on them in a shipped product.

### What to store

Store the minimum that changes a programming decision. For each condition:

| Field | Example | Why it earns its place |
|---|---|---|
| `condition` | `type_1_diabetes` | Selects the card |
| `status` | `stable` / `flaring` / `acute` | Changes what is allowed today |
| `clearance` | `yes, 2026-03-14, Dr Okafor, moderate only` | Gates intensity |
| `restrictions` | `no loaded spinal flexion` | Hard constraint on exercise selection |
| `monitoring` | `glucose pre/post` | Drives session prompts |
| `stop_signs` | free text from the card | Read at session start |
| `emergency` | `fast carbs in bag; contact: Sam` | Needed in the worst 60 seconds |
| `consent` | `stored 2026-03-14, purpose: programming` | Audit trail |

Do not store: diagnoses the client did not volunteer, test results, medication
doses, mental health history beyond what affects programming, or anything
scraped from a clearance letter beyond the restrictions and the ceiling.

### How to flag it

- Conditions live on the athlete profile, not buried in session notes.
- Every condition flag carries a review date. Stale flags are worse than none.
- The agent surfaces active restrictions at exercise-selection time, not as a
  wall of text at session start.
- A red-flag event gets logged with a timestamp and what the agent said. That log
  is the thing anyone will want after an incident.
- Deletion on request must actually delete, including the session-note copies.

### Consent wording that works

"I'm going to store [condition] and [restriction] so I don't program something
that hurts you. I won't store anything else medical, and you can tell me to
delete it at any time. Is that OK?" Wait for yes. Log the yes.

---

## 5. Open questions for the user

1. **Jurisdiction.** Which country's rules govern this? HIPAA, GDPR, and state
   consumer-health-data laws point different directions on storing condition
   flags. The data-handling section above assumes US and is thin without this.
2. **Who is the user.** Is this agent for you alone, or for trainers with
   clients? Self-use lowers the liability question and raises the "will it
   nag me" question. Multi-client use needs the audit log to be real.
3. **Refusal strength.** When a client says "I know, train me anyway", does the
   agent hard-refuse, or proceed with a logged disclaimer? I have written the
   cards assuming hard refusal on red flags and disclaimers elsewhere. Confirm.
4. **Condition breadth at launch.** 25 cards is a lot to maintain. Which
   conditions actually apply to you or your first users? I would ship the global
   red flags plus 5 cards rather than all 25 half-checked.
5. **Clearance storage.** Do you want the agent to hold clearance letters, or
   only a structured summary the user types in? Holding documents changes the
   data-protection picture materially.
6. **PEM handling.** The long COVID / ME-CFS card disables automatic progression.
   Does slice 03's progression engine have an off switch, or does this need one
   building?

---

## 6. Gaps in this slice

Named honestly so nobody trusts them by omission.

- ACSM Guidelines 11th edition and ACSM's Exercise Management for Persons with
  Chronic Diseases and Disabilities are both paywalled books. I worked from
  position statements and open-access guidelines instead. The screening algorithm
  boxes and the special-populations FITT tables should be checked against the book.
- ACOG 804's Box 2 contraindication list is not quoted; both ACOG and the Green
  Journal returned paywalls. The warning-sign list is from secondary reporting of
  Box 3.
- ADA 2016 glucose thresholds beyond the carbohydrate quotes are unverified.
- SEES eating-disorder medical stability criteria unverified.
- No IDEA scope-of-practice statement found.
- EULAR inflammatory arthritis physical activity recommendations not retrieved.
- 2015 Heart Rhythm Society POTS consensus not retrieved; POTS card leans on
  secondary sources.
- Rotator cuff rehab has no numbers here.
- Transgender athletes deliberately excluded, per slice 11.
