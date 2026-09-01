# Open questions: resolution sweep

Date 2026-09-01. Covers 32 unswept rows from the two synthesis tables plus 3
re-checks of agent picks awaiting veto. Rows the user settled today (S3, S6-S8,
S11-S16, S19, S21-S25, S31, T3, T4, T12, T15) are out of scope and absent.

Verdicts: **SETTLED** research decides. **INTAKE** agent asks the user at
runtime. **TASTE** only Nicole picks. **GAP** corpus silent.

Counts: SETTLED 24, INTAKE 5, TASTE 4, GAP 2.

## Resolution table

| id | question | verdict | decision | evidence | conf |
|---|---|---|---|---|---|
| S2 | Paid Claude plan? | SETTLED | Moot. 01 q7's only job was ranking the runner-up for a friend. S1 picked Notion Free, so plan status buys nothing | 01 open q7 | high |
| S4 | Agent runs unattended? | GAP | No | 06 §behaviour-change ("no randomised trial on reminders"); 04 §5.2 opt 3 | low |
| S5 | Does the "Jim" app come back? | TASTE | See Taste calls | 01 open q5 | n/a |
| S9 | Liftoscript: reimplement or vendor? | SETTLED | Write own grammar. Liftosaur client is AGPL-3.0, server OSS status unproven, API Pro-gated. Vendoring drags AGPL into a personal log. 04 §1.2 already has a representation | 05 App A.2 licence table; 04 §1.2 | high |
| S10 | Apple Health / Health Connect? | SETTLED | Skip. Both model sessions, not sets. Buys a calorie estimate and a closed ring, not the log | 05 open q6 | med |
| S17 | RPE: accept-if-typed, never prompted *(re-check)* | SETTLED | **Pick holds.** Zourdos 2016: novices under-rate maximal sets (8.96 vs 9.80, p=0.023). 03 rule 20 hard-gates RPE off below 1yr training age. 03 conflict table: "Do not require RPE from novices". 03's own intake q3 calls dropping RPE "a legitimate choice" | 03 §7; 03 rule table row 20; 03 conflicts; kb "Novel Resistance Training-Specific RPE Scale Measuring Repetitions in Reserve" | high |
| S26 | `20x8` grey band: guess from last set *(re-check)* | SETTLED | **Pick holds, cited passage is wrong.** 04 §2.6 does not say "never open a dialogue mid-set"; it says never ask twice per exercise, never reject a line. Real support is 04 §3: carry-forward priority 2 is last session's actual weight, and "if a wrong guess is one word to reverse, the agent can guess aggressively". Fix the citation in the synthesis | 04 §3 carry-forward + undo; 04 §2.6 (contra the synthesis's paraphrase) | high |
| S27 | Auto-log rest from timestamps? | SETTLED | Compute, never surface unless asked. 02's derived-field table already says `rest_seconds`: "Computed from timestamps. Never asked". 04 §5.2 ranks timestamp-derived feedback above a fake timer | 02 §derived fields; 04 §5.2 | high |
| S28 | Readiness block: one 1-5, skippable *(re-check)* | SETTLED | **Pick holds, with a named cost.** 02 §4 recommends one 1-5 integer over four fields; four usually-blank fields teach skipping. Cost stated in synthesis delta 10: 03's rule 5 fires on "3 consecutive nights poor sleep", one per-session number can only say "3 consecutive sessions readiness <=2". That restatement is a deviation from the sleep literature and must ship labelled | 02 §4; synthesis-system delta 10 | high |
| S29 | Per-side reps on every row? | SETTLED | Off by prompt, on by schema. 02 §2 already has `side` enum defaulting `both` and nullable `reps_left`/`reps_right`. Optional nullable columns cost nothing when unused, so no ask is needed | 02 §2 set-field table | high |
| S30 | Two-a-days? | SETTLED | Allowed. Opaque session id. 02 §8 warns against wger's `unique_together = (date, user, routine)`; synthesis delta 12 confirms | 02 §8; synthesis-system delta 12 | high |
| T1 | Which jurisdiction? | INTAKE | Ask once at setup. Scope of practice varies by state and country, and CIMSPA permits more nutrition advice than ACE. HIPAA, GDPR and state consumer-health-data law point different ways on condition flags | 12 §11 q1 (ACE ch.1 p.8); 10 §5 q1 | high |
| T2 | Solo, friends, or trainers with clients? | TASTE | See Taste calls | 10 §5 q2; 12 §11 q2; 12 §8.3 | n/a |
| T5 | Video in scope? | SETTLED | No for release 1. 07 §7's chat-only list already covers everything r1 needs: full PAR-Q+, intake, e1RM from a reported rep-max, push-up/plank/wall-sit/squat counts, knee-to-wall, talk test, session RPE, readiness, circumferences, training-age classification. The video-only list is movement screening, and 07's FMS metas say FMS does not predict injury. Note video validity is *not* the objection: telehealth assessment is well sourced | 07 §7; 07 §3.3; kb "The Utility of Physiotherapy Assessments Delivered by Telehealth" | med |
| T6 | Body composition: excluded or opt-in? | SETTLED | Body-fat percentage never, any method. 07 §4.5: BIA has poor accuracy; BIA, ADP and skinfolds all disagree with DXA with -1.8% to -10.7% systematic bias; skinfolds need one trained measurer, which does not exist here. Composition off by default for everyone, opt-in once for weight and circumference. 11 §6 defaults to performance metrics for the same reason | 07 §4.5; 07 §7 "Must skip"; 11 §6; 11 §9 q3 | high |
| T7 | Screening says "see a clinician": then what? | SETTLED | Write nothing programme-shaped. Light walking only, then gate everything behind a user-confirmed clearance flag with a date. 07 §7 already forbids maximal testing of anyone the algorithm routed to clearance; ACE scope of practice forbids programming past a referral | 07 §1 PAR-Q+/ePARmed-X+ pathway; 07 §7; 12 §2; kb "The PAR-Q+ and ePARmed-X+" | med |
| T8 | Store ExRx / Symmetric Strength tables locally? | SETTLED | Neither in r1. They feed advanced training-status classification, which 07 §11 lists as UNVERIFIED (NSCA Essentials not retrieved). Do not cache tables to serve a claim that is not sourced. Licence and reuse terms for both are unchecked, so revisit only if r2 needs percentiles | 07 §10 q7; 07 §11 evidence health check | med |
| T9 | Mobility: named restriction, or general habit? | SETTLED | Against a named restriction only. Warneke 2024 plus two further meta-analyses on chronic static stretching are in 08's source list; the general-habit case is content volume, not evidence, and it competes with training time | 08 §stretching and mobility; 08 §10 q4 | high |
| T10 | Achievement timelines, or ladder only? | SETTLED | Ladder only. 08 §Goal 6 states its timelines are coaching convention with no measured medians found; 12 §12 independently reports no absolute per-year strength-gain percentages exist, the literature only gives between-condition contrasts. Nothing to quote. The separate "missed timeline is a quit trigger" claim is unevidenced (12 §12 BCT ranking unretrieved) and should not be the stated reason | 08 §Goal 6; 08 §10 q5; 12 §12 gaps | high |
| T11 | C25k ladder with no interval-structure evidence? | SETTLED | Yes, labelled a convention. 08 §conflicts states the general rule outright: when a coaching convention and a trial disagree, the convention may still be a fine default but must be labelled one. 08 applies the same treatment to the 10% rule against Buist 2008 | 08 §conflicts and resolutions; 08 §running progression | high |
| T13 | How hard is the nutrition line? | INTAKE | Ask, store as a config flag. 12 q3 says it explicitly: a config flag, not a hidden default. The strict US reading refuses a protein target, which is right for a product and possibly wrong for a personal tool | 12 §11 q3; 12 §scope of practice; 08 §10 q6 | high |
| T14 | Sport profiles as data, or live needs-analysis script? | SETTLED | Script is the mechanism, profiles are a cached lookup, ship only sports actually used. The NSCA needs-analysis structure is in 09's well-sourced list, so the script generalises on solid ground; 20 maintained profiles are not | 09 §11 well-sourced list; 09 §10 q1 and q5 | high |
| T16 | ACWR gate hardness? | SETTLED | Soft flag. Surface the number, never block. Gabbett and the Impellizzeri critique are both in 09's well-sourced list; the critique is a conceptual attack on the ratio itself, so a hard stop would be built on a measure its own literature disputes | 09 §11; kb "Acute:Chronic Workload Ratio: Conceptual Issues and Fundamental Pitfalls" | high |
| T17 | Who is the referral? | INTAKE | Ask for the name at intake, store in config. The *policy* is settled by research: GP by default, physiotherapist for musculoskeletal complaints past two weeks. The person is a profile fact and is never defaulted | 09 §10 q4; 12 §2 (ACE Appendix A referral content) | high |
| T18 | Accept under-18 users? | TASTE | See Taste calls | 09 §10 q6; 09 §LTAD | n/a |
| T19 | Hard refuse, or logged disclaimer? | SETTLED | Hard refusal on red flags and out-of-scope requests. Not a preference: ACE scope of practice makes it mandatory, and 10's cards are written assuming it. Logged pushback with user override everywhere else, per 12 §8.4. Residue: how irritating the pushback is allowed to be is a config knob, same shape as T13 | 12 §2 scope of practice; 12 §8.4; 10 §5 q3 | med |
| T20 | How many condition cards at launch? | INTAKE | Global red flags always, plus cards chosen from what the user and first users actually have. 10 q4 recommends 5 over 25 half-checked; which 5 is a profile fact and is asked, never guessed | 10 §5 q4; 10 §condition cards | high |
| T21 | Clearance letters, or a typed summary? | SETTLED | Typed structured summary: diagnosis, intensity ceiling, movements to avoid, monitoring, date, clinician. Storing less is safer under both HIPAA and GDPR, so the answer survives T1 either way. Weak leg: 10 self-flags its data-handling section as thin pending jurisdiction, and no kb page covers document-holding obligations | 10 §4 data handling (self-flagged thin); 10 §5 q5 | med |
| T22 | HRT details, or a coarse flag? | SETTLED | Coarse flag: direction plus start date. 11 §4's adjustments table is indexed on exactly those two, and Harper 2021, Wiik 2020 and Gois 2025 all report by direction and time-on-treatment. Nothing downstream reads a dose | 11 §4 adjustments table; 11 §9 q7 | high |
| T23 | Volunteer sport eligibility policy? | TASTE | See Taste calls | 11 §9 q2; 11 §5 policy table | n/a |
| T24 | Policy-refresh mechanism? | GAP | No | 11 §5 policy table; 11 §9 q4 | low |
| T25 | Non-binary ambiguous shape: guess, or decline? | SETTLED | Answer it, and it is not guesswork. 11 §7 already gives the method: an ambiguous or de-emphasized shape means avoiding the emphasis ordinary programs default to, so ask which regions to de-emphasize and do less there. 11 §3 row "Non-binary, no HRT" says there is no separate physiology and no trans-specific evidence is needed. Declining would refuse a request ordinary programming answers | 11 §7; 11 §3 programming table; 11 §9 q5 | high |
| T26 | How hard to push the disordered-eating screen? | SETTLED | Do not screen repeatedly, react to what is said. Teti 2020 documents the pathway, so the risk is real, but administering SCOFF or LEAF-Q is outside scope of practice and 10 flags the SEES stability criteria as unverified anyway. Repeated screening is surveillance for a population already scrutinised | 11 §9 q6; 12 §8.4; 10 §6 gaps | med |
| T27 | Which ADHD adherence tactics? | INTAKE | Ask, from 12 §4.9's list of eight. Research cannot rank them: 12 §12 reports no verified meta-analysis on which behaviour-change techniques predict adherence, and the Michie 2009 finding was never retrieved. Adherence tactics are a profile fact | 12 §4.9; 12 §12 gaps | high |
| T28 | Disclaimers visible or configured away? | SETTLED | Once at first contact, once in exported documents, never per message. 12 rule 10 requires disclosure, not repetition, and per-message disclaimers are pure friction on a daily personal tool. Weak leg: ACE's numbered code principles were never retrieved (12 §12) | 12 §disclosure rule 10; 12 §11 q4; 12 §12 gaps | med |

## Taste calls

Nicole picks. No experiment settles these and no note does either.

**S5. Does the "Jim" app come back?**
- Never. Notion is the store, full stop. Costs nothing extra.
- Maybe later. Notion is a stopgap and you migrate off it. Cost: a migration you have already agreed to pay, plus CSV export discipline (S6).
- Yes, soon. Supabase or Cloudflare D1 becomes the shared backend now. Cost: reverses S1, adds a hosting bill and an auth story, kills "friends replicate it in one click".

**T2. Solo, friends, or trainers with clients?**
- You alone. Consent and confidentiality machinery is near zero. Cost: 12 §8.3 is dead weight in the repo.
- You plus friends running their own logs. Current default. Cost: light consent text, no audit log.
- Trainers with real clients. Cost: 12 §8.3 becomes load-bearing, the audit log becomes real infrastructure, and T1 stops being answerable once per install.

**T18. Accept under-18 users?**
- No, 18+ only. Cost: cut 09's LTAD section entirely.
- Yes, with a guardian-confirmed flag. Cost: LTAD becomes a hard constraint in the agent, not a reference file, plus a consent record.
- Yes, unrestricted. Cost: as above plus youth data law (COPPA in the US, GDPR-K in the EU), which T1 has to answer first.

**T23. How much does the agent volunteer about sport eligibility policy?**
- Never unless asked. Cost: a competing client can be blindsided by a rule they could have known.
- Once at intake, only if they say they compete, with a date and no opinion. Current default.
- Always surface it for competitive clients. Cost: repeatedly telling someone their eligibility is in question.

11 §9 q2 declined to pick this one deliberately, calling it a product decision
with real consequences. That refusal is why it is here and not marked SETTLED.

I cannot ask you these from inside this task, per the brief. Nicole's standing
instruction is to ask when unclear, so treat every bullet above as an open ask,
not a recommendation I have quietly made.

## Gaps

**S4. Does the agent need to run unattended?**
Searched: kb `exercise reminder notification adherence trial`, best hit 0.47 and
off-topic (a rest-timer guide). 06 §behaviour-change states outright that it
found no randomised trial on reminders. 04 §5.2 puts push notifications out of
scope without arguing the case. So the one thing that would justify building
unattended runs, evidence that scheduled prompts move adherence, is absent.
- Brief: do scheduled prompts, reminders or push notifications improve
  resistance-training adherence in adults, and does effect survive past 4 weeks?
  Prefer RCTs and the mHealth adherence meta-analyses. Search PubMed for
  reminder / prompt / push notification crossed with exercise adherence, and
  check whether any ADHD-population study exists.
- Until then the constraint from 01 q3 stands on its own: unattended rules out
  the Notion MCP's interactive OAuth and forces a REST token.

**T24. Policy-refresh mechanism for eligibility rules.**
Searched: kb `transgender sport eligibility policy` returns the four policy
pages themselves (NCAA 2025, UCI 2023, World Athletics 2023, IOC 2026) and no
page on revision cadence. 11 §9 q4's "stale within a year" is an assertion with
nothing behind it, and the live-fetch option is contradicted by fetch failures
elsewhere rather than measured (01 gaps, 05 App A.2 Cloudflare blocks).
- Brief: how often have IOC, World Athletics, UCI and NCAA revised their
  transgender eligibility rules since 2019, and what is the median interval?
  Pull each body's rule-change history and date every version.
- The answer decides between a dated "last checked" field, a scheduled
  re-research task, and live fetching. Do not pick before the cadence is known.
