# Research index

Written 2026-08-31. Start with the two syntheses; the numbered notes are the
evidence behind them. Every note has a TL;DR at the top and an "open
questions" section near the end.

## Read first

| File | What it settles |
|---|---|
| `00-synthesis-system.md` | Where the log lives, the architecture, the data-model fixes, 31 open questions with defaults |
| `00-synthesis-trainer.md` | The trainer-agent skill set, client flow, safety envelope, open questions with defaults |

## System half (how the log works)

| File | Topic |
|---|---|
| `01-storage-options.md` | Notion vs git vs wger vs 25 others, scored on the phone loop and friend replication |
| `02-data-model.md` | Sets, sessions, routines, exercise catalog; compared with Strong, Hevy, FitNotes, Liftosaur, wger |
| `03-progression-heuristics.md` | When to raise, hold, lower, or deload; every named scheme with numbers |
| `04-routines-and-logging-ux.md` | Preset routines, the set-entry grammar, "what do I have today", as-you-go flow |
| `05-existing-tools-and-formats.md` | What to reuse: exercise DBs, program DSLs, MCP servers, export formats |
| `06-trainer-agent-skills.md` | The 15-skill catalog and the evidence on LLM coaching |
| `13-plugin-packaging.md` | Packaging the skills as a git repo for Claude Code, Codex and Copilot; Remote Control and the terminal-free friend path |
| `19-notion-database-create-api.md` | The `POST /v1/databases` payload this repo must render, every claim carrying a developers.notion.com URL |
| `20-host-capability-matrix.md` | What a packaged skill can do on each host, so the trainer survives being added to a webapp chat and not just a terminal |
| `15-exercise-catalog-coverage.md` | Measured coverage of free-exercise-db and wger against an 84-exercise probe list: hit rates, 24-item true gap, schema comparison, seed-plus-extras decision |

## Trainer half (how the agent coaches)

| File | Topic |
|---|---|
| `07-baselining-and-assessment.md` | Intake script, screening, test menu with norms, re-test cadence |
| `08-goal-specific-programming.md` | Health, strength, hypertrophy, cardio, mobility, achievements, fat loss, power, two goals |
| `09-sport-specific-programming.md` | Needs analysis, periodization, load management, 24 sports, injury-prevention programs |
| `10-medical-and-special-populations.md` | 26 condition cards, clearance workflow, scope of practice, data handling |
| `11-transgender-clients-and-hrt.md` | HRT physiology timelines, programming adjustments, safety, policy, wording |
| `12-trainer-practice-and-ethics.md` | The 10 rules of conduct, communication playbook, regression ladders, AI ethics |
| `14-gaps-adherence-policy-minors.md` | Three closed gaps: reminder adherence has no RCT and is null at 24 months; eligibility-policy revision cadence and a 12-month staleness rule; under-18 clients, COPPA vs the UK Children's Code, and the guardian consent record |
| `16-program-library.md` | Free, legally shippable program templates for `library/` across all goal categories: 16 SHIP, 5 POINTER, 2 SKIP, with the copyright rule for the SHIP/POINTER split and a format-fit list feeding the s1.5 stress test |
| `17-ottawa-paediatric.md` | Ottawa ankle/knee rules in children: age floor 5 (Dowling 2009 ankle, Vijayasankar 2009 knee meta-analyses), rule text unchanged above the floor, growth-plate (Salter-Harris) caveat below it. Sources build-plan s6.1 rule S4, closing (lim L-40) |
| `18-parq-plus-verification.md` | The published PAR-Q+ checked word by word against the copy this repo used. Written for the deleted `screen` skill; kept for the form wording |
| `21-athlete-support-teams.md` | Who is on an athlete's staff, what each role owns and decides, where the boundaries get crossed, and which roles are real knowledge versus artefacts of a big organisation |
| `22-how-a-team-builds-a-program.md` | How a performance staff actually produces a plan: the calendar first, the medical gate, the nine steps with who signs off, the revision loop, and which steps survive when one person wears every hat |

## Verified by hand this session

- notion.com/pricing: Public API and Webhooks on Free; Notion Agent gated at Business.
- Obsidian Git README: mobile "very unstable", not recommended.
- ACSM resistance-training position stand, MSSE 2026-03-17: the numbers in
  `00-synthesis-system.md` and `00-synthesis-trainer.md` are re-anchored on it.

## Known gaps

Each note ends with a gaps list. The biggest: paywalled ACSM/NSCA/ACOG texts,
several vendor pricing pages behind JS or bot walls, and a few rules tagged
DERIVED that need a prototype before they ship.

## Follow-ups before any build

Owned by the next session that starts building. Each came out of the
trail review on 2026-08-31. Items 1, 3, 4 and 5 were worked on 2026-09-01.

1. **DONE.** Brzycki 1RM: ship `w / (1.0278 - 0.0278 * reps)`. The minus is
   correct. At `reps = 1` the denominator has to come to 1.0, and only the
   minus version does; a peer-reviewed table (PMC11435939) prints it that way
   too. PMC9465738 is the paper with the inverted Brzycki sign, and
   PMC11435939 is the one with a bad Epley constant — take each formula from
   the paper that gets it right. `02-data-model.md` §9.
2. **NOT STARTED.** Build the `progression: manual` off switch for the load
   rules before the PEM hard stop and the HRT branch can work
   (`00-synthesis-trainer.md`). This one is build work, not research.
3. **DONE.** Pelland et al. 2026 (PMID 41343037) read. **The 10-to-20 band does
   not move.** Volume raises hypertrophy and strength with 100% posterior
   probability and no identified ceiling, so the 20 is a recovery ceiling
   rather than an optimum; frequency turns out to be a strength variable, not
   a hypertrophy one. Bonus: its winning "fractional" set-counting method is
   the same 0.5-per-secondary-muscle weighting `02-data-model.md` had tagged
   UNVERIFIED, so that tag is retired.
   `03-progression-heuristics.md` "Volume evidence base",
   `00-synthesis-trainer.md` "ACSM 2026 re-anchor".
4. **DONE.** The "cannot bear weight after acute injury" red flag is sourced to
   four Stiell papers, all captured (`llmwiki search "Ottawa ankle rules"`).
   The real criterion is "unable to bear weight **both immediately after the
   injury and in the ED**", four steps for the knee — narrower than the note's
   old wording. UNVERIFIED tag retired in `00-synthesis-trainer.md`; note 06's
   own red-flag table still carries the old wording.
5. **DONE.** Nine flagged citations checked. **One fabrication**, the
   "Yun et al. 2023 meta" (0 PubMed hits; Gois 2025 substitution stands). The
   other eight are real; three were fetch failures that cleared through
   E-utilities, four are genuinely paywalled or blocked, and one is a
   legitimate preprint. Table in `00-synthesis-trainer.md` "Citation audit".
6. **DONE (2026-08-31).** The three "verified by hand" sources above are
   captured in `.kb` (`llmwiki search "ACSM 2026"`), so the claims can be
   re-read.

Left open after the 2026-09-01 pass: item 2, and the paywalled bodies of
Spiering 2021, DiStasio 2014 and Brzycki 1993. None of those three blocks a
build decision.

## Source library (round 3, 2026-08-31)

`research/sources/NN-<slice>.tsv` lists the most reputable primary resources
per category plus one hop of what they cite (url, title, kind, cited_by,
why, access). Every URL was fetch-checked by the list author.

Ingested into `.kb` with `scripts/ingest-sources.sh` (serial, idempotent,
PubMed URLs rewritten to the E-utilities abstract endpoint). Rerun it after
editing a list; it skips what the kb already has. Failures land in
`research/sources/ingest-failures.tsv` and `.kb/log.md`.

Result: 315 sources, 463 pages. Known holes: publisher landing pages that
block non-browser clients (doi.org to Wiley, T&F, Springer), IOC and USAPL
policy pages, eur-lex, MLB Pitch Smart. Paywalled papers are in as
abstracts only.
