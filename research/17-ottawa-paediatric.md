# Ottawa ankle and knee rules in children and adolescents

Research slice 17. Written 2026-09-01. Answers docs/build-plan.md s6.1 rule
S4, which currently states the under-18 Ottawa threshold with no paediatric
source (`(lim L-40)`, dec "T18 final" at decisions.tsv:97). All five papers
below are captured in `.kb` (`llmwiki search "Ottawa ankle rules children
meta-analysis"`).

---

## TL;DR

Age floor is **5 years**, both rules, same number from two independent
pooled meta-analyses: Dowling 2009 for the ankle rule (12 studies, n=3,130,
pooled sensitivity 98.5%) and Vijayasankar 2009 for the knee rule (3
studies, n=1,130, pooled sensitivity 99%). Both conclude the rule is
reliable "for children over the age of 5 years" / "greater than 5 years of
age" and both say the same thing about the gap below that: "not enough good
data to advocate application." Three individual validation studies (Plint
1999 ankle, Bulloch 2003 knee, Libetta 1999 ankle) enrolled children as
young as 1-2 and still measured good sensitivity, but the pooled analyses
are the higher evidence tier and are the more conservative read, so they win.

**Rule text applies unchanged above the floor.** None of the five papers
modify the criteria (weight-bearing both immediately and in the ED, point
tenderness at the same landmarks). They test the adult rule against a
paediatric cohort, not a paediatric variant of it.

**Growth-plate caveat, stated by the source, not inferred.** Dowling names
the failure mode directly: "most missed fractures were minor (Salter-Harris
Type I or small avulsion fractures)." The rule was built and validated on
skeletally mature anatomy; open growth plates are exactly where it is
weakest, which is also the mechanistic reason the floor sits where it does
rather than lower.

---

## Evidence table

| Study | Year | n | Ages | Rule | Sensitivity | Specificity | Verdict |
|---|---|---|---|---|---|---|---|
| Dowling et al., *Acad Emerg Med* | 2009 | 3,130 (12 pooled studies, 671 fractures) | studies spanning childhood; conclusion stated for >5y | Ankle | 98.5% (95% CI 97.3-99.2) | not reported in abstract | "Reliable tool to exclude fractures in children greater than 5 years of age"; missed fractures mostly Salter-Harris I |
| Plint et al., *Acad Emerg Med* | 1999 | 670 | 2-16 | Ankle | 100% (95% CI 95-100) | 24% (95% CI 20-28) | Sensitive for clinically significant (≥3mm) fractures; no age floor stated |
| Bulloch et al., *Ann Emerg Med* | 2003 | 750 | 2-16 | Knee | 100% (95% CI 94.9-100) | 42.8% (95% CI 39.1-46.5) | "Valid in children"; no age floor stated |
| Vijayasankar et al., *Emerg Med J* | 2009 | 1,130 (3 pooled studies) | not stated in abstract; conclusion split at 5y | Knee | 99% (95% CI 94.4-99.8) | 46% (95% CI 43.0-49.1) | "High sensitivity and adequate specificity for children over the age of 5 years... not enough good data to advocate application... in children less than 5 years" |
| Libetta et al., *J Accid Emerg Med* | 1999 | 761 study / 782 historical control | 1-15 | Ankle | 98.3% | 46.9% | Before-after design; radiography rate down 7.2 points, no increase in missed fractures (1 per arm); no age floor stated |

---

## The age-floor tension, and why the meta-analyses win

Three single-site studies (Plint, Bulloch, Libetta) enrolled children down
to age 1-2 and measured sensitivity at or near 100% with no floor called out
in their own conclusions. Read alone, they would support applying the rule
much younger than 5. The two pooled analyses (Dowling for ankle, Vijayasankar
for knee) sit above those studies in the evidence hierarchy, pool more
patients, and both independently land on the same cutoff with the same
reasoning: not that the rule fails below 5, but that there isn't enough
data below 5 to say it doesn't. That is a "we can't clear this age band"
finding, not a "the rule works fine here too" finding, and for a hard-stop
safety rule the absence of a proof floor is the operative fact, not the
individual studies that happened to enroll a handful of younger children
without reporting age-stratified accuracy.

## Open questions

Flagging per the instruction that unclear points get written down, not
guessed at:

1. **Exact treatment of age 5 itself is not resolved by the abstracts.**
   Dowling says "greater than 5"; Vijayasankar splits "over 5" against
   "less than 5." Neither abstract states whether a child on their 5th
   birthday is in or out. This note resolves it conservatively for the
   DECISION line below (5-year-olds treated as below the floor); the full
   text of either paper would settle it properly and hasn't been fetched.
2. **Dowling's abstract does not report pooled specificity**, only
   sensitivity. Not load-bearing for a hard-stop refer rule (sensitivity is
   what matters for a rule that must not miss a fracture), noted for
   completeness.
3. **Vijayasankar's abstract does not state the age range of the three
   pooled studies**, only that the conclusion splits at 5. Full text not
   fetched.
4. **No paper here addresses ages 16-18 specifically** — Plint and Bulloch
   both cap their paediatric cohorts at 16. The rules are separately
   validated on adults from age ~18 up (00-synthesis-trainer.md "The Ottawa
   rules"). Nothing in this search surfaced a 16-18 gap study; the working
   assumption is that 16-18-year-olds are close enough to skeletal maturity
   that the adult validation (Stiell 1992/1993/1995/1996) covers them, but
   that is this note's inference, not a cited finding.

---

## DECISION

For `ref/red-flags`, replacing the unsourced under-18 branch in
docs/build-plan.md s6.1 rule S4:

> **For a client under 18: age 5 and up, the Ottawa ankle/knee rule text
> applies unchanged (same two-timepoint weight-bearing test, same
> tenderness landmarks) — sourced to Dowling 2009 (ankle, n=3,130, pooled
> sensitivity 98.5%) and Vijayasankar 2009 (knee, n=1,130, pooled
> sensitivity 99%). Under age 5, including exactly age 5, there is no rule
> arithmetic: any suspected ankle or knee fracture after acute injury
> refers for imaging regardless of exam findings, because the paediatric
> meta-analyses found insufficient data below that age and the rule's known
> failure mode (Salter-Harris growth-plate fracture) is concentrated
> exactly there.**

---

## Sources

All five ingested into `.kb`; see `research/sources/17-ottawa.tsv`.

- Dowling S, Spooner CH, Liang Y, Dryden DM, Friesen C, Klassen TP, Wright
  RB. Accuracy of Ottawa Ankle Rules to exclude fractures of the ankle and
  midfoot in children: a meta-analysis. *Acad Emerg Med.* 2009. PMID 19187397.
- Plint AC, Bulloch B, Osmond MH, Stiell I, Dunlap H, Reed M, Tenenbein M,
  Klassen TP. Validation of the Ottawa Ankle Rules in children with ankle
  injuries. *Acad Emerg Med.* 1999. PMID 10530658.
- Bulloch B, Neto G, Plint A, Lim R, Lidman P, Reed M, Nijssen-Jordan C,
  Tenenbein M, Klassen TP, Bhargava R; Pediatric Emergency Researchers of
  Canada. Validation of the Ottawa Knee Rule in children: a multicenter
  study. *Ann Emerg Med.* 2003. PMID 12827123.
- Vijayasankar D, Boyle AA, Atkinson P. Can the Ottawa knee rule be applied
  to children? A systematic review and meta-analysis of observational
  studies. *Emerg Med J.* 2009. PMID 19307383.
- Libetta C, Burke D, Brennan P, Yassa J. Validation of the Ottawa ankle
  rules in children. *J Accid Emerg Med.* 1999. PMID 10505914.
