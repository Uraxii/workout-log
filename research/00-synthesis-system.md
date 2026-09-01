# Synthesis: what the workout-log system should be

Covers research notes 01 to 06 (the system half). Notes 07 to 12 cover trainer
knowledge and are synthesized separately. Written 2026-08-31.

Every claim below points at the note and section it came from. Where two notes
disagreed, the disagreement is named and settled in the conflicts section.
UNVERIFIED tags carried over from the source notes are preserved as written.

---

## TL;DR

1. **Store: Notion, Free plan.** Public API and Webhooks are checkmarked on
   Free (01 TL;DR, 01 §1). The $24/mo belief was wrong; no Notion tier costs $24.
2. **Interface: the Claude mobile app with the Notion connector.** Web connectors
   work on iOS and Android for all users (01 "How the phone triggers an agent", 1).
   Verified this session: the claude.ai Notion connector read the workspace on the
   current non-Business plan.
3. **Why: the phone entry path is the chat itself.** She types `185x5` to Claude;
   Claude writes to Notion. Nothing to build, nothing to host, no terminal.
4. **Friend replication: 5 steps, no command line, $0.** Duplicate one Notion
   template page, connect the connector, say "set me up".
5. **Runner-up: markdown in a private GitHub repo.** Zero lock-in, `git commit`
   is the write path, and the derived analytics layer is free (02 §11). It loses
   because the phone trigger needs Claude Code on the web, which needs a paid
   Claude plan (01 "Friend replicates it", option 2 step 5).
6. **Dropped: Obsidian + Obsidian Git.** The plugin README says mobile is "very
   unstable" and the maintainer does not recommend it (01 TL;DR). Mobile is the
   whole point.
7. **Dropped for release 1: self-hosted wger.** Best schema in the survey, only
   official MCP server (05 TL;DR), but it needs a server, a public HTTPS endpoint,
   and Docker. Crib the schema, do not run the stack.

---

## Tradeoffs table

Columns are the user's actual loop: phone, mid-set, five seconds per entry, ADHD.

"Phone entry speed" is scored for the mid-set case, not for browsing history.
In every chat-driven option the typing is identical (`185x5` into Claude), so the
column really measures write latency and how often the agent has to stop and ask.

| Option | Agent write path | Phone entry speed | Phone trigger path | Auth / sharing | Cost | Friend steps | Lock-in | Offline |
|---|---|---|---|---|---|---|---|---|
| **Notion Free (recommended)** | REST API with internal integration token, or MCP over OAuth (01 §1, §2) | Fast. One API round trip per write; buffer per exercise, not per set | Claude mobile app + Notion connector, works for all Claude users (01, phone-trigger rank 1) | notion.com login; Publish page, or up to 10 external guests (01 §1) | $0 | **5** | Medium. Exports Markdown and CSV, as blocks not as your layout (01 open q 6) | Poor, cache only (01 table) |
| Markdown / CSV in private GitHub repo | `git commit` from Claude Code, or contents REST API (01 table) | Fast in chat. Slow for hand edits: typing a set log into a mobile code editor is not fun (01 §git-native) | Claude Code on the web, **needs Pro, Max or Team** (01 phone-trigger rank 2). Or GitHub mobile edit plus a push-triggered Action | github.com login; invite a collaborator or go public (01 table) | $0 storage, plus a paid Claude plan for the phone leg | **7** (01 prose; the 01 table says ~5, an internal inconsistency in that note) | None. Plain text, exactly the bytes you wrote (01 open q 6) | Good |
| Self-hosted wger + official MCP server | wger REST API; **auth model UNVERIFIED** (01 table). Read API needs no auth key (05 OSS table) | Fast in chat. Native Android and iOS apps exist for hand entry (01 §fitness-specific) | claude.ai custom connector pointed at your own remote MCP endpoint. Needs public HTTPS. Claude Free allows **one** custom connector (01 §4) | Self-run; sharing UNVERIFIED (01 table) | Server cost only, roughly $2/mo Fly to $5/mo Railway (01 §databases) | ~4 Docker steps (01 table), but the MCP-over-internet leg is not counted in that 4 and is the hard part | Low, AGPL-3.0 (05 OSS table) | Ok |
| Google Sheets | Sheets API v4, service account or OAuth (01 table) | Fast in chat. Native app for hand edits | No first-party Claude connector found in 01. Would need a custom MCP server, so same problem as wger | Google login; real link sharing with viewer and editor roles (01 §databases) | $0 | ~7. Needs a GCP project, an enabled API, and credentials (01 §databases) | Low, CSV and XLSX export | Ok |
| GitHub Issues as the log | Issues REST API or `gh` (01 table) | Poor as a set log. Issue bodies are not rows | Same as the git option: Claude Code on the web, paid plan | github.com login; public repo means public log | $0 | ~3, the lowest in 01's whole table | Medium, JSON export | Poor |
| Hevy + `hevy-mcp` | Hevy REST API, **Pro-gated** (05 master table) | Fast, best native app in the survey | Custom connector to a self-run `hevy-mcp` | Hevy account; social feed sharing | Pro required. Price UNVERIFIED, circulating figure ~$3/mo (01 §fitness-specific) | ~3 | High | Good |

**Why Hevy loses despite being the best app.** Every friend needs a paid
subscription, which contradicts the replication requirement outright (05 open q 4,
which reaches the same verdict).

**Why the low step counts do not win.** GitHub Issues is 3 steps and wger is 4,
but both put a paid Claude plan or a public HTTPS server between the friend and
their first logged set. Notion's 5 steps are 5 taps in two apps.

---

## Proposed architecture

### Components

```
  phone                     agent                       store
  -----                     -----                       -----
  Claude mobile app  --->  Claude + skills       --->  Notion workspace
  (typing "185x5")         (trainer-core, ...)         one duplicated page
                                |                        |
                                |                        +-- Log (databases)
                                +-- reads catalog,       +-- Config (pages)
                                    programs, config     +-- Programs (pages)
                                    from the same page   +-- Exercises (database)
```

One artifact. One Notion page tree, duplicated by a friend in one click. There is
no server, no repo, no Docker, and no code to deploy.

### Where each thing lives

| Thing | Where | Why |
|---|---|---|
| Set log | Notion database, one row per set | Matches every surveyed export's grain (05 "Verified CSV shapes": Hevy and Strong are both one row per set) |
| Sessions | Notion database, one page per session | 04 §7.3 |
| Exercise catalog | Notion database, seeded from free-exercise-db | 876 exercises, Unlicense, public domain, no attribution burden (05 "Exercise database recommendation") |
| Programs | Notion pages, plain text bodies in the line grammar from 04 §1.2 | A program is read whole, never filtered. Properties would buy nothing |
| Config (`athlete`, `limits`, `preferences`) | Notion pages, plain text bodies | 06 "What must be user-editable config" requires hand-editable files. A page body is hand-editable; a property grid is not |
| Trainer skills | Notion child pages under one Trainer page | Keeps replication to a single duplicate. Costs the agent a page read at session open. Alternative, faster but two artifacts: a Claude Project with the skills attached |
| Open-session cursor | Property on the open session page | 04 §7.3: deriving the cursor costs a Notion round trip every turn; accept the duplication and repair on session open |

**The one call I am least sure about** is putting the skills in Notion. It makes
replication a single click, which is the requirement, but it means the agent reads
its own instructions over the network at every session start. If that turns out
slow, move the skills into a shared Claude Project and accept two replication
artifacts.

### Daily flow

```
User:  what do i have today
Agent: Day B (Lower) - 5 exercises, ~40 min.
       Squat 3x5 @ 185. Last time: 180 x5,5,5.
       Warm-up: bar x5, 95x5, 135x3, 165x2.
```

Three lines, then stop (04 §4.1). The rest of the day is available on `list it`.
Ten lines of plan is ten decisions, and the neurodivergent self-tracking work
reports participants stuck on a single question for an hour (04 §4.1, citing
Chasing Shadows, arXiv).

Then as-you-go. The agent states one target, takes the result in any granularity,
confirms in one line, states the next target (04 §5.1). The user can answer with a
single character (`5`), a whole exercise (`135 5/5/4`), or a whole day
(`as planned`). Parsing rules are 04 §2.4 rules A to J, unchanged.

Close on `done for today`. The cursor advances, unlogged exercises are recorded as
`not done` with no commentary (04 §3), and the session gets one commit-equivalent
write.

**Write batching.** Do not call the Notion API per set. Buffer within an exercise
and write on exercise completion or on a 60-second idle. Notion's limit is about
3 requests per second per connection with a per-workspace limit that scales with
plan and is unpublished (01 §1). Batching also keeps the mid-set confirm line fast,
which is the whole five-second budget.

**Idempotency.** Every incoming user message gets a stable id and every write
records the id that produced it (04 §7.4). A re-sent `5` after a signal drop is a
no-op, not a duplicate set. In Notion this is the `client_key` property described
in 04 §7.3: query before create, update if it exists.

### Skill list for the first release

06 says ship five. I am shipping six.

| Skill | Why it is in release 1 |
|---|---|
| `trainer-core` | Scope, disclaimers, config load. Everything else sits on it (06 §1) |
| `intake` | Nothing can run without `config/athlete.md` (06 §2) |
| `program-design` | Selects from the library, never invents (06 §3) |
| `session-runner` | The daily loop (06 §5) |
| `load-adjust` | The raise-or-hold decision (06 §7) |
| **`pain-triage`** | **06's own layering rule says it "cannot be skipped" and "pre-empts everything" (06 "Layering"). Shipping the other five without it contradicts that. This is a correction to 06's TL;DR, not a preference** |

Deferred to release 2: `warmup` folds into `session-runner` as a plate-math
routine for release 1, because it makes no decisions. Then `substitute-exercise`,
`re-entry`, `deload`, `weekly-review`, `plateau-review`, `adherence`,
`technique-cues`, `lifestyle-prompts`.

### Progression default, re-anchored on ACSM 2026

03's engine stands: **double progression in a rep range, capped by effort, with
failure-triggered deloads** (03 TL;DR). ACSM's 2026 stand changes the dose targets
around it, not the session-to-session rule.

| Setting | Value | Source |
|---|---|---|
| Rep range and load step per exercise | e.g. 6-10 reps, 2.5 kg barbell step | 03 TL;DR rule 1 |
| Increase | all prescribed sets hit top of range, then +1 step, drop to bottom | 03 TL;DR rule 2 |
| Effort cap | leave 1 to 2 reps in reserve. Do not train to momentary failure by default | ACSM 2026 (via 06 §3.6): failure is "not strictly necessary". Replaces 03's RPE 9.5 grinder cap as the default |
| Hold | any set below top of range, add 1 rep to the weakest set next time | 03 TL;DR rule 3 |
| Decrease | miss bottom of range 2 sessions running, or 3 of 4, then -10% | 03 TL;DR rule 5 |
| Deload | autoregulated triggers first, 8-week calendar backstop. Volume -30 to -50%, load -10 to -20%, 5 to 7 days | 03 "Deload", Bell et al. Delphi consensus |
| Step-size guard | if one step exceeds ~5% of the working weight, add reps instead | 03 "Increment sizing", tagged **DERIVED** in that note |
| Frequency floor | every major muscle group at least twice a week. **Hard check, not advice** | ACSM 2026 (via 06 §3.2), which calls this more important than a perfect plan |
| Hypertrophy volume target | about 10 working sets per muscle per week | ACSM 2026 and Schoenfeld 2017 (03 §8, 06 §3.5) |
| Strength work | about 80% 1RM, 2 to 3 sets | ACSM 2026 (via 06 §3.4) |
| Power work | 30 to 70% 1RM, fast concentric | ACSM 2026 (via 06 §3.4) |
| Periodization | none in release 1 | ACSM 2026: complex periodization "not strictly necessary" (06 §3.6) |
| RPE gate | training age under 1 year, RPE is logged but never read by a rule | 03 rule 20, Zourdos 2016: novices systematically under-rate maximal sets |

---

## Data-model deltas (changes note 02 needs)

Thirteen changes. The first three come from the conflicts the brief named.

1. **Brzycki sign.** 02 §9 prints `1RM = load / (1.0278 - 0.0278 x reps)` in the
   table and then flags that the cited paper printed the plus form. Settled: the
   minus form is correct for estimating 1RM. Remove the flag, keep the guard rails
   (do not compute above 10 reps; do not compute from a set that was not near
   failure).
2. **Progression unit.** Add `progression_unit: session | week | block` to the
   program. 02 keys progression configs off wger's `iteration`, which counts passes
   through the program, not weeks. Madcow and the Texas Method progress **per week**
   (03 §10, which flags this for slice A explicitly). Also derive `week_index` on
   each session from the session's local date, using the local-date field 02 §8
   already specifies, so a late-night session lands in the right week.
3. **Rule reference gets three slots, not one.** 02 §6 carries a single
   `progression_rule` plus a `deload_rule`. 06's open question 8 asks whether 03's
   rule format covers deload and re-entry. It covers the per-session progression
   step and the decrease branch as executable rules; the deload and re-entry
   branches exist only as prose triggers in 03's decision table (rows 2 to 4 and 7
   to 11). Model them as three named slots: `progress`, `deload`, `reentry`.
4. **Per-exercise progression state.** 02 §6 says "rule ref plus per-exercise
   state" without enumerating it. It needs: consecutive-fail counter, current
   training max plus its history (03 §5), stage index for tier ladders (03 §6),
   variation index for bodyweight chains (03 §11), and last-deload date.
5. **One difficulty axis.** 03 §11 asks slice A directly for this: treat
   "variation index" and "load" as the same abstract difficulty axis, so one engine
   covers barbell progression and bodyweight progression. Add `variation_chain`
   (ordered list) and `variation_index` to the catalog entry.
6. **Plate inventory moves to a Location.** 02 §5 hangs `equipment_profiles` and
   `min_increment` off the catalog entry, but 02's own open question 5 notes that
   plate inventory is per-location. Home and commercial gyms have different smallest
   jumps, and the whole `jump_pct` guard (03 "Increment sizing") depends on knowing
   which. Add a `Location` entity; the catalog holds defaults, the location overrides.
7. **Athlete entity.** 02 has no athlete or profile entity at all. 03 rule 20 gates
   RPE on `user.training_age` and 06 requires `config/athlete.md`, `config/limits.md`,
   `config/preferences.md`. Add them.
8. **Pain flag gets a lifecycle.** 02 §2 has a per-set `pain_flag` of
   `none | niggle | stop`. 06 §9 needs a persistent record with a status of
   `open | resolved | cleared by clinician` that blocks programming for that
   movement while open. A `stop` on a set must create or link a Limits entry.
9. **Idempotency key on every set.** Add `source_message_id`. 02 has no such field;
   04 §7.4 makes it mandatory for a phone that loses signal and retries.
10. **Readiness collapses to one number, and rule 5 changes with it.** 02 §4 already
    recommends one 1-to-5 integer over four fields. Accept. The cost: 03's decision
    table row 5 fires on "3+ consecutive nights poor sleep", which one per-session
    number cannot express. Restate the rule as "3 consecutive sessions with
    readiness <= 2". **This is a deviation from 03's sourced rule** (the sleep
    literature is about consecutive nights, not sessions) and should be labelled as
    such wherever it ships.
11. **Cut `tempo` and `band` from release 1.** Both are tagged UNVERIFIED in 02 §2
    and §3 with no surveyed prior art. Keep `machine_setting`, which earns its place
    because carry-forward makes it free to record and it makes the stimulus
    reproducible.
12. **Session key is an opaque id.** 02 §8 warns against copying wger's
    `unique_together = ('date', 'user', 'routine')`. Confirmed: two-a-days must be
    legal, and 04 §1.4 allows "did day 2 twice" as a first-class case.
13. **`is_amrap` and `to_failure` as independent booleans** beside the `set_type`
    enum, per 02 §2's own recommendation. With one change: under the ACSM 2026
    default, `to_failure` is a thing the log records, not a thing a program
    prescribes.

---

## Conflict resolutions

**(a) Brzycki sign.** 02 §9 cites Thompson et al. printing `1.0278 + 0.0278 x reps`,
which is the inverse (nRM from 1RM) direction. Standard for estimating 1RM is
`load / (1.0278 - 0.0278 x reps)`. Use the minus form. 02's own flag was correct
and can now be closed.

**(b) Per-week progression.** 03 §10 found Madcow and the Texas Method progress per
week, and flagged that a session-to-session engine cannot express them. 02's model
carries wger's `iteration`, which is not a week. Add `progression_unit` to the
program and derive `week_index` per session (delta 2 above).

**(c) 03 predates the ACSM 2026 stand.** What changes: training to momentary failure
stops being a default, so the effort cap becomes "leave 1 to 2 in reserve" rather
than 03's RPE 9.5 grinder threshold; complex periodization is out of release 1; the
twice-a-week-per-muscle frequency floor becomes a hard check in `program-design` and
`weekly-review`. What does not change: 03's raise, hold, decrease and deload logic.
ACSM sets dose targets, not session-to-session rules.

**(d) Config location, and 03's rule coverage.** Config lives as **page bodies, not
Notion properties**, because 06 requires the user be able to open and edit it and a
property grid is not a text file. Log data lives as properties, because it gets
filtered. On rule coverage: 03 covers progress and decrease as executable rules;
deload and re-entry are prose triggers, so give the rule reference three slots
(delta 3 above).

**(e) Units and partial sessions.** Default to **lb**, on two grounds: 04 §2.4's
Rule A thresholds are written lb-first, and 02 §11's sample session file uses
`America/Chicago`. That is a sample file, so this is a weak signal and a one-word
flip. Partial session: **advance the cursor on explicit close, not on the first
set** (04's own proposal in §1.4 and open question 2). Auto-close at the next day's
first interaction also advances, per 04 §5.3.

**(f) wger + official MCP versus Notion.** wger wins on schema and on having the
only official MCP server for a self-hostable FLOSS backend (05 TL;DR). It loses the
user's loop: the agent reaches it through a claude.ai custom connector, which needs
a public HTTPS MCP endpoint and a paid-for server, and Claude Free allows one custom
connector (01 §4). Its API auth model is **UNVERIFIED** (01 table); 05 confirms only
that the read API needs no auth key. Verdict: crib the schema, which 02 and 05 both
already recommend, and do not run the stack. Revisit if Notion's unpublished
per-workspace rate limit bites, or if the 3000-plus set rows a year make analytics
painful (02 §11).

**(g) Phone path per option.** Notion: Claude mobile app plus the Notion connector,
free for all Claude users (01 phone-trigger rank 1). Git: Claude Code on the web,
which needs Pro, Max or Team (rank 2), or a GitHub mobile hand-edit that fires a
push-triggered Action (rank 3, free within 2,000 Action minutes a month). wger and
Sheets: a custom connector to your own MCP endpoint, one allowed on Claude Free.
That difference is why the runner-up is the runner-up.

---

## Friend replicates it

Five steps. No command line. $0.

1. Sign up for a free Notion account at notion.com.
2. Open the shared Workout Log template page and click Duplicate. This brings across
   the Sets and Sessions databases, the exercise catalog, the program library, the
   config pages, and the trainer skill pages in one action.
3. In the Claude mobile or web app, open connector settings and connect Notion.
   OAuth, no keys to copy (01 "Friend replicates it", option 1 step 3).
4. Grant the connector access to the duplicated page.
5. Say "set me up" to Claude. `intake` runs, asks the goal, training age, schedule,
   equipment, and the PAR-Q+ screening questions, then writes `athlete` and `limits`
   (06 §2).

Optional, later:
6. Publish the log page to share with a coach. Unlimited published pages on Free
   (01 §1).
7. For anything unattended, create an internal integration in Settings, Connections
   and copy the token. Notion MCP requires an interactive OAuth flow and does not
   support non-interactive authorization, so cron jobs need the REST API and a token
   (01 §2).

01 quoted 4 steps for Notion. This is 5 because intake is real work and skipping it
leaves the agent with no config to read.

---

## Open questions, with defaults

Deduplicated across notes 01 to 06. 47 questions in the source notes collapse to 31.

**Two of these cannot be safely defaulted** (training age and injuries). Both have a
conservative fallback so silence is still an answer, but both are worth 30 seconds.

### Store and stack

| # | Question | Proposed default | From |
|---|---|---|---|
| 1 | Notion or git? | Notion Free | 02 q8, 04 q6, 05 q1 |
| 2 | Do you have or want a paid Claude plan? | Assume no. That is why Notion wins | 01 q7 |
| 3 | What does "shared with others" mean? | A published read-only page. No editors, no guests | 01 q2 |
| 4 | Does the agent need to run unattended? | No. It runs only when you talk to it | 01 q3 |
| 5 | Does the "Jim" app come back? | No. If it does, it reads the Notion API | 01 q5 |
| 6 | How much does lock-in bother you? | Accept Notion. Monthly CSV export as insurance | 01 q6 |
| 7 | Emit an interchange format? | No exporter in release 1. Hevy's CSV column set is the target if ever | 05 q2 |
| 8 | Import existing history? | No. Start fresh | 02 q9 |
| 9 | Liftoscript: reimplement or vendor? | Write our own grammar (04 §1.2). Do not vendor Liftosaur's library | 05 q3 |
| 10 | Apple Health / Health Connect integration? | Skip. Both model sessions, not sets (05 "Is there a standard format") | 05 q6 |

### Training

| # | Question | Proposed default | From |
|---|---|---|---|
| 11 | Units | **lb** | 02 q1, 04 q1, 06 q6 |
| 12 | **Training age** | **Cannot default safely.** Fallback if silent: treat as under 1 year, which disables every RPE-gated rule. Conservative, and wrong for you if you are past that | 03 q1, 06 q2 |
| 13 | Primary goal | General strength and size. Double progression | 03 q2, 06 q1 |
| 14 | Days per week, minutes per session | 3 days, 45 minutes. The honest number, not the aspirational one (06 §2.3) | 06 q3 |
| 15 | Equipment, plate pairs, dumbbell jump | Commercial gym, 2.5 lb smallest pair, 5 lb dumbbell jump. Re-ask on the first stall | 02 q5, 03 q4, 03 q5, 06 q4 |
| 16 | **Injuries and PAR-Q+** | **Cannot default safely.** Fallback if silent: program conservatively and record the refusal (06 §2 guardrails) | 06 q5 |
| 17 | RPE or RIR: which do you say, and on or off? | Off. Accepted if typed, never prompted. Inert anyway while training age is under 1 year | 02 q2, 03 q3, 04 q4 |
| 18 | Deload preference | Autoregulated triggers, 8-week calendar backstop | 03 q6 |
| 19 | Auto-apply decisions or suggest them? | Apply, state it in the confirm line, `undo` reverses it | 03 q7 |
| 20 | May the agent raise sleep and food? | One prompt after a visibly bad session, then drop it | 06 q7 |

### Logging UX

| # | Question | Proposed default | From |
|---|---|---|---|
| 21 | Does a partial session advance rotation? | Advance on explicit close only | 04 q2 |
| 22 | Rest days in the cycle? | No. "Next up is Lower, whenever you want it" | 04 q3 |
| 23 | Streaks? | None. A streak turns a missed session into a loss | 04 q5 |
| 24 | Voice input: real or hypothetical? | Assume real. Accept `by`, `at`, and spelled numbers as first-class | 04 q7 |
| 25 | Volunteer PR hints? | Only when today's top set is within one increment of a rep-max PR | 04 q8 |
| 26 | The `20x8` grey band | **Guess weight, rely on `undo`.** This overrides 04's proposal to ask once per exercise, because 04 §3's carry-forward rule makes last session's weight the guess and says the agent can guess aggressively when a wrong guess is one word to reverse. Flagging the disagreement rather than hiding it | 04 q9 |
| 27 | Auto-log rest from timestamps? | Compute it, never show it unless asked | 02 q7 |
| 28 | Readiness block | One 1-to-5 number, offered at session open, skippable. See data-model delta 10 for what this costs | 02 q3 |
| 29 | Per-side reps on every row? | Off. Record `side` only when you say it | 02 q4 |
| 30 | Two-a-days? | Allowed. Session key is an opaque id, not (date, program) | 02 q6 |
| 31 | Where do the trainer skills live? | Notion child pages, so replication is one click. Move to a Claude Project if the page read at session open feels slow | 06 q8, first half |

---

## What is still unverified

Carried forward unchanged from the source notes. None of these are softened.

- Notion's per-workspace API rate limit scales with plan, and the numbers are
  unpublished (01 §1).
- The `workspace_search` versus `ai_search` distinction is inferred from tool
  output, not from any Notion doc (01 §2).
- wger's API auth model: blocked by bot protection on wger.de (01 gaps).
- Hevy Pro's price: pricing page is a JS shell, help article returns 403 (01 gaps).
- Strong's CSV header was read from a real export in a public repo, not from Strong's
  own docs (02 §10, 05 gap 3).
- Hevy's schema came from a third-party OpenAPI mirror; Hevy's own docs endpoint
  served the petstore sample (02 §10).
- The 0.5 fractional weighting for secondary-muscle volume is a convention with no
  cited source (02 §9).
- The 5% `jump_pct` threshold, the "-5% per RPE point over target" heuristic, the
  time-off resumption percentages, and the statistical plateau definition are all
  tagged **DERIVED** or **UNVERIFIED** in 03 and must not ship as evidence-based.
- The set-entry grammar's slash notation (Rule C), the `#` suffix for lb (Rule I),
  and all of the voice-input handling (04 §5.4) are design inferences with no
  first-party precedent.
- Most of 06's safety and behaviour-change citations are search-snippet-only,
  including the ACSM 2009 stand's numbers, the movement-pattern taxonomy, the FDA
  general-wellness guidance, and every ADHD-adherence claim. The ACSM **2026**
  numbers are the verified ones.
