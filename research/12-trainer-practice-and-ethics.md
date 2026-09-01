# How a personal trainer is supposed to act

Research slice 12. Written 2026-08-31.

Sibling slices: 06 = skill catalog, 07 = baselining, 08 = goal-specific
programming, 09 = sport-specific, 10 = medical populations, 11 = transgender
clients. This file is the **conduct and process layer** those slices sit on. It
covers ethics, scope, session process, communication, and the "meet them where
they are" craft. It deliberately contains almost no programming numbers. Slices
03, 07 and 08 own those.

Everything here is cited. Where I could not find a primary source, the claim is
tagged `UNVERIFIED` and explained.

Nothing in this file is legal advice. Where it touches liability, waivers, or
data law it says "consult a lawyer" and means it.

---

## TL;DR: ten rules of conduct for the agent

1. **Stay inside scope. Prevention and fitness only.** A trainer's focus is
   "prevention and involves enhancing components of health and fitness for the
   general, healthy population or those cleared for exercise", and trainers "do
   not diagnose or treat areas of pain or disease".
   ([NASM Code of Professional Conduct](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))
2. **Screen before you program, and re-screen on any change.** NASM forbids
   beginning training "prior to receiving and reviewing a current health-history
   questionnaire signed by the client".
   ([NASM code](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))
   Screening decides who needs medical clearance.
   ([ACSM 2015 screening update](https://pubmed.ncbi.nlm.nih.gov/26473759/))
3. **Refer, and say who to.** Refer on any change in health status or
   medication, any undiagnosed illness or injury, and any unusual pain during a
   session, in which case "immediately discontinue the session". Refer nutrition
   and supplement requests out.
   ([NASM code](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))
4. **No meal plans, no supplements, no diagnoses.** ACE: clients wanting "specific
   meal plans, recipes, or recommendations for nutritional supplements should be
   referred to a registered dietitian".
   ([ACE PT Manual ch.1, p.9](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))
   General healthy-eating information is allowed and encouraged.
   ([ACE nutrition scope position](https://www.acefitness.org/resources/pros/expert-articles/6248/nutrition-scope-of-practice-what-you-can-do-as-a-personal-trainer/))
5. **Never contradict the client's medical team.** If a physician's release sets
   intensity or exercise limits, "the trainer must follow these guidelines when
   designing the client's exercise program".
   ([ACE ch.1, p.9](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))
6. **Treat everything the client tells you as confidential.** Protect it "in
   conversations, advertisement and any other arena unless otherwise agreed upon
   by the client in writing", and store and dispose of records securely.
   ([NASM code](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))
   ACE says hold it to the HIPAA standard even though the trainer relationship is
   not legally privileged.
   ([ACE ch.1, p.14](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))
7. **Keep a professional boundary and get consent for contact.** ACE: "Avoid
   touching clients/participants unless it is essential to instruction", tell
   them why first, offer an alternative if they object, and stop if it seems to
   make them uncomfortable.
   ([ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))
8. **Support autonomy. The client decides.** ACSM requires treating people with
   "dignity, respect, and fairness, recognizing their autonomy and right to make
   informed decisions regarding their health, training, and participation".
   ([ACSM Code of Ethics](https://acsm.org/wp-content/uploads/2025/05/ACSM-Code-of-Ethics.pdf))
   Autonomy support also predicts adherence.
   ([Teixeira 2012](https://link.springer.com/article/10.1186/1479-5868-9-78))
9. **Do not oversell. Realistic timelines only.** ACE calls out "Lose 10 pounds in
   10 days" style claims as undermining public trust, and requires that trainers
   not "represent yourself in an overly commercial or misleading manner".
   ([ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))
10. **Disclose that you are an AI, and say what you cannot do.** The EU AI Act
    Article 50 requires AI systems that interact with people to inform them at
    first contact, in a way they notice.
    ([EU AI Act Art. 50 guidance](https://artificialintelligenceact.eu/transparency-rules-article-50/),
    [EC FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act))
    Current research says AI exercise prescriptions still need "expert validation
    before clinical deployment".
    ([Consistency of AI-generated exercise prescriptions](https://arxiv.org/abs/2604.11287))

---

## 1. Scope of practice

### 1.1 What a scope of practice is

ACE defines it as "the legal range of services that professionals in a given
field can provide, the settings in which those services can be provided, and the
guidelines or parameters that must be followed."
([ACE ch.1, p.8](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

Two things follow. First, the boundary is partly **legal and varies by state,
province and country**, because "most laws defining a profession are determined
and regulated by state regulatory agencies, including licensure."
([ACE ch.1, p.8](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))
Second, the certifying body layers its own code on top of the law.

For an AI agent this means the scope table below is a floor, not a ceiling. The
agent cannot know the user's jurisdiction unless asked. See open questions.

### 1.2 The do / don't / refer table

This is the IDEA Personal Fitness Trainers' Scope of Practice as reprinted in
the ACE Personal Trainer Manual, Table 1-2, with the referral target named.
([ACE ch.1, p.9](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf);
originally IDEA Health & Fitness Association opinion statement, 2001)

| Trainers do NOT | Trainers DO | Refer to |
|---|---|---|
| Diagnose | Receive exercise, health or nutrition guidelines from a physician, PT or RD. Follow national consensus guidelines. Screen for exercise limitations. Identify potential risk factors through screening. | Physician, physiotherapist |
| Prescribe (exercise, in the clinical sense) | Design exercise programs | Physician / clinical exercise physiologist for an exercise *prescription* |
| Prescribe diets or recommend specific supplements | Provide general information on healthy eating per MyPlate | Registered dietitian |
| Treat injury or disease | Refer for treatment. Use exercise to improve overall health. Help clients follow physician or therapist advice. | Physician, physiotherapist |
| Monitor progress for medically referred clients | Document progress. Report progress to the referring professional. Follow their recommendations. | The referring clinician |
| Rehabilitate | Design an exercise program once the client has been released from rehabilitation | Physiotherapist |
| Counsel | Coach. Provide general information. | Qualified counsellor or therapist |
| Work with patients | Work with clients | n/a |

Extra referral targets ACE names explicitly:

- Suspected eating disorder: "a client/participant who is suspected of an eating
  disorder should be referred to an eating disorders specialist."
- Family or marital problems, or addictive behaviour including substance abuse:
  refer to a clinical psychologist.
- A client who wants to lose more weight than is advisable and will not accept a
  safer goal: refer to "a registered dietitian who has experience with body image
  and related issues."
  (all three: [ACE ch.1 appendix A and p.15](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

### 1.3 The positive scope

ACE's own statement of what its CPTs *are* allowed to do is worth keeping intact,
because it is the best short description of the job. The ACE Certified Personal
Trainer scope includes developing safe programs for people who are apparently
healthy or medically cleared, conducting health-history interviews and stratifying
risk "to determine the need for referral", administering assessments using
"research-proven and published protocols", helping clients set realistic goals,
teaching exercise "through demonstration, explanation, and proper cueing and
spotting techniques", empowering adherence "using guidance, support, motivation,
lapse-prevention strategies, and effective feedback", educating on health topics,
protecting confidentiality under HIPAA, referring out when appropriate, and being
ready for emergencies.
([ACE ch.1, Figure 1-2, p.10](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

NSCA frames the same job as using "an individualized approach to assess,
motivate, educate, and train clients regarding their health and fitness needs",
plus responding appropriately in emergencies.
([NSCA-CPT page](https://www.nsca.com/certification/nsca-cpt/essentials-of-personal-training--3rd-edition/))

CIMSPA in the UK draws the line slightly differently and includes "nutritional
advice and overall lifestyle management" in the PT role.
([CIMSPA Professional Standard: Personal Trainer v1.1](https://cimspa.co.uk/?jet_download=5b612d0f802c7e03f150a5eed82b744cf9ba0996))
This is a real divergence from the US bodies, not a wording quirk. UK trainers
have more nutrition latitude than US trainers do. If the agent has UK users, do
not assume the ACE line is the law there.

### 1.4 Supplements

ACE is blunt. Supplements are not FDA-regulated, so "their strength, purity,
safety, and effects are not guaranteed", and some interact badly with prescribed
medication. Trainers who know a lot about supplements "are no more qualified to
recommend these supplements to clients than they are to recommend or prescribe
medications."
([ACE ch.1, p.16](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

Agent rule: answer factual questions about what a supplement is. Never recommend
one, never dose one, never sequence one with medication. Refer.

---

## 2. Consent, records, boundaries, liability

### 2.1 Informed consent and waivers

Informed consent should cover "the content and process of the program delivery
system, risk and benefits, confidentiality, responsibilities of client, and
documentation of the accepted information."
([NSCA CPT ch.25 summary](https://www.ptpioneer.com/personal-training/certifications/nsca-cpt/nsca-cpt-chapter-25/) —
secondary source summarising the NSCA text; `UNVERIFIED` against the NSCA
textbook itself, which is paywalled)

A waiver is a contractual promise not to sue if injured. It does **not** cancel
the duty to perform competently. An assumption-of-risk agreement "does not
relieve the personal trainer of the duty to perform in a competent and
professional manner."
([NSCA CPT ch.25 summary](https://www.ptpioneer.com/personal-training/certifications/nsca-cpt/nsca-cpt-chapter-25/))
NSCA publishes a template.
([NSCA waiver form](https://www.nsca.com/contentassets/4b984f503013432bb81de11a14627582/nsca-waiver-pdf.pdf))

Consent is not a one-time form. It has to be re-taken when the program materially
changes, and it has to be understood, not just signed. `UNVERIFIED` as a
citation, but it follows directly from ACSM's requirement to recognise the
client's "right to make informed decisions".
([ACSM code](https://acsm.org/wp-content/uploads/2025/05/ACSM-Code-of-Ethics.pdf))

Liability insurance: ACE recommends all certified professionals carry
professional liability insurance.
([ACE ch.1, p.16](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))
NASM makes it mandatory: certified professionals "must maintain adequate
liability insurance."
([NASM code, Business Practice](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))
Anything past that is a question for a lawyer in the relevant jurisdiction.

### 2.2 Records and documentation

NASM requires "adequate and truthful progress notes for each client", accurate
records, and secure storage and disposal.
([NASM code](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))
ACE adds that trainers should "maintain confidential records that include the
client's health history" even when there is no physician referral.
([ACE ch.1](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

A trainer-adapted SOAP note is the standard shape. It is borrowed from clinical
practice rather than mandated by any of the certifying bodies, so treat the
format as craft convention, not a rule. `UNVERIFIED` as a fitness-industry
standard.

| SOAP field | Clinical meaning | Trainer adaptation |
|---|---|---|
| S — Subjective | What the patient reports | What the client said: sleep, stress, soreness, mood, "my knee felt weird on set 3" |
| O — Objective | What the clinician measured | Sets, reps, load, RPE, rest, HR, session RPE, what you observed in their movement |
| A — Assessment | Clinical judgement | Your read: fatigue accumulating, technique breaking down at load X, adherence slipping |
| P — Plan | Next step | What changes next session, what stays, what you will watch |

Agent rule: write S, O, A, P for every session. The O row is the workout log and
should already exist. The A row is the one agents skip and it is the one that
makes the next session good.

### 2.3 Boundaries and dual relationships

ACE puts responsibility for the boundary on the professional, not the client:
"Fitness professionals are responsible for setting and monitoring the boundaries
between a working relationship and friendship with their clients/participants."
The rules are: never initiate or encourage discussion of a sexual nature; avoid
touching unless essential to instruction; inform before touching and offer an
alternative if the client objects; stop touching if it appears to cause
discomfort; take reasonable steps so personal and social contact does not damage
the trainer-client relationship. If the boundary cannot be held, "the prudent
course of action is to terminate the relationship" and refer on.
([ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

IDEA says the same thing and names the referral targets: another trainer, a
medical doctor, or a mental health specialist.
([IDEA Code of Ethics for Personal Trainers](https://www.ideafit.com/personal-training/idea-code-of-ethics-for-personal-trainers/))

ACSM requires professionals to "maintain appropriate professional boundaries and
manage any real or perceived conflicts of interest to ensure objectivity and
prevent exploitation."
([ACSM code](https://acsm.org/wp-content/uploads/2025/05/ACSM-Code-of-Ethics.pdf))

Conflict of interest specifically: IDEA says recommend products or services only
if they benefit the client, "not because they will benefit you financially or
occupationally", and disclose when a recommendation earns you money.
([IDEA code](https://www.ideafit.com/personal-training/idea-code-of-ethics-for-personal-trainers/))

**Touch and spotting consent, as an agent protocol.** An AI trainer cannot touch
anyone, so this rule transfers to two places. First, when the agent tells a human
spotter or training partner what to do, it passes the consent rule on: say what
you are going to touch and why, before you touch it. Second, the same
ask-before-you-act pattern applies to the agent's own intrusions: photos, video
form checks, weigh-ins, body measurements, progress pictures. Ask, explain why,
accept no, offer an alternative. `UNVERIFIED` as a published rule for AI
trainers. It is a direct transfer of the ACE touching rule.

---

## 3. The client process

### 3.1 The two industry models

Both major US models say the same structural thing: start where the person is,
build a base before you build performance, and let assessment timing follow the
client rather than lead them.

**ACE Integrated Fitness Training (IFT).** Two tracks, four phases each.
Functional movement and resistance: (1) Stability and Mobility, (2) Movement,
(3) Load, (4) Performance. Cardiorespiratory: (1) Aerobic Base, (2) Aerobic
Efficiency, (3) Anaerobic Endurance, (4) Anaerobic Power. ACE's own framing is
that "clients are met exactly where they are and guided toward their goals
through a combination of well-timed assessments".
([ACE IFT model](https://www.acefitness.org/fitness-certifications/personal-trainer-certification/ace-ift-model.aspx),
[IFT cardio phases](https://www.acefitness.org/certifiednewsarticle/709/ace-ift-model-for-cardiorespiratory-training-phases-1-4/),
[IFT movement phases 3-4](https://www.acefitness.org/certifiednewsarticle/684/ace-integrated-fitness-training-ift-model-for-functional-movement-and-resistance-training-phases-3-and-4/))

Phase 1 cardio is aimed at people "that are sedentary or have little
cardiorespiratory fitness", working in zone 1 at RPE 3-4 on a 0-10 scale, to
build the habit before building fitness.
([ACE IFT cardio phases](https://www.acefitness.org/certifiednewsarticle/709/ace-ift-model-for-cardiorespiratory-training-phases-1-4/))
That is the single most useful number in this file for a deconditioned beginner.

**NASM OPT.** Three levels, five phases: (1) Stabilization Endurance, (2) Strength
Endurance, (3) Muscular Development / Hypertrophy, (4) Maximal Strength, (5)
Power.
([NASM OPT model](https://www.nasm.org/certified-personal-trainer/the-opt-model))

The agent does not need to pick one. What matters is the shared rule: **stability
and movement quality before load, load before performance.** Slice 08 owns the
numbers inside each phase.

### 3.2 The end-to-end flow

The ACE exam content outline names the competencies in order: "developing and
enhancing rapport with clients, collecting adequate health-history information
and determining the appropriateness of referral, conducting appropriate
assessments, designing and modifying exercise programs to help clients progress
toward their goals, motivating clients to exercise and adhere to their programs,
and always acting in a professional manner within the personal trainer's scope of
practice."
([ACE ch.1, p.13](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

That is the flow, in order:

```
1. RAPPORT      Build it first. Nothing below works without it.
                   |
2. INTAKE       Health history + goals + life constraints + preferences.
                Signed, dated, reviewed. NASM: no training before this exists.
                   |
3. SCREEN       Any red flag -> refer, wait for clearance, do not train.
                ACSM 2015: screen on activity level, signs/symptoms/known
                disease, and desired intensity.
                   |
4. ASSESS       Only what will change the program. Well-timed, not front-loaded.
                Slice 07 owns the battery.
                   |
5. PROGRAM      Match the phase to the person, not the person to the phase.
                   |
6. COACH        Deliver sessions. Cue, feed back, adjust in the moment, log.
                   |
7. REASSESS     Fixed cadence + event triggers. Loop back to 4 or 5.
```

Steps 3 and 7 are the ones that most often get skipped, and they are the two that
protect the client.

### 3.3 Screening: the current standard

ACSM replaced risk-factor stratification in 2015. The new model screens on three
things: current physical activity level, presence of signs or symptoms and/or
known cardiovascular, metabolic or renal disease, and desired exercise intensity.
People are referred for medical clearance based on signs, symptoms and known
disease, not on a count of risk factors.
([Updating ACSM's Recommendations for Exercise Preparticipation Health Screening](https://pubmed.ncbi.nlm.nih.gov/26473759/),
[ACSM screening guidelines PDF](https://www.exerciseismedicine.org/assets/page_documents/ACSM%20Preparticipation%20Screening%20Guidelines.pdf))

The change was deliberate. The old algorithm produced "excessive physician
referrals, possibly creating a barrier to exercise participation", and the new one
cut referrals by about 41%.
([ACE: New Preparticipation Screening Guidelines](https://www.acefitness.org/resources/pros/expert-articles/6921/new-preparticipation-screening-guidelines-what-health-and-fitness-pros-need-to-know/))

Read that as a two-sided rule. Do not train someone who needs clearance. Also do
not send someone for clearance they do not need, because that is itself a harm.

### 3.4 Session structure

The warm-up / main / cool-down shape is universal enough that no single body
claims it. The RAMP framework (Raise, Activate, Mobilise, Potentiate) is the
common warm-up structure and slice 06 already assigned it to a `warmup` skill.
`UNVERIFIED` here as a cited standard within the certification texts I read.

The part worth adding is the **debrief**, which most session templates leave out
and which is where the coaching actually lands:

| Block | Purpose | Agent behaviour |
|---|---|---|
| Check-in (1-2 min) | Sleep, stress, soreness, time available today | One question, not a form. Adjust the session before starting, not after it fails. |
| Warm-up | Raise temp, prep the patterns in today's session | Specific to today's lifts, not generic |
| Main work | The stimulus | Cue, log, adjust load in real time |
| Cool-down | Come down, close the session | Optional. Do not moralise about it. |
| Debrief (2 min) | Consolidate | What went well (name one specific thing), what changes next time, what to watch. Then log the SOAP A and P. |

The debrief is where affirmation, self-efficacy building, and the plan for next
session all happen. It costs two minutes and it is the highest-leverage part of
the session for adherence. `UNVERIFIED` as a measured claim. The components are
evidenced individually (affirmation and mastery-experience framing, below), the
"put them in a two-minute debrief" packaging is craft.

---

## 4. Communication playbook

### 4.1 Motivational interviewing

MI is "an empathic, person-centered counseling approach that prepares people for
change by helping them resolve ambivalence, enhance intrinsic motivation, and
build confidence to change."
([MINT](https://motivationalinterviewing.org/understanding-motivational-interviewing))

The core skill set is OARS: Open questions, Affirmations, Reflections, Summaries.
([ISSUP OARS summary](https://www.issup.net/knowledge-share/resources/2019-10/motivational-interviewing-open-questions-affirmation-reflective),
[MICCSI OARS quick guide](https://www.miccsi.org/wp-content/uploads/2025/05/Key-Concepts-of-MIOARS-Quick-Guide.pdf))

Adapted to a chat interface:

| Skill | What it is | Chat example |
|---|---|---|
| **O**pen question | Invites the person to "tell their story" in their own words without leading them | "What made today feel harder than last week?" not "Did you sleep badly?" |
| **A**ffirmation | Statement of appreciation that names a strength or an effort, independent of whether the change happened | "You came back after a three-week gap. That's the hard part and you did it." |
| **R**eflection | Repeat, rephrase, or guess deeper at what they meant | They say "I just don't have time." You say "Training feels like one more thing you can't fit." |
| **S**ummary | Reflective listening applied at a transition point | "So: knee's fine, sleep is bad, you want to keep squatting but drop the volume. Have I got that right?" |

Chat-specific notes:

- Reflections are cheap in text and expensive in a live session. Use more of them
  than a human trainer would. Text has no tone, so a reflection is how the agent
  proves it listened.
- Do not stack an affirmation onto every message. It reads as flattery and it is
  what a sycophantic bot does. One specific affirmation beats five generic ones.
- An open question ending a message is an invitation. An open question in the
  middle of a wall of advice is decoration. Ask, then stop typing.
- Ambivalence is normal, not a problem to argue with. MI's whole premise is
  helping the person resolve it themselves, not resolving it for them.

### 4.2 Stages of change (TTM)

Six stages: precontemplation ("not ready"), contemplation ("getting ready"),
preparation ("ready"), action, maintenance, termination. Plus ten processes of
change, decisional balance, self-efficacy and temptation.
([Transtheoretical model overview](https://en.wikipedia.org/wiki/Transtheoretical_model),
[TTM StatPearls](https://www.ncbi.nlm.nih.gov/books/NBK556005/),
[Prochaska & Velicer 1997](https://pubmed.ncbi.nlm.nih.gov/10170434/))

The one operational thing to take from TTM: **the intervention has to match the
stage.** Giving a precontemplation client a program is wasted. Giving an action
client more education is wasted. In practice the agent should ask what stage
someone is in before it decides whether to write a plan or have a conversation.

TTM is contested as a theory. Several reviews have questioned whether stage-matched
interventions outperform non-staged ones. I did not verify a specific critique
this session. `UNVERIFIED` — flag for follow-up before the agent leans on TTM
hard.

### 4.3 Self-determination theory

Three basic psychological needs: autonomy, competence, relatedness. Satisfying
them fosters autonomous motivation, and that can be "self-driven or can be
fostered in social environments that are need supportive."
([Teixeira et al. 2012, IJBNPA](https://link.springer.com/article/10.1186/1479-5868-9-78),
[PubMed](https://pubmed.ncbi.nlm.nih.gov/22726453/))

The 66-study review found "a consistent pattern of positive relations between
autonomous motivation and exercise behavior", with identified regulation
predicting **adoption** and intrinsic motivation predicting **maintenance**.
([Teixeira 2012](https://link.springer.com/article/10.1186/1479-5868-9-78))

That split matters. Early on, "this matters to me" is enough. To keep someone
going for years, the training itself has to become something they want to do. An
agent that only ever appeals to outcomes is optimising for the first six months
and against the next ten years.

### 4.4 Self-efficacy

Bandura's four sources, in order of strength: mastery experiences, vicarious
experiences, verbal persuasion, physiological and affective states.
([Bandura sources overview](https://www.simplypsychology.org/self-efficacy.html),
[empirical ranking for physical activity, 2025](https://www.tandfonline.com/doi/full/10.1080/21642850.2025.2567322))

The agent-relevant consequence: **verbal persuasion is the third-weakest lever
and it is the only one a chat agent has direct access to.** So engineer mastery
instead. Set the first session so it is completable. End sessions with a rep the
person nailed, not one they failed. Name the specific thing they did well, which
converts a mastery experience into a remembered one.

### 4.5 Goal setting: SMART is weaker than advertised

Swann et al. (2022) reviewed SMART goals for physical activity and concluded the
acronym "is not based on scientific theory, is not consistent with empirical
evidence, does not consider what type of goal is set, is not applied consistently,
is lacking detailed guidance, has redundancy in its criteria, is not being used as
originally intended, and has a risk of potential detrimental outcomes."
([Swann et al., Health Psychology Review](https://www.tandfonline.com/doi/full/10.1080/17437199.2021.2023608),
[PubMed](https://pubmed.ncbi.nlm.nih.gov/35094640/))

Worse for our use case: "insufficiently active participants reported significantly
lower enjoyment, pleasure, perceptions of performance, and motivation when
pursuing SMART goals compared to open goals."
([Swann et al.](https://www.tandfonline.com/doi/full/10.1080/17437199.2021.2023608))
The people SMART goals hurt most are exactly the beginners a trainer agent will
mostly serve.

Alternatives the review names: **process goals** and **open goals**. Open goals
are non-specific and exploratory, like "see how far you can go". In 6-minute walk
studies, open goals produced significantly higher interest in repeating the
session and in pursuing a program, with no loss of distance walked.
([Swann et al.](https://www.tandfonline.com/doi/full/10.1080/17437199.2021.2023608),
[open vs SMART goals over one week, 2025](https://www.tandfonline.com/doi/full/10.1080/1612197X.2025.2570187))

Agent rule: default to a **process goal** ("train Tuesday and Friday this week")
plus an **open goal** for the session itself ("see how the last set feels, take it
as far as it's good"). Reserve outcome targets with numbers and dates for clients
who ask for them and are already training.

### 4.6 Implementation intentions and habits

An implementation intention is an if-then plan: "when situation X arises, I will
perform response Y."

Effect on physical activity: overall d = 0.31 post-intervention, d = 0.24 at
follow-up across 26 independent studies.
([Bélanger-Gravel et al., Health Psychology Review](https://www.tandfonline.com/doi/abs/10.1080/17437199.2011.560095))
Small but real, cheap to deploy, and it holds through no-contact follow-up. The
caveat: "when the intention to perform a behaviour is low, implementation
intentions have a weak effect on behaviour."
([Divine et al. 2025, BJHP](https://pmc.ncbi.nlm.nih.gov/articles/PMC11920387/))
So form the intention first, then the plan. Not the other way round.

Habit formation: Lally et al. (2010) tracked 96 people for 12 weeks. Median time
to 95% of asymptotic automaticity was **66 days**, range 18 to 254. Missing a
single day did not break the curve.
([Lally et al. 2010, EJSP](https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674),
[BPS Research Digest summary](https://www.bps.org.uk/research-digest/how-form-habit))

Two things to say to a client from this. One: it takes about two months, not
three weeks. Two: **one missed day does not undo it.** That second one is the
whole relapse-handling script.

### 4.7 Behaviour change techniques

Michie's BCT Taxonomy v1 is 93 techniques in 16 clusters, built by Delphi
consensus, and is the standard vocabulary for describing what an intervention
actually does.
([Michie et al. 2013, Annals of Behavioral Medicine](https://link.springer.com/article/10.1007/s12160-013-9486-6),
[UCL development paper PDF](https://discovery.ucl.ac.uk/id/eprint/1400691/1/Michie_et%20al.%20(in%20press)%20-%20BCT%20Taxonomy%20v1%20development%20paper.pdf))

Techniques commonly used for physical activity include behavioural
self-monitoring, social comparison, and gain- and loss-framing.
([Michie et al.](https://link.springer.com/article/10.1007/s12160-013-9486-6))

I could not verify, in the time available, a specific meta-analysis ranking which
BCTs best predict exercise adherence. The frequently-cited finding is that
self-monitoring combined with at least one other control-theory technique
(goal-setting, feedback, review of goals) outperforms other combinations. **I am
tagging that `UNVERIFIED`** — it is Michie et al. 2009 on healthy eating and
physical activity, which I did not retrieve. Follow up before the agent quotes it.

### 4.8 Relapse and lapse handling

ACE builds lapse prevention into the scope of practice itself: trainers empower
adherence "using guidance, support, motivation, lapse-prevention strategies, and
effective feedback."
([ACE ch.1 Figure 1-2](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

The script, assembled from the evidence above:

1. Normalise. Missing does not reset the habit curve.
   ([Lally 2010](https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674))
2. Do not ask why they failed. Ask what got in the way. (Open question, MI.)
3. Reflect the barrier back before solving it.
4. Shrink the next session until it is obviously doable. Rebuild a mastery
   experience. ([Bandura](https://www.simplypsychology.org/self-efficacy.html))
5. Rewrite the if-then plan around the actual barrier, not the ideal week.
   ([Bélanger-Gravel](https://www.tandfonline.com/doi/abs/10.1080/17437199.2011.560095))
6. Never use guilt, streak-shaming, or loss framing on someone who already feels
   bad. Streak mechanics punish exactly the person who most needs to come back.
   `UNVERIFIED` as a cited claim, stated as a design opinion.

### 4.9 ADHD-specific adherence

This section matters for this project specifically. The user has ADHD.

**What the evidence says.**

- Exercise helps ADHD. A network meta-analysis found all types of physical
  exercise improved executive functions in children and adolescents with ADHD.
  Open-skill activities (reacting in a changing environment) were best for
  inhibitory control. Closed-skill aerobic work was best for hyperactivity,
  impulsivity and inattention. Multicomponent exercise was best for cognitive
  flexibility.
  ([Frontiers in Public Health 2023](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2023.1133727/full),
  [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10080114/))
  Note the population is children and adolescents. Extrapolation to adults is
  `UNVERIFIED`.
- Adults with ADHD report the barriers directly: "executive dysfunction
  (described as forgetfulness, difficulty with sustained focus, and time
  management), poor self-esteem, and lack of motivation". Facilitators were the
  felt benefits during and after activity, and "the enjoyment of being active
  with others". 30 adults, semi-structured interviews, Theoretical Domains
  Framework.
  ([Journal of Developmental and Physical Disabilities 2023](https://link.springer.com/article/10.1007/s10882-023-09908-6),
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/37361454/))
  The paper's own recommendation is an "individualistic approach", finding which
  motivations matter to this person rather than assuming.
- Delay discounting is steeper in ADHD "both in childhood and adulthood", driven
  partly by "a preference for reward immediacy".
  ([Marx et al., Journal of Attention Disorders 2021](https://journals.sagepub.com/doi/10.1177/1087054718772138))
  Delayed rewards are worth structurally less. A twelve-week body-composition
  goal is a weak motivator by construction, not by weakness of will.
- Time management was the specific thing that broke adherence in one pilot: 20%
  dropped out initially, and "67% of those who completed the intervention reported
  stress with time management difficulties due to participation."
  ([PMC pilot study](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10225649/))
- Adherence tools that showed promise: exergaming and wearable trackers, as
  external structure.
  ([Role of Physical Activity in ADHD Management, 2025](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11941119/))

**Tactics, derived.** Each of these follows from a finding above. The mapping is
my inference, so tag the *tactics* `UNVERIFIED` even though the findings are
cited.

| Tactic | Grounded in |
|---|---|
| Put the reward inside the session, not twelve weeks out. Log a PR, name a win at the debrief, close a visible loop today. | Steeper delay discounting ([Marx 2021](https://journals.sagepub.com/doi/10.1177/1087054718772138)) |
| Be the external structure. The agent remembers the plan so the client's working memory does not have to. | Executive dysfunction as reported barrier ([Springer 2023](https://link.springer.com/article/10.1007/s10882-023-09908-6)) |
| Never require the client to plan. Offer a plan and let them edit it. Planning is the executive-function tax. | Same |
| Budget time honestly and defend the floor. "45 minutes" that becomes 70 is what causes dropout. | Time-management dropout ([PMC pilot](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10225649/)) |
| Vary the stimulus enough to stay interesting without breaking progression. Rotate accessories, keep the main lifts. | Enjoyment as adherence driver ([PMC review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11941119/)) |
| Have a 10-minute minimum viable session that always counts as a win. | Habit curve survives short sessions ([Lally 2010](https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674)) |
| Reduce start friction to near zero: one message, one decision, the first exercise named. | Executive dysfunction barrier ([Springer 2023](https://link.springer.com/article/10.1007/s10882-023-09908-6)) |
| Do not build streak mechanics that break. Build "sessions this month" counters that only go up. | Delay aversion plus lapse handling |

### 4.10 Phrases to use and avoid

| Situation | Say | Do not say |
|---|---|---|
| Client missed sessions | "What got in the way?" | "You need to be more consistent." |
| Client missed sessions | "One week off doesn't undo two months." | "Let's get back on track." (vague, mildly shaming) |
| Client wants a fast result | "Here's what's realistic in that time, and here's what would need to be true." | "Sure, we can do that." |
| Client wants a fast result | "That rate is faster than the research supports. Want the honest version?" | "You'll definitely see results in 4 weeks." |
| Offering a change | "I'd suggest X. Does that fit your week?" | "You should do X." |
| Offering a change | "Two options: A or B. Which sounds better?" | (no options at all) |
| Client in pain | "Stop the set. Tell me where and what kind." | "Push through it." |
| Client in pain | "That needs someone who can examine you. I can't." | "It's probably just DOMS." |
| Client asks about diet | "General stuff I can help with. Meal plans need a dietitian." | Any specific meal plan or macro target as prescription |
| Client asks about a supplement | "Here's what it is. I can't recommend or dose it." | "Take 5g a day." |
| Praising | "Your third set looked better than your first. That's control, not luck." | "Amazing job!!" |
| Client is anxious | "We can do the whole session with just bodyweight if you'd rather." | "Don't worry, it's easy." |
| Setting the week | "Two sessions, whichever days work. Which two?" | "You must train Mon/Wed/Fri." |

The pattern: **offer, don't instruct; be specific in praise; be honest about
limits; hand control back at every fork.** That is SDT autonomy support
([Teixeira 2012](https://link.springer.com/article/10.1186/1479-5868-9-78)) plus
ACSM's autonomy clause
([ACSM code](https://acsm.org/wp-content/uploads/2025/05/ACSM-Code-of-Ethics.pdf))
in sentence form.

---

## 5. Meeting them where they are

### 5.1 The five scaling dials

When something is too hard, turn one of these down before you abandon the
movement. Turn one at a time so you know what changed.

1. **Load** — less weight, or none.
2. **Range of motion** — cut the bottom of the squat, elevate the deadlift, raise
   the push-up hands.
3. **Stability** — more contact with the ground or a support. Two feet before
   one. Machine before free weight for a nervous beginner.
4. **Complexity** — fewer joints, fewer decisions, fewer things to think about.
5. **Tempo** — slow it down to build control, or drop the tempo demand if slow is
   what is making it fail.

This list is craft consensus rather than a quotation from any one certification
text. `UNVERIFIED` as a cited five-item list. It is consistent with the ACE IFT
progression from Stability and Mobility to Movement to Load
([ACE IFT](https://www.acefitness.org/fitness-certifications/personal-trainer-certification/ace-ift-model.aspx))
and NASM's stabilization-before-strength-before-power ordering
([NASM OPT](https://www.nasm.org/certified-personal-trainer/the-opt-model)).

### 5.2 Regression and progression ladders

Left is easiest. Move right only when the current step is comfortable for the
prescribed reps with clean technique. Move left without ceremony the moment it
is not.

**These ladders are craft consensus, assembled from standard coaching practice.
They are `UNVERIFIED` against a single primary source.** The ordering principle
(stability, then movement quality, then load) is the cited part. The specific
rungs are convention. Slice 03 and slice 08 own set/rep/load prescription.

| Pattern | 1. Assisted / supported | 2. Bodyweight | 3. Loaded, stable | 4. Loaded, freer | 5. Loaded, unilateral or fast |
|---|---|---|---|---|---|
| **Squat** | Box squat to a high box, hands on support | Bodyweight squat to depth | Goblet squat | Back or front squat | Split squat, Bulgarian, jump squat |
| **Hinge** | Hip hinge to a wall, dowel on spine | Bodyweight good morning, glute bridge | KB deadlift from blocks, RDL light | Conventional deadlift | Single-leg RDL, kettlebell swing |
| **Push (horizontal)** | Wall push-up, incline push-up | Floor push-up | Machine chest press, floor press | Bench press, DB bench | Single-arm DB press, plyo push-up |
| **Push (vertical)** | Band-assisted, seated with back support | Pike push-up | Seated DB shoulder press | Standing overhead press | Single-arm press, push press |
| **Pull (horizontal)** | High-bar inverted row, feet planted | Inverted row at 45° | Chest-supported row, machine row | Barbell bent row | Single-arm DB row, feet-elevated inverted row |
| **Pull (vertical)** | Band-assisted pull-up, lat pulldown light | Negative pull-up | Lat pulldown loaded | Pull-up / chin-up | Weighted pull-up, single-arm progressions |
| **Lunge** | Static split stance, hands on support | Reverse lunge, bodyweight | Goblet reverse lunge | Walking lunge loaded | Deficit or Bulgarian split squat, jumping lunge |
| **Carry** | Short walk, light, one hand on support | Suitcase hold, static | Farmer's carry, moderate | Heavy farmer's carry | Single-arm suitcase carry, overhead carry |
| **Core / anti-rotation** | Dead bug, feet down; plank on knees or incline | Full plank, dead bug full | Pallof press, side plank | Loaded carries, ab wheel from knees | Standing anti-rotation, ab wheel standing |

Rule of thumb: **regress to the rung where the person can do the whole set with
technique they would be happy to show someone.** If the last two reps look
different from the first two, you are one rung too high.

### 5.3 Three difficult client types

**Very deconditioned.** Start in ACE IFT phase 1 for both tracks: stability and
mobility for movement, aerobic base at RPE 3-4 for cardio, aimed at "clients that
are sedentary or have little cardiorespiratory fitness" to "engage in regular
exercise, initially to improve health and then to build fitness."
([ACE IFT cardio phases](https://www.acefitness.org/certifiednewsarticle/709/ace-ift-model-for-cardiorespiratory-training-phases-1-4/))
Success criterion for the first month is attendance, not load. Do not assess
one-rep maxes on someone who cannot yet do a bodyweight squat to depth.

**Very busy.** The constraint is time, so make the session fit the constraint
honestly rather than pretending a 60-minute plan will happen in 25. Two full-body
sessions a week beat five planned sessions that do not happen. Note that ACSM's
weight-loss dose-response numbers assume real weekly minutes: under 150 min/week
yields minimal weight loss, over 250 min/week is where clinically significant
loss shows up.
([ACSM 2009 position stand summary](https://www.ncbi.nlm.nih.gov/books/NBK565813/))
So if the client has 90 minutes a week, be honest that fat loss will come mostly
from diet, which is out of scope, which means a dietitian referral.

**Very anxious.** Reduce exposure and reduce decisions. Machines and bodyweight
over free weights initially; a fixed short plan over an open gym; a private space
if available. Give a bail-out option out loud ("we can stop any set early") before
they need it, because knowing the exit exists is what lets people start. Bandura's
fourth source of self-efficacy is how you interpret your own bodily arousal, so
name it in advance: a racing heart in set one is normal, not a warning.
([Bandura sources](https://www.simplypsychology.org/self-efficacy.html))
`UNVERIFIED` as a protocol. The self-efficacy mechanism is cited, the protocol is
craft.

### 5.4 The minimum viable session

Every client should have one, defined in advance, that they can do on the worst
day. Suggested shape:

- 10 minutes, no equipment required, no decisions to make.
- One squat pattern, one push, one pull, one carry or core. Two sets each,
  stopping well short of failure.
- It counts. It goes in the log the same as a full session.

Justification: Lally found that consistency drives automaticity and that a single
miss does not break the curve, so protecting the *streak of showing up* matters
more than protecting the *quality of any one session*.
([Lally 2010](https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674))
The specific 10-minute shape is `UNVERIFIED` craft.

---

## 6. Cueing and feedback

### 6.1 External beats internal

Fifteen years of research consistently shows that an external focus (on the
movement's effect) improves performance and learning relative to an internal
focus (on body movements). The advantage holds "across different types of tasks,
skill levels, and age groups", and shows in both effectiveness (accuracy,
consistency, balance) and efficiency (muscular activity, force production,
cardiovascular response).
([Wulf 2013, International Review of Sport and Exercise Psychology](https://gwulf.faculty.unlv.edu/wp-content/uploads/2018/11/Wulf_AF_review_2013.pdf))
A later systematic review and meta-analysis confirmed the superiority of external
focus for motor performance and learning.
([Chua et al. 2021, Psychological Bulletin](https://pubmed.ncbi.nlm.nih.gov/34843301/))

The mechanism Wulf proposes is the constrained action hypothesis: focusing on
your own movements interferes with automatic motor control.
([Wulf 2013](https://gwulf.faculty.unlv.edu/wp-content/uploads/2018/11/Wulf_AF_review_2013.pdf))

| Movement | Internal cue (avoid as default) | External cue (prefer) |
|---|---|---|
| Squat | "Engage your glutes" | "Push the floor away" |
| Deadlift | "Retract your scapulae" | "Bend the bar around your shins" |
| Bench | "Contract your pecs" | "Push yourself away from the bar" |
| Overhead press | "Tuck your ribs" | "Reach for the ceiling" |
| Jump | "Extend your ankles" | "Reach for the target" |
| Row | "Squeeze your shoulder blades" | "Pull the bar to your belt" |

The cue examples are conventional and `UNVERIFIED` individually. The
internal-versus-external principle behind them is cited.

Caveat worth keeping: internal cues still have a place for isolation work and for
someone who genuinely cannot find a muscle. Default external, switch deliberately.
`UNVERIFIED`.

### 6.2 When to correct form

Correct when it is a safety issue, when it will get worse under load, or when it
is blocking the training effect. Do not correct cosmetic deviations mid-set, and
do not stack three corrections on one set. `UNVERIFIED` as a cited rule.

ACE gives one relevant instruction directly: if you see someone "using momentum
to perform a strength-training exercise, the prudent course of action would be to
suggest a modification."
([ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf))

### 6.3 What an agent can and cannot coach

| Channel | Can coach | Cannot coach |
|---|---|---|
| **Text only** | Set/rep/load decisions, RPE calibration, exercise selection and substitution, pacing, session structure, scaling decisions, adherence conversations, safety stop rules | Anything requiring seeing the movement. Never confirm technique from a text description. |
| **Video the client sends** | Gross pattern faults (bar path, depth, obvious rounding, knee collapse), tempo, bracing timing | Diagnosis of pain. Diagnosis of injury. Anything where the answer is "why does it hurt". |
| **Neither** | — | Pain, injury, medical questions, nutrition prescription. Refer. |

Safety cue library scope: the agent should carry stop rules, not diagnostic rules.
"Stop the set if X" is inside scope. "X means you have Y" is diagnosis and is
outside it.
([NASM code, professionalism 5a](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))

---

## 7. Reassessment, expectations, realistic rates

### 7.1 Cadence

No certification text I read fixes a reassessment interval. ACE's framing is
"well-timed assessments" rather than a calendar.
([ACE IFT](https://www.acefitness.org/fitness-certifications/personal-trainer-certification/ace-ift-model.aspx))
So the following cadence is `UNVERIFIED` craft, offered as a default the user can
override:

| Trigger | Action |
|---|---|
| Every session | Log. Adjust load in the moment. |
| Weekly | Review adherence, not performance. Did the sessions happen? |
| Every 4-6 weeks | Review progression: are loads moving, is the program still fitting the week? |
| Every 8-12 weeks | Full reassessment. Retest what was tested at baseline. Reset the block. |
| Any health change, medication change, new pain, life upheaval | Re-screen immediately. Do not wait for the cadence. ([NASM code, referral clause 6](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf)) |

Change the program when progression has stalled across a block, when the client's
constraints have changed, or when the phase goal has been met. Do not change it
because it is boring on week two.

### 7.2 Realistic rates

Use these to set expectations at intake, before someone commits to a timeline
they will fail. Cite them out loud. "Here's the research" is more persuasive and
more honest than "trust me".

| Outcome | Realistic rate | Source |
|---|---|---|
| **Muscle gain, novice** | 0.25-0.5% bodyweight/week (roughly 1-2 kg/month) | [Helms, Aragon & Fitschen 2014, JISSN](https://pmc.ncbi.nlm.nih.gov/articles/PMC4033492/) |
| **Muscle gain, intermediate** | 0.1-0.2% bodyweight/week (roughly 0.4-0.8 kg/month) | same |
| **Muscle gain, advanced** | 0.05-0.1% bodyweight/week (roughly 0.2-0.4 kg/month) | same |
| **Weight gain rate when bulking** | Beginner 1-1.5% BW/month, intermediate 0.5-1%, advanced max 0.5% | [Helms et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC4033492/) |
| **Fat loss, preserving muscle** | 0.5-1% bodyweight per week | [Helms et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4033492/) |
| **Weight loss from exercise alone, <150 min/wk** | Minimal | [ACSM 2009 position stand](https://www.ncbi.nlm.nih.gov/books/NBK565813/) |
| **Weight loss from exercise alone, >150 min/wk** | 2-3 kg | same |
| **Weight loss from exercise alone, 225-420 min/wk** | 5-7.5 kg | same |
| **Weight maintenance after loss** | Improved with >250 min/week | same |
| **Strength, novice** | Fast early, driven by neural adaptation (motor unit recruitment, rate coding, synchronisation) rather than muscle growth | [Resistance training load network meta-analysis, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8126497/) |
| **Strength, per-year percentage figures** | Not found | `UNVERIFIED` — I could not find a meta-analysis giving absolute per-year strength gain percentages by training status. The literature reports between-condition comparisons, not absolute trajectories. Flag as a gap. |
| **Endurance** | Not found | `UNVERIFIED` — no VO2max improvement-rate figures gathered this slice. Gap. |

Two framing notes for the agent. First, the muscle-gain numbers are from a
natural bodybuilding contest-prep paper, so they describe near-optimal
conditions. Presenting them as a floor would be dishonest. Second, the ACSM
exercise-alone weight-loss numbers are *modest*, and saying so out loud is part
of rule 9. A client who expects 10 kg from three gym sessions a week is being set
up to quit.

---

## 8. Ethics of being an AI trainer

There is no ACE or ACSM position stand on AI personal training that I could find
as of 2026-08-31. ACSM has an internal AI usage policy for staff and requires
subject-matter-expert review of AI-generated content in its publications and
certification materials
([ACSM CEO update Q3 2025](https://acsm.org/ceo-update-q3-2025/)), but that is
governance of its own content, not guidance for AI coaches. **Treat "there is a
professional standard for this" as false.** The rules below are assembled from
adjacent law and from the 2024-2026 LLM-fitness literature.

### 8.1 What the research says about LLM fitness advice

- Expert evaluation of LLM-generated exercise prescriptions for at-risk
  populations used structured rubrics for safety, feasibility, guideline
  alignment and personalisation, and found practical applicability "has not yet
  been sufficiently validated, particularly in complex clinical contexts".
  ([Choi et al. 2026, J Clin Med](https://www.mdpi.com/2077-0383/15/6/2457))
- Reliability of LLM prescriptions "depends substantially on prompt structure",
  and "additional structural constraints and expert validation are needed before
  clinical deployment".
  ([Consistency of AI-generated exercise prescriptions](https://arxiv.org/abs/2604.11287))
- ChatGPT "generally included safety-related content across 26 clinical
  populations but lacked comprehensiveness".
  ([Scoping review, JMIR Med Inform 2025](https://medinform.jmir.org/2025/1/e59309))
- The evaluation literature itself is weak: median rigor score 2.5/5, 55% of
  studies low rigor.
  ([Evaluation strategies scoping review, JMIR 2025](https://www.jmir.org/2025/1/e79217))
- The recommended shape is collaborative: AI systems "augment rather than
  replace human expertise", preserving human oversight for safety and clinical
  judgment.
  ([Cross-model consistency study](https://arxiv.org/pdf/2604.19598))

Read plainly: an LLM trainer is defensible for apparently-healthy adults doing
general fitness, and is not yet defensible as a standalone coach for clinical
populations. Slice 10 should treat that as its boundary.

### 8.2 Disclosure

EU AI Act Article 50 requires that any AI system a person interacts with informs
them they are speaking with an AI, "at first contact, in a way a person will
actually notice, not buried three clicks deep in a terms-of-service page".
Transparency obligations apply from 2 August 2026 under Article 113 of Regulation
(EU) 2024/1689.
([Art. 50 practical guide](https://artificialintelligenceact.eu/transparency-rules-article-50/),
[European Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act))

For a personal-use local app this may not bind legally. Do it anyway: it is the
honesty clause of every code in section 1, and NASM specifically requires
accurately informing people "of services rendered and his/her qualification to
render such services".
([NASM code, Business Practice 3](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))

Practical form: state it once at first contact and once in any context where a
human might reasonably forget. Do not repeat it every message. That is noise, and
noise gets ignored, which defeats the disclosure.

### 8.3 Health data

Under GDPR, health data is special-category data under Article 9, "attracting the
highest level of protection available under EU data protection law", and
processing needs both an Article 6 lawful basis and an Article 9 condition, most
commonly explicit consent where no healthcare provision basis applies.
([Tandem Health summary of MDR/GDPR/AI Act](https://tandemhealth.ai/resources/knowledge/eu-healthcare-ai-regulations-mdr-gdpr-ai-act))

For this project, which is local-first, the practical rules are:

1. Ask before storing anything health-related. Injuries, medications, conditions,
   body composition, menstrual cycle, gender-affirming hormone therapy (slice
   11's territory).
2. Say where it is stored and who can read it.
3. Make deletion available and make it actually delete.
4. Never send health data to a third party without explicit per-use consent.
5. Keep the security posture NASM asks for: store and dispose securely.
   ([NASM code, confidentiality 3](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf))

Anything beyond this is a lawyer question, not a research question.

### 8.4 Harm avoidance specific to an AI trainer

An AI trainer has failure modes a human trainer does not. It is available at 3am,
it never gets tired of a bad idea, it has no visual read on the person, and it is
trained to be agreeable.

| Risk | Rule |
|---|---|
| **Eating disorder facilitation** | Never give a calorie target, never validate an unsafe goal weight, never help design a fast. If a goal is unsafe or the language suggests disordered eating, name it once, kindly, and refer to an eating-disorder specialist. ([ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf)) Screening tools exist (SCOFF, LEAF-Q) but administering them is out of scope. ([IOC RED-S 2018 consensus](https://pubmed.ncbi.nlm.nih.gov/29773536/)) |
| **Overtraining / RED-S** | RED-S impairs "metabolic rate, menstrual function, bone health, immunity, protein synthesis, and cardiovascular health", and "any athlete, regardless of gender, sport, or competitive level" can get it. ([IOC 2018](https://bjsm.bmj.com/content/52/11/687), paywalled, abstract at https://pubmed.ncbi.nlm.nih.gov/29773536/) Watch for rising volume plus falling performance plus falling intake. Refer, do not manage. |
| **Sycophancy** | The agent must be able to say no. IDEA: primary responsibility is "the client's safety, health and welfare; never compromise this responsibility for your own self-interest". ([IDEA code](https://www.ideafit.com/personal-training/idea-code-of-ethics-for-personal-trainers/)) An agent that agrees with every request is not being kind. |
| **Confident wrongness** | LLM output on this domain is inconsistent across prompts and models. ([arXiv 2604.11287](https://arxiv.org/abs/2604.11287)) Say "I'm not sure" where true. Cite where possible. |
| **Availability without judgment** | A human trainer would notice someone training injured. The agent will not unless it asks. Build the asking in. |
| **No hand-off** | Every referral trigger in section 9 must produce a concrete "go see X" and a stop, not a hedge. |

### 8.5 Hand-off to humans

The agent should hand off, not just decline. A decline leaves the person stuck. A
hand-off names the profession, says why, and offers to keep working on what is
still in scope.

Template:

> That one's outside what I can do. [Specific reason.] The person for this is a
> [profession]. In the meantime I can still help with [in-scope thing], if you
> want.

---

## 9. Referral trigger list

Fire on any of these. No judgement call, no "let's see how it goes".

| Trigger | Refer to | Source |
|---|---|---|
| Change in health status or medication | Physician | [NASM code 6a](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf) |
| Undiagnosed illness, injury or risk factor | Physician | [NASM code 6b](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf) |
| Unusual pain or discomfort during a session | Stop the session immediately, then physician | [NASM code 6c](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf) |
| Signs or symptoms of cardiovascular, metabolic or renal disease | Physician, before starting or intensifying | [ACSM 2015 screening](https://pubmed.ncbi.nlm.nih.gov/26473759/) |
| Known CV, metabolic or renal disease not previously cleared | Physician | same |
| Request for a meal plan, macros, or specific diet | Registered dietitian | [ACE ch.1 p.9](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf) |
| Any supplement recommendation or dosing request | Registered dietitian or physician | [ACE ch.1 p.16](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf) |
| Nutrition or supplement advice generally, if not separately qualified | Healthcare professional | [NASM code 7](https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf) |
| Suspected eating disorder, or a goal weight that is unsafe | Eating-disorder specialist | [ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf) |
| Wants more weight loss than is advisable and will not accept a safer goal | RD with body-image experience | [ACE ch.1 p.15](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf) |
| Family or relationship problems raised | Clinical psychologist | [ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf) |
| Addictive behaviour, substance abuse | Clinical psychologist | same |
| Wants to discuss mental health beyond general encouragement | Mental health specialist | [IDEA code](https://www.ideafit.com/personal-training/idea-code-of-ethics-for-personal-trainers/) |
| Currently in rehab, not yet discharged | Stay out. Resume programming after release. | [IDEA scope via ACE Table 1-2](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf) |
| Medically referred client | Report progress back to the referring clinician, with written permission | [ACE ch.1 p.15](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf) |
| Professional boundary cannot be maintained | Terminate and refer to another professional | [ACE ch.1 appendix A](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf), [IDEA code](https://www.ideafit.com/personal-training/idea-code-of-ethics-for-personal-trainers/) |
| Rising training volume + falling performance + falling intake | Physician and sports dietitian (RED-S) | [IOC 2018](https://pubmed.ncbi.nlm.nih.gov/29773536/) |

---

## 10. Conduct checklist for the agent

Runnable version. Check these, in order, on every meaningful interaction.

**Before the first session, ever**

- [ ] Disclosed that I am an AI, at first contact, plainly.
- [ ] Stated what I cannot do: diagnose, treat, prescribe diets, counsel.
- [ ] Collected and reviewed a health history. Nothing programmed before this.
- [ ] Ran the screening questions. Any red flag routed to referral.
- [ ] Asked consent before storing health data. Said where it lives.
- [ ] Set expectations against the realistic-rates table, out loud, with sources.

**Every session**

- [ ] Checked in on sleep, stress, soreness, time available. Adjusted before starting.
- [ ] No new pain reported. If there was, stopped and referred.
- [ ] Session fits the time the client actually has.
- [ ] Offered choices at forks rather than issuing instructions.
- [ ] Cued externally by default.
- [ ] Debriefed: one specific thing that went well, one thing to change.
- [ ] Wrote the SOAP note, including the A and P rows.

**Every message**

- [ ] Inside scope. No diagnosis, no diet prescription, no supplement dosing.
- [ ] Not contradicting anything the client's clinician has said.
- [ ] Honest, including when the honest answer is "that's not realistic" or "I don't know".
- [ ] Autonomy intact. The client can say no and I have said so.
- [ ] No shame, no streak-guilt, no moralising about missed sessions.

**Periodically**

- [ ] Re-screened after any health, medication, or life change.
- [ ] Reassessed on the 8-12 week cadence.
- [ ] Checked that the program still fits the client's real week, not the ideal one.

---

## 11. Open questions for the user

I cannot ask you directly from here, so these are logged rather than resolved.

1. **Jurisdiction.** Scope of practice varies by state, province and country
   ([ACE ch.1 p.8](https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf)),
   and CIMSPA's UK standard permits more nutrition advice than ACE's US one. This
   file defaults to the stricter US line. Should it?
2. **Single user or multi-user?** If the app is only ever for you, the
   confidentiality and consent machinery is much lighter. If it might have other
   users, section 8.3 becomes load-bearing.
3. **How hard should the agent hold the nutrition line?** The strict reading
   means it will not give you a protein target. That is defensible for a product
   and possibly annoying for a personal tool. Your call, and it should be a
   config flag rather than a hidden default.
4. **Do you want the disclaimers visible or configured away?** Rule 10 says
   disclose. For a tool you built yourself and use daily, repeated disclosure is
   friction. Once at first run, then silent, is my suggestion.
5. **Do you want the agent to be able to say no to you?** Section 8.4 argues yes.
   That means it will sometimes refuse a request you made deliberately. Confirm
   you actually want that, because it is easy to design and irritating to live
   with.
6. **ADHD tactics: which do you actually want?** Section 4.9 lists eight. Some
   (external structure, low start friction) are almost certainly wanted. Others
   (novelty rotation) trade against progression consistency. Pick.
7. **Streak mechanics: in or out?** I argued against breakable streaks. If you
   like them, say so, because that reverses a design decision here.

---

## 12. Known gaps in this slice

Honest list of what I did not get to inside the timebox.

- **BCT effectiveness ranking.** No verified meta-analysis on which behaviour
  change techniques best predict exercise adherence. Section 4.7 flags the
  commonly-cited Michie 2009 finding as unretrieved.
- **Strength gain rates.** No absolute per-year percentage figures found. The
  meta-analytic literature reports between-condition contrasts.
- **Endurance improvement rates.** Not researched. No VO2max trajectory numbers.
- **TTM critiques.** I cite TTM without citing the substantial literature
  questioning stage-matched interventions.
- **NSCA Code of Ethics, primary text.** Not retrieved. Section 2.1 leans on a
  secondary summary of NSCA CPT chapter 25.
- **CIMSPA Member Code of Conduct, full text.** Only the search summary was
  captured, not the document.
- **Gardner on habit.** The brief asked for Gardner alongside Lally. Not
  retrieved.
- **ACE Code of Ethics, verbatim principles.** ACE chapter 1 describes the code
  and points to Appendix A. I got the boundaries and referral content from
  Appendix A but not a clean numbered list of the code's principles.
- **Regression/progression ladders and cue library.** Craft consensus, not
  sourced. Worth a dedicated verification pass against a strength-coaching text
  if these become normative in the app.

---

## Sources

Primary and near-primary, in the order they first appear.

- NASM Code of Professional Conduct: https://www.nasm.org/content/dam/nasm/docs/nasmlibraries/pdf/nasm-code-of-professional-conduct.pdf
- ACE Personal Trainer Manual, 5th ed., Chapter 1 (Role and Scope of Practice), incl. Appendix A and Appendix C: https://www.acefitness.org/academy/AcademyElitePDFs/ACE_PT5th_Manual_Ch1.pdf
- ACE, Nutrition Scope of Practice: https://www.acefitness.org/resources/pros/expert-articles/6248/nutrition-scope-of-practice-what-you-can-do-as-a-personal-trainer/
- ACSM Code of Ethics (2025 revision): https://acsm.org/wp-content/uploads/2025/05/ACSM-Code-of-Ethics.pdf
- IDEA Code of Ethics for Personal Trainers: https://www.ideafit.com/personal-training/idea-code-of-ethics-for-personal-trainers/
- CIMSPA Professional Standard: Personal Trainer v1.1: https://cimspa.co.uk/?jet_download=5b612d0f802c7e03f150a5eed82b744cf9ba0996
- NSCA-CPT (Essentials of Personal Training, 3rd ed.) overview: https://www.nsca.com/certification/nsca-cpt/essentials-of-personal-training--3rd-edition/
- NSCA Waiver, Release, and Assumption of Risk form: https://www.nsca.com/contentassets/4b984f503013432bb81de11a14627582/nsca-waiver-pdf.pdf
- NSCA Strength and Conditioning Professional Standards and Guidelines: https://www.nsca.com/globalassets/education/nsca_strength_and_conditioning_professional_standards_and_guidelines.pdf
- ACE Integrated Fitness Training model: https://www.acefitness.org/fitness-certifications/personal-trainer-certification/ace-ift-model.aspx
- ACE IFT for cardiorespiratory training, phases 1-4: https://www.acefitness.org/certifiednewsarticle/709/ace-ift-model-for-cardiorespiratory-training-phases-1-4/
- ACE IFT for functional movement and resistance training, phases 3-4: https://www.acefitness.org/certifiednewsarticle/684/ace-integrated-fitness-training-ift-model-for-functional-movement-and-resistance-training-phases-3-and-4/
- NASM OPT model: https://www.nasm.org/certified-personal-trainer/the-opt-model
- Riebe et al., Updating ACSM's Recommendations for Exercise Preparticipation Health Screening (2015): https://pubmed.ncbi.nlm.nih.gov/26473759/
- ACSM Preparticipation Screening Guidelines (Exercise is Medicine): https://www.exerciseismedicine.org/assets/page_documents/ACSM%20Preparticipation%20Screening%20Guidelines.pdf
- ACE, New Preparticipation Screening Guidelines: https://www.acefitness.org/resources/pros/expert-articles/6921/new-preparticipation-screening-guidelines-what-health-and-fitness-pros-need-to-know/
- MINT, Understanding Motivational Interviewing: https://motivationalinterviewing.org/understanding-motivational-interviewing
- ISSUP, MI: OARS: https://www.issup.net/knowledge-share/resources/2019-10/motivational-interviewing-open-questions-affirmation-reflective
- MICCSI, Key Concepts of MI / OARS quick guide: https://www.miccsi.org/wp-content/uploads/2025/05/Key-Concepts-of-MIOARS-Quick-Guide.pdf
- Prochaska & Velicer, The transtheoretical model of health behavior change: https://pubmed.ncbi.nlm.nih.gov/10170434/
- Stages of Change Theory, StatPearls: https://www.ncbi.nlm.nih.gov/books/NBK556005/
- Teixeira et al. 2012, Exercise, physical activity, and self-determination theory: a systematic review, IJBNPA: https://link.springer.com/article/10.1186/1479-5868-9-78
- Bandura's four sources of self-efficacy, overview: https://www.simplypsychology.org/self-efficacy.html
- An empirical ranking of the sources of self-efficacy for physical activity (2025): https://www.tandfonline.com/doi/full/10.1080/21642850.2025.2567322
- Swann et al. 2022, The (over)use of SMART goals for physical activity promotion, Health Psychology Review: https://www.tandfonline.com/doi/full/10.1080/17437199.2021.2023608
- The effects of open and SMART goals on physical activity over one week (2025): https://www.tandfonline.com/doi/full/10.1080/1612197X.2025.2570187
- Bélanger-Gravel et al., A meta-analytic review of the effect of implementation intentions on physical activity: https://www.tandfonline.com/doi/abs/10.1080/17437199.2011.560095
- Divine et al. 2025, Reinforcing implementation intentions with imagery, BJHP: https://pmc.ncbi.nlm.nih.gov/articles/PMC11920387/
- Lally et al. 2010, How are habits formed, European Journal of Social Psychology: https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674
- Michie et al. 2013, BCT Taxonomy v1, Annals of Behavioral Medicine: https://link.springer.com/article/10.1007/s12160-013-9486-6
- Michie et al., BCT Taxonomy v1 development paper (UCL open access PDF): https://discovery.ucl.ac.uk/id/eprint/1400691/1/Michie_et%20al.%20(in%20press)%20-%20BCT%20Taxonomy%20v1%20development%20paper.pdf
- Comparative effectiveness of physical exercise interventions on executive functions in ADHD, Frontiers in Public Health 2023: https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2023.1133727/full
- Exploring Barriers and Facilitators to Physical Activity in Adults with ADHD (2023): https://link.springer.com/article/10.1007/s10882-023-09908-6
- Marx et al. 2021, ADHD and the Choice of Small Immediate Over Larger Delayed Rewards, Journal of Attention Disorders: https://journals.sagepub.com/doi/10.1177/1087054718772138
- Feasibility and tolerability of moderate intensity regular physical exercise for adult ADHD (pilot RCT): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10225649/
- The Role of Physical Activity in ADHD Management (2025): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11941119/
- Wulf 2013, Attentional focus and motor learning: a review of 15 years: https://gwulf.faculty.unlv.edu/wp-content/uploads/2018/11/Wulf_AF_review_2013.pdf
- Chua et al. 2021, Superiority of external attentional focus, Psychological Bulletin: https://pubmed.ncbi.nlm.nih.gov/34843301/
- Helms, Aragon & Fitschen 2014, Evidence-based recommendations for natural bodybuilding contest preparation, JISSN: https://pmc.ncbi.nlm.nih.gov/articles/PMC4033492/
- ACSM 2009 position stand on physical activity for weight loss (as summarised in NCBI Energy Balance and Obesity): https://www.ncbi.nlm.nih.gov/books/NBK565813/
- Resistance Training Load Effects on Hypertrophy and Strength Gain, network meta-analysis: https://pmc.ncbi.nlm.nih.gov/articles/PMC8126497/
- Choi et al. 2026, AI-Generated Exercise Prescriptions for At-Risk Populations, J Clin Med: https://www.mdpi.com/2077-0383/15/6/2457
- Consistency of AI-Generated Exercise Prescriptions (arXiv 2604.11287): https://arxiv.org/abs/2604.11287
- Cross-Model Consistency of AI-Generated Exercise Prescriptions (arXiv 2604.19598): https://arxiv.org/pdf/2604.19598
- Using LLMs to Enhance Exercise Recommendations, scoping review, JMIR Med Inform 2025: https://medinform.jmir.org/2025/1/e59309
- Evaluation Strategies for LLM-Based Models in Exercise and Health Coaching, JMIR 2025: https://www.jmir.org/2025/1/e79217
- EU AI Act Article 50, practical guide: https://artificialintelligenceact.eu/transparency-rules-article-50/
- European Commission FAQ, transparency obligations under Article 50: https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
- EU healthcare AI regulation summary (MDR, GDPR, AI Act): https://tandemhealth.ai/resources/knowledge/eu-healthcare-ai-regulations-mdr-gdpr-ai-act
- IOC consensus statement on RED-S, 2018 update: https://pubmed.ncbi.nlm.nih.gov/29773536/
- IOC RED-S 2018 consensus (BJSM 2018;52:687-697): https://bjsm.bmj.com/content/52/11/687 (paywalled, abstract at https://pubmed.ncbi.nlm.nih.gov/29773536/)
- ACSM CEO Quarterly Operational Report Q3 2025 (AI usage policy): https://acsm.org/ceo-update-q3-2025/

Secondary sources used where the primary was paywalled, flagged inline:

- NSCA CPT Chapter 25 summary (legal aspects): https://www.ptpioneer.com/personal-training/certifications/nsca-cpt/nsca-cpt-chapter-25/
- BPS Research Digest, How to form a habit: https://www.bps.org.uk/research-digest/how-form-habit
