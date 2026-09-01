# Three closed gaps: reminder adherence, policy-refresh cadence, under-18 clients

Written 2026-09-01. Closes S4, T24 and the research half of T18 from
`research/00-open-questions-resolution.md`. User order: "if not send agents out
to find the info required to make a decision."

Sources: `research/sources/14-gaps.tsv`. All 34 ingested to `.kb`.

---

## TL;DR

1. **Reminders do not earn an unattended agent.** No RCT tests scheduled
   reminders against resistance-training adherence. The one trial that measured
   muscle-strengthening sessions under a reminder condition found **median 2 vs
   2, no difference** (Wolner-Strohmeyer 2021). The longest trial found, 24
   months and actual strength training, was **null at p=0.57** (Baker 2020).
   Carraça 2021's 62-RCT moderator analysis found "prompts/cues" **not** a
   significant moderator, while goal setting and graded tasks were.
2. **No ADHD evidence exists.** Eight PubMed searches, zero hits. Only 7 adult
   ADHD exercise RCTs exist in all of PubMed, and adherence is not an outcome in
   any of them. T27's "ask, do not rank" ruling holds for the same reason.
3. **Eligibility policy median interval is 33-37 months, but the number is a
   trap.** Pooled median across IOC, World Athletics, UCI and NCAA is **36.6
   months** over 9 intervals. Changes are step functions triggered by external
   shocks (a CAS award, a US executive order, an IOC presidency change), not a
   clock. Three of four bodies changed between 2023 and 2026.
4. **Asking age at intake does not trigger COPPA.** FTC FAQ A.12: "The Rule does
   not require operators to ask the age of visitors." FAQ A.8: COPPA does not
   apply to information collected from adults about children. A trainer entering
   a minor client's data is the A.8 case.
5. **"We store nothing" is not the defence it sounds like.** 16 CFR 312.2
   defines *Collects* as the gathering, and *Operator* as one who "collects **or
   maintains**". The real exposure is the UK Children's Code, which names
   "general health, fitness or wellbeing apps" as in scope, sets the threshold
   at **under 18**, and makes a DPIA mandatory.
6. **The guardian consent record is 13 fields.** Full list in section 3.4. Two
   things deliberately excluded: any copy of a government ID, and any guardian
   data beyond name and contact.

---

## 1. Gap S4: do scheduled reminders improve resistance-training adherence?

### 1.1 Verdict

**No RCT found** for the strict question. No trial isolates scheduled
reminders, prompts or push notifications as the intervention with
resistance-training adherence as the outcome.

For general exercise the picture is mixed and skews weak: positive short-term
signals come from multi-component apps bundling feedback, tracking and
reminders, never from reminders alone. Where the reminder was the isolated
variable, results were null.

### 1.2 Reminder as the isolated variable

| Study | Population | n | Follow-up | Result |
|---|---|---|---|---|
| Wolner-Strohmeyer 2021 | Adults over 60 | UNVERIFIED, not in abstract | 12 wk | **Muscle-strengthening: median 2 vs 2 sessions, no difference.** Moderate PA 269 vs 173 min/wk, p=0.080 NS |
| Baker 2020 BOOST-TLC | Knee OA age 50+, **strength training** | 104 randomised, 89 completed | **24 months** | Adherence 0-10: control 4.01 (95% CI 3.03-4.99) vs TLC 3.63 (95% CI 2.70-4.56), **p=0.57, null** |
| Foccardi 2021 | Post-cardiac-rehab | 32 | 3 months | Moderate PA +244.7 min (95% CI 189.1-300.4), p<0.001; 30s sit-to-stand +2.2 reps (95% CI 1.23-3.17), p=0.03. **Pilot, n=32** |

One positive, and it is an n=32 pilot in a clinical population at 3 months. The
two trials that measured strength work found nothing.

### 1.3 Multi-component apps (reminders bundled with feedback and tracking)

| Study | Population | n | Follow-up | Result |
|---|---|---|---|---|
| Barun 2024 | Whiplash home exercise | UNVERIFIED | 6 months | Adherence 4-pt Likert median 3 [2-4] vs 2 [2-4], p=0.005. App worth about 1 Likert point |
| Srp 2026 SpiroGym | Parkinson, expiratory muscle strength training | 75; at-risk subgroup 34 | 24 wk | At-risk subgroup beta=496.9 (95% CI 130.7-863.3), p=.008; max expiratory pressure +43.1 vs +22.8 cmH2O, p=.006, **Cohen d=0.74**. **No significant 3-way interaction (p=.14) in the full sample** |
| Gavanda 2025 | Trained adults, **resistance training** | 79 | 12 wk (UNVERIFIED) | Adherence supervised 88.2%, app-guided 81.2%, PDF self-guided 52.2%. **Supervision contrast, not a reminder contrast** |

Gavanda is the closest thing to an answer and it is answering a different
question. What moved adherence 52% to 88% was a human being, not a notification.

### 1.4 Reviews and meta-analyses

| Review | Scope | Result |
|---|---|---|
| Carraça 2021 | 62 RCTs, adults with overweight or obesity | **"Prompts/cues" was NOT a significant moderator.** Goal setting (behaviour), goal setting (outcome), graded tasks and social incentive were, adjusted R-squared=0.22 |
| Tarantino 2025 | 40 studies, 16 meta-analysed, post-intervention boosters | Boosters add about **6% MVPA** over intervention alone. No SMD, CI or I-squared in the abstract, UNVERIFIED |
| Lang 2022 | 10 RCTs, n=1117, digital adjunct to home exercise | 7 of 10 favoured digital, 3 equivalent, **and the 3 equivalent trials were the longer-follow-up ones** |
| Cinthuja 2022 | 5 studies, lower-limb OA, over 12-month adherence | **No significant between-method differences beyond 12 months** |
| Van Roie 2026 | 69 studies, 36 RCTs, muscle-strengthening promotion | **Only 9 of 69 measured actual muscle-strengthening engagement.** 52 of 69 rated weak quality |
| Ibeneme 2021 | SMS reminders, 10 RCTs, n=1621 | States outright "there were no RCTs on PE" (physical exercise) in its field |
| Palmer 2021, Cochrane CD012675 | 14 trials, n=25,633, medication adherence | Boundary evidence. SMS-alone systolic BP MD **-1.55 mmHg (95% CI -3.36 to 0.25)**, CI crosses zero. Low certainty |

### 1.5 Does it survive past 4 weeks?

It attenuates, and at 24 months it is gone.

- Longest follow-up found is **Baker 2020, 24 months, strength training, null**.
- Longest positive is Barun 2024 at 6 months, general home exercise, not
  resistance training.
- Lang 2022 says it directly: digital adjuncts "likely increase exercise
  adherence in the short term, with longer term effects less certain."
- Cinthuja 2022: gains present under 12 months, nothing significant past 12.

Nobody has demonstrated durable reminder-driven resistance-training adherence.

### 1.6 ADHD population

**Not found.** No RCT in any age group tests reminders on exercise adherence in
an ADHD population.

| Search | Hits | Relevant |
|---|---|---|
| `ADHD AND exercise adherence AND intervention` | 33 | 0 |
| `ADHD AND reminder AND physical activity` | 1 | 0 |
| `(ADHD OR "attention deficit")[tiab] AND (exercise OR PA OR resistance training) AND (adherence OR compliance OR dropout OR attrition)` | 44 | 0 |
| `(ADHD OR "attention deficit")[tiab] AND (reminder* OR prompt* OR "push notification" OR mHealth OR app) AND (exercise OR "physical activity")` | 14 | 0 |
| `(ADHD OR "attention deficit hyperactivity") AND adult* AND ("resistance training" OR "strength training")` | 1 | 0 |
| `(ADHD OR "attention-deficit") AND adult* AND (exercise OR "physical activity") AND randomized controlled trial[pt]` | **7 in all of PubMed** | 0 on adherence |
| `ADHD[tiab] AND ("exercise adherence" OR "physical activity adherence")` | 2 | 0, both children |
| `(ADHD OR "attention deficit") AND ("implementation intention" OR "habit formation" OR reminder*) AND (exercise OR PA OR gym)` | 1 | 0 |

Closest work, neither answering the question:

- **Zhu 2025**, mHealth tailored exercise RCT, ADHD children 6-12, n=144, 12 wk,
  3 arms. Outcomes are symptoms and executive function, **not adherence**. Its
  own stated limitation: "Lack of posttraining follow-up."
- **Schoenfelder 2017**, adolescents with ADHD, **n=11, 4 weeks, single-arm**
  feasibility. This is the entire ADHD evidence base on the question.

This independently re-confirms T27. Research still cannot rank ADHD adherence
tactics, so they stay a profile fact asked at intake.

**DECISION S4: do not build unattended runs. Reminders have no evidence in
resistance training, are null at 24 months, and "prompts/cues" is not a
significant moderator in the 62-RCT analysis; keep the agent user-initiated and
spend the effort on goal setting and graded tasks, which are.**

---

## 2. Gap T24: how fast does eligibility policy go stale?

### 2.1 Versions since 2019, with the pre-window predecessor

Publication dates. Effective dates given where they differ.

**IOC**

| Version | Published | Effective | Change |
|---|---|---|---|
| Consensus Meeting on Sex Reassignment and Hyperandrogenism | 2015-11 (UNVERIFIED, doc dated Jan 2016) | guidance | Dropped surgery requirement; T under 10 nmol/L for 12 months |
| Framework on Fairness, Inclusion and Non-Discrimination | 2021-11-16 | on release | Abandoned a single testosterone rule, 10 principles, "no presumption of advantage", devolved to each IF |
| Policy on the Protection of the Female (Women's) Category | 2026-03-26 | LA28, not retroactive | Female category limited to biological females via one-time SRY screen |

**World Athletics**

| Version | Published | Effective | Change |
|---|---|---|---|
| IAAF Eligibility Regs for the Female Classification (DSD) v1 | 2018-04-26 | 2018-11-01, stayed by CAS | T under 5 nmol/L for 6 months, restricted events 400m to mile |
| DSD Regulations v2.0 | 2019-05-01 (UNVERIFIED) | 2019-05-08 | Post-CAS reissue after the Semenya award |
| C3.5A Transgender + C3.6A Female Classification | 2023-03-23 | 2023-03-31 | Excluded post-male-puberty trans women; DSD tightened to 2.5 nmol/L for 24 months, event restriction removed |
| C3.3A Eligibility + C3.5A Implementation (SRY pre-clearance) | 2025-07-30 | 2025-09-01, applied at Tokyo | Mandatory once-in-a-lifetime SRY gene test as pre-clearance |

**UCI**

| Version | Published | Effective | Change |
|---|---|---|---|
| Transgender participation rules | 2020-01-30 | 2020-03-01 | First framework, T under 5 nmol/L for 12 months |
| Revised rules | 2022-06-16 | 2022-07-01 | Threshold halved to 2.5 nmol/L, window doubled to 24 months |
| Current rules | 2023-07-05 (UNVERIFIED, widely reported as announced 14 Jul) | 2023-07-17 | Full ban; men's renamed "Men/Open" |

**NCAA**

| Version | Published | Effective | Change |
|---|---|---|---|
| Inclusion of Transgender Student-Athletes | adopted 2010, handbook 2011-08 | 2011-12 season | One year testosterone suppression |
| Sport-by-sport participation policy | 2022-01-19 board vote, policy page 2022-01-27 (UNVERIFIED, originals now 301) | phased from 2022-23 | Deferred to each sport's NGB, else IF, else IOC |
| Phase Two and Three of the same policy | 2023-24 and 2024-25 | as scheduled | Documentation and testing step-ups. Not a new version, a phase. UNVERIFIED, no dated primary retrievable |
| Current participation policy | 2025-02-06 | immediately | Women's competition limited to student-athletes assigned female at birth |

### 2.2 Intervals

| Body | Consecutive gaps, months |
|---|---|
| IOC | 72.5, 52.3 |
| World Athletics | 12.2, 46.7, 28.3 |
| UCI | 28.5, 12.6 |
| NCAA | 125.6, 36.6 |

Pooled, all 9 sorted: `12.2, 12.6, 28.3, 28.5, 36.6, 46.7, 52.3, 72.5, 125.6`
-> **median 36.6 months**.

Restricted to intervals starting 2019 or later, dropping the two long pre-window
legs: `12.6, 28.3, 28.5, 36.6, 46.7, 52.3` -> **median 32.6 months**.

### 2.3 Why the median is the wrong number to build on

The tail is heavy and old. Every body's most recent interval is shorter than its
own median, and three of four changed between 2023 and 2026. The changes are not
periodic: World Athletics 2019 was forced by a CAS award, NCAA 2025 followed a US
executive order, IOC 2026 followed a presidency change, and that IOC policy is
currently cascading into IF rules. Shortest observed gap is 12.2 months.

Two structural findings that matter more than the median:

- **The NCAA current policy page carries no version history at all.** A stored
  "last checked" date cannot be validated against the page it points at.
- **World Athletics telegraphs.** Its 2025 SRY rule was preceded by a public
  stakeholder consultation. Changes are visible months ahead if anyone looks.

**DECISION T24: store a `policy_checked` date per body, treat it as stale at 12
months (the shortest observed interval, not the 33-37 month median), and never
live-fetch; olympics.com returned no response at all to every non-browser client
tried, so a live fetch would fail silently exactly when the policy had just
changed.**

---

## 3. Gap T18: what the tool must do for under-18 clients

Framing note: this section reports what the regulations say and cites them. It is
not legal advice, and the "operator" question in 3.5 is a facts-and-application
question the rule text does not settle.

Decided upstream: users include trainers with clients (T2), and there is no age
gate, age is asked at intake as a programming input (T18).

### 3.1 The decisive question: does asking age trigger COPPA?

**No.** Two passages settle it.

FTC COPPA FAQ A.12:

> "COPPA covers operators of general audience websites or online services only
> where such operators have **actual knowledge** that a child under age 13 is the
> person providing personal information. **The Rule does not require operators to
> ask the age of visitors.** However, an operator of a general audience site or
> service that chooses to screen its users for age in a neutral fashion may rely
> on the age information its users enter, even if that age information is not
> accurate."

FTC COPPA FAQ A.8:

> "**No.** COPPA only applies to personal information collected online **from
> children**, including personal information about themselves, their parents,
> friends, or other persons."

An adult trainer entering a minor client's data is the A.8 case. Age is also not
enumerated as personal information in 16 CFR 312.2, so the intake question
collects nothing COPPA-covered.

Three caveats that do bite:

1. **"Stores nothing" is not the defence it sounds like.** 312.2 defines
   *Collects* as "the gathering of any personal information from a child by any
   means, including... Requesting, prompting, or encouraging a child to submit
   personal information online." Collection is the gathering, not the retention.
   *Operator* is disjunctive: one who "collects **or maintains**" the
   information, or "on whose behalf such information is collected or maintained."
2. **A minor using the tool directly flips it.** FAQ A.12 closes: "If, however,
   the operator later determines that a particular user is a child under age 13,
   COPPA's notice and parental consent requirements **will be triggered**." The
   age screen then becomes the actual-knowledge trigger it was not before.
3. **Age screening is permitted, never required, and only helps a general- or
   mixed-audience service.** If the tool were "directed to children" under
   312.2, FAQ D.6 forbids blocking under-13s outright.

### 3.2 Which regime covers which ages

| Regime | Ages | Trigger | Requires |
|---|---|---|---|
| COPPA, 16 CFR 312 | Under 13 | "Directed to children" per 312.2, or actual knowledge of collecting or maintaining PI from a child (312.3) | Notice (312.4), verifiable parental consent before collection (312.5), parental review and revocation (312.6), no conditioning participation (312.7), written infosec program (312.8), written retention policy and deletion (312.10) |
| COPPA "mixed audience" | Under 13 | Directed to children but children not the primary audience, no PI collected before age determination | Neutral age screen, then full COPPA for users identified under 13 |
| US federal, 13 to 17 | 13 to 17 | **Nothing. COPPA stops at 13** | No federal children's privacy statute covers teens |
| State AADCs: Maryland (2024-10-01), Nebraska LB 504 (2026-01-01), Vermont S.69 (2027-01-01) | Under 18 for MD and VT; Nebraska threshold UNVERIFIED | Varies; both NE and VT carry revenue thresholds that likely exclude a small tool | DPIA, high-privacy defaults, minimisation, profiling and dark-pattern limits |
| California AADC (AB 2273) | Under 18 | Enjoined. 5 of 6 challenged provisions still enjoined after a Mar 2026 Ninth Circuit ruling. UNVERIFIED, search snippet only | n/a while enjoined |
| GDPR Art. 8 | Under 16, member-state floor 13 | Information society service offered **directly to a child**, processing relying on **consent** | Consent from the holder of parental responsibility, plus "reasonable efforts to verify" |
| UK Children's Code (DPA 2018 s.123) | **Under 18** | Services "likely to be accessed by" children in the UK. Not limited to services aimed at children | 15 standards, see 3.3 |

### 3.3 The UK Children's Code is the binding constraint, not COPPA

Its scope guidance names this product shape by hand:

> "This code does not apply to websites or apps specifically offering online
> counselling or other preventive services (such as health screenings or
> check-ups) to children... However, **more general health, fitness or wellbeing
> apps or services are covered.**"

And: "A child is defined... for the purposes of this code as **a person under
18**." The code applies to services "that aren't specifically aimed or targeted
at children, but are nonetheless likely to be used by under-18s." The ICO reads
"likely" as more probable than not.

Which of the 15 standards bite here:

| Standard | Bites? |
|---|---|
| 1 Best interests of the child | Yes. A minor's training load and body-composition targets are where this has teeth |
| 2 Data protection impact assessments | **Yes, mandatory** |
| 3 Age appropriate application | Yes. The intake age field is already the mechanism |
| 4 Transparency | Yes, at the child's comprehension level |
| 5 Detrimental use of data | Yes. Sharpest one here: calorie targets and weight goals for a 14-year-old |
| 6 Policies and community standards | Weak, no user community |
| 7 Default settings | Yes, high privacy by default |
| 8 Data minimisation | Yes |
| 9 Data sharing | **Yes.** The Notion write is data sharing |
| 10 Geolocation | Only if gym or location data is collected |
| 11 Parental controls | Yes, both ways. If a trainer or guardian can monitor the minor, the **child** must be told |
| 12 Profiling | **Yes.** AI-generated individualised programming from a minor's data is profiling. Off by default absent a compelling reason |
| 13 Nudge techniques | Yes. Streaks, badges, adherence prompts aimed at minors |
| 14 Connected toys and devices | Only with wearable integration |
| 15 Online tools | Yes, accessible data-rights tools |

GDPR Art. 8 itself engages narrowly: only where the lawful basis is consent under
Art. 6(1)(a), and only for services offered "directly to a child". A
trainer-operated tool is arguably outside it, and the trainer, not the tool, is
the controller. Art. 8(1) sets 16 with a member-state floor of 13; Art. 8(2)
requires "reasonable efforts to verify... taking into consideration available
technology", a proportionality test, not COPPA's enumerated method list.

Bigger than Art. 8 for this product: fitness intake data (weight, injuries,
medical restrictions, menstrual cycle) is likely Art. 9 special-category health
data, which needs an Art. 9(2) condition on top of the Art. 6 basis. Note 12
section 8.3 already carries that rule.

### 3.4 Minimal guardian consent record

| Field | Why | Rule |
|---|---|---|
| `child_id` | Consent attaches per child. Pseudonymous key, not a name, where the workflow allows | 312.5(a)(1); ICO std 8 |
| `child_dob` or `child_age_at_intake` | Selects the regime. Captured neutrally: no default value, no hint that under-13 loses features | 312.2 *Child*; FTC FAQ D.7; 312.2 mixed-audience neutrality clause |
| `guardian_name` | Names who consented | 312.4(c)(1)(i) |
| `guardian_relationship` | Parent or legal guardian, both qualify | 312.2 *Parent*, "includes a legal guardian" |
| `guardian_contact` | Channel for direct notice, the confirmatory step, and revocation | 312.4(c)(1)(vi); 312.5(b)(2)(viii) and (ix) |
| `consent_method` | Which of 312.5(b)(2)(i) to (ix) was used. Without it you cannot show the method was "reasonably calculated" | 312.5(b)(1) and (b)(2) |
| `verification_evidence_ref` | A **pointer** to the artifact, never the artifact. Signed-form reference, confirmatory-email message id, call log entry | 312.5(b)(2)(v) and (vii) both require prompt deletion of government ID after verification; GDPR Art. 5(2) |
| `consent_timestamp` | Proves consent preceded collection | 312.5(a)(1), "before any collection" |
| `scope_of_consent` | The specific data items and purposes the guardian saw | 312.4(c)(1)(iii) |
| `third_party_disclosure_consent` | **Separate** boolean, not folded into the main consent. New in the 2025 amendments | 312.5(a)(2); 312.4(c)(1)(iv) |
| `notice_version_id` | Which notice text the guardian saw. A material change needs fresh consent | 312.5(a)(1) |
| `revoked_at` (nullable) | Revocation must be recorded and honoured | 312.6(a)(3); GDPR Art. 7(3) |
| `delete_after` | The Rule now requires a deletion timeframe, not just a policy | 312.10 |

Deliberately excluded: any copy of a government ID (312.5(b)(2)(v) and (vii)
require prompt deletion once verification completes, and under the amended 312.2
a government-issued identifier is itself personal information), and any guardian
data beyond name and contact.

Verifiable parental consent methods, 16 CFR 312.5(b)(2), abbreviated: (i) signed
form by mail, fax or scan; (ii) credit or debit card or payment system notifying
the account holder of each discrete transaction; (iii) toll-free number staffed
by trained personnel; (iv) video-conference with trained personnel; (v)
government ID checked against a database, deleted promptly; (vi) knowledge-based
authentication with dynamic multiple-choice questions a child 12 or younger in
the household could not reasonably answer; (vii) government photo ID face-matched
against a webcam image, confirmed by trained personnel, both deleted promptly;
(viii) **email plus** additional steps; (ix) **text message plus** additional
steps. Both (viii) and (ix) are available only to operators that do not
"disclose" children's PI, and both must give notice that consent can be revoked.
312.5(b)(1) governs all of them: the method must be "reasonably calculated, in
light of available technology, to ensure that the person providing consent is the
child's parent."

For a small tool, (viii) and (ix) are the only affordable options, and both turn
on whether writing to a third-party workspace counts as disclosure. See 3.5.

### 3.5 What the 2025 COPPA amendments changed

Citation: **90 FR 16918 (22 Apr 2025), FTC, RIN 3084-AB20, FR Doc. 2025-05904.**
Effective 23 Jun 2025; compliance date 22 Apr 2026 except for 312.11(d)(1),
(d)(4) and (g). Both dates have passed.

| Area | Change |
|---|---|
| New definition | **Mixed audience website or online service**, formalising a previously informal category. Age information must be collected "in a **neutral manner** that does not default to a set age or encourage visitors to falsify age information" |
| *Online contact information* | Now includes mobile phone numbers, where used only to text a parent in connection with obtaining consent |
| *Personal information* | Adds government-issued identifiers (312.2(6)) and biometric identifiers (312.2(10)): fingerprints, retina and iris patterns, genetic data, voiceprints, gait patterns, facial templates |
| *Directed to children* | Added audience-composition evidence: marketing materials, representations to consumers or third parties, user reviews, age of users on similar services |
| **Separate disclosure consent** | 312.5(a)(2): the parent must be able to consent to collection and use "**without** consenting to disclosure... to third parties, unless such disclosure is integral", with separate VPC for the disclosure |
| New VPC methods | Text-message-plus (b)(2)(ix); KBA and photo-ID face-match codified at (b)(2)(vi) and (vii) |
| New 312.10 | Retention only "as long as is reasonably necessary", no indefinite retention, plus a **written retention policy** naming purposes, business need and a deletion timeframe, published in the notice |
| Expanded 312.8 | A **written information security program**: designated coordinator, annual risk assessments, sized safeguards, regular testing, annual evaluation, written assurances from third parties before they receive children's PI |
| Not finalised | Proposed ed-tech and school-authorization amendments were dropped pending the Department of Education's FERPA rulemaking |
| New 312.13 | Severability clause |

**DECISION T18: keep the no-age-gate intake; asking age does not trigger COPPA
(FTC FAQ A.12 and A.8), but when the intake age is under 18 the agent must
require a guardian consent record with the 13 fields in 3.4 before writing any
health data, and must apply the Children's Code defaults (no profiling, no
calorie or weight targets, no streak nudges) regardless of jurisdiction, because
the tool cannot know where the client is.**

---

## 4. Where this lands in the existing notes

| Note | What changes |
|---|---|
| `00-open-questions-resolution.md` S4 | GAP -> answered. No unattended runs. The 01 q3 REST-token constraint is now moot for this reason |
| `00-open-questions-resolution.md` T24 | GAP -> answered. 12-month staleness, no live fetch |
| `00-open-questions-resolution.md` T18 | TASTE -> the research half is settled. The taste half, whether to accept minors at all, is still the user's |
| `11-transgender-clients-and-hrt.md` s5 | The policy table's four anchors are all confirmed. It needs a `checked` date column |
| `10-medical-and-special-populations.md` "Children and adolescents" | Its NSCA programming content is untouched. What is new is that the card now has a consent gate in front of it |
| `12-trainer-practice-and-ethics.md` s8.3 | Its five health-data rules hold. Children's Code standards 5, 11, 12 and 13 are additions specific to minors |

Not edited. This note is the evidence; applying it is build work.

---

## 5. Fetch failures and capture gaps

| URL | Status | Handling |
|---|---|---|
| olympics.com IOC 2026 policy page | curl 000, no response; WebFetch timeout 60s | Corroborated via the NZOC republication, captured |
| olympics.com IOC 2021 framework page | curl 000; WebFetch timeout | Date sourced from PMC8739444, captured |
| stillmed.olympics.com and stillmed.olympic.org PDFs (2021 framework, 2015 consensus) | curl 000 | Not captured. IOC dates tagged UNVERIFIED above |
| NCAA 2022 policy pages (3 URLs) | 301 to current pages, original text gone | Dates from search result titles and URL paths. UNVERIFIED |
| `ncaaorg.s3.amazonaws.com` 2011 handbook and 2022 phase-in deck | Fetch 200, but llmwiki rejects `application/pdf` | **Not captured.** Removed from the TSV so every listed URL is genuinely ingested |
| eCFR versioner API XML, Federal Register JSON API | Fetch 200, llmwiki rejects `application/xml` and `application/json` | **Not captured**, but redundant: the eCFR HTML Part 312 page and the FR full-text `.txt` are both captured and carry the same text. Every 16 CFR and 90 FR quote above traces to them |
| eCFR per-section pages, ftc.gov, ico.org.uk, federalregister.gov HTML | 302 or 403 to non-browser clients | All resolved by a browser user agent and captured |
| eur-lex CELEX 32016R0679 | Not attempted | gdpr-info.eu used as the pre-authorised fallback |

The `llmwiki` PDF, XML and JSON content-type rejections are a real capture
limit, not a fetch problem. Any future source list should prefer an HTML or plain
text rendering of the same document.

---

## 6. Open questions for the user

Written here rather than asked, per the standing instruction to ask when unclear:
this note was produced without a user channel.

1. **Do you actually want to accept under-18 clients?** The research half of T18
   is closed; the taste half is not. Section 3.4's 13 fields plus a mandatory
   DPIA plus Children's Code defaults is real work. "18+ only, and say so at
   intake" remains a legitimate answer and costs one line of prompt.
2. **Is the tool ever used self-serve by a minor, or only by a trainer?** This
   flips the COPPA analysis. Trainer-only stays out under FAQ A.8. Any direct
   minor use makes the intake age question an actual-knowledge trigger under FAQ
   A.12.
3. **Which GDPR lawful basis is contemplated?** Art. 8 engages only where the
   basis is consent under Art. 6(1)(a). Under contract, Art. 9 health data
   becomes the binding constraint instead.
4. **Does the tool target UK or EU users at all?** The Children's Code's reach
   depends on it, and it names fitness apps explicitly.
5. **Is writing to the user's own Notion workspace a "disclosure" under 312.2?**
   This is the single highest-value unresolved question. If yes, consent methods
   (viii) and (ix) are unavailable and the cheap path closes. 312.2's carve-out
   for "a person who provides support for the internal operations" may cover a
   storage backend, but that turns on facts the Rule text does not settle.
6. **Publication dates or effective dates as canonical for the policy table?**
   I used publication dates throughout. Effective dates give a different median.

---

## 7. Known gaps in this note

- IOC 2015 consensus publication date. Meeting Nov 2015, document circulated Jan
  2016. Primary PDF unreachable. UNVERIFIED.
- World Athletics DSD v2.0 date (2019-05-01) comes from a PDF URL slug in search
  results, not a fetched document. UNVERIFIED.
- UCI 2023 publication date. The primary carries no dateline; the Management
  Committee met 5 Jul, rules in force 17 Jul, widely reported as announced 14
  Jul. Using 14 Jul shifts that interval from 12.6 to 12.9 months. UNVERIFIED.
- NCAA Jan 2022 dates and the 2023-24 phase-in. Originals now redirect.
  UNVERIFIED.
- No UCI action found after Jul 2023 responding to the IOC 2026 policy. Absence
  of evidence, not evidence of absence.
- Sample sizes for Wolner-Strohmeyer 2021 and Barun 2024, and Gavanda 2025's
  exact duration. Not in the abstracts. Only abstracts were read for gap 1; no
  full texts were pulled.
- Tarantino 2025's "about 6%" has no SMD, CI or I-squared in the abstract.
- Nebraska LB 504's age threshold, California AB 2273's post-Ninth-Circuit
  status, the per-member-state EU Art. 8 age table, and the list of US state
  comprehensive privacy laws with 13-to-16 opt-in rules. All UNVERIFIED.
- Whether Notion qualifies as "support for the internal operations" under 312.2.
  Open question 5 above.
