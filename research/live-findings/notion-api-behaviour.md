# Live Notion test — findings

In plain words: this is the first time any workout-log skill has touched a
real Notion workspace instead of the offline fake. I played an athlete by
hand (intake, program-design, session-runner) against a real scratch page,
and wrote down every place the real Notion API answered differently from
what `tools/mock-notion/` assumes. All names, health answers, and numbers
below are invented for this test. No real person's data appears anywhere in
this file or in the Notion pages it created.

Branch `master`, HEAD `9dc5ed8`, tree clean before and after
(`make check` passed both times, 26/26 fixtures, exit 0).

Scratch workspace used, nothing else touched:
`https://app.notion.com/p/3d378d6f98b681a68296ebef3958cca9`

## Status: complete

Every stage in ACCEPTANCE ran and was verified against the real API: two
databases created from the schema's own DDL, a full intake (profile +
7 PAR-Q+ questions), a program designed and written to a real page, 6 sets
logged across 2 exercises, a session closed, and all 5 named findings
either confirmed or refuted with real evidence. `load-adjust` was also
exercised live, beyond what ACCEPTANCE required, because it sits directly
on top of finding 4.

## Does the loop work end to end against real Notion?

Mostly, but only because I stood in for parts the docs assume the
Notion API does automatically and it does not. Database creation, intake's
config writes, program-design's picks, and session-runner's set logging
all produced correct data once translated into real API calls by hand.
Three of those translations are not obvious and are not written down
anywhere in the repo today (see "New, only found live" below). A model
following the skills literally, with no one telling it to fenced-code-block
its JSON or to swap in the real session page id, would corrupt data
silently on the first real run.

## What worked end to end

- `intake/scripts/ddl.py`'s renderer produces exactly the SQL DDL the real
  `notion-create-database` tool wants. Both `Sets` (31 properties) and
  `Sessions` (15 properties) were created in one call each, synchronously
  (no `async_task` came back either time), and a `notion-fetch` on both
  data sources afterward showed every property name, type, select enum, and
  the `e1RM` formula matching `schema/notion-schema.json` exactly.
- A full intake ran, 23 questions plus 7 PAR-Q+ items, driven turn-by-turn
  through the real `intake_turn(line, state)` seam with invented answers,
  ending "All set." with `intake_cursor` at 23 and `clearance: cleared`.
- `program-design` picked PHUL (not GZCLP, not nsuns-lp) for a 4-day
  general-strength profile, wrote `program/current` and
  `agent/progression-state`, and both were fetched back byte-for-byte
  correct once the JSON body was placed in a fenced code block instead of
  plain bullet text (see delta below).
- `session-runner` opened a session, logged 3 sets of "185x5" on bench and
  3 of "145x5" on squat, and closed it. All 6 rows were queried back via
  `notion-query-data-sources` (SQL mode) and every `Load`, `Reps`,
  `Set index`, and `Session` value matched what was said.

## Real-API-vs-mock deltas, with exact evidence

1. **`notion-create-database` takes SQL DDL text, not a properties object.**
   The mock's `writer.py.database_create` and `notion_ddl.py` model the
   payload as `{"parent": ..., "schema": ...}` where `schema` is already a
   DDL string, so this one matches — but only because `intake/scripts/ddl.py`
   already renders DDL. Nothing else in the repo could have produced a
   working payload; a hand-built REST-style properties object (the shape
   `references/db-create.md` explicitly warns against) would have been
   rejected outright.

2. **Config pages have no real Notion primitive.** `AGENTS.md` and
   `docs/build-plan.md` s1 say config is "page bodies", but the real
   `notion-update-page` tool only allows a page-level `properties.title`
   for a page outside a database — every other key-value has to live in the
   page's Markdown *content*, not a property. I represented each
   `config/*` page as a bulleted `` `key`: value `` list and each
   `config_write(page, key, value)` as either a full page create (turn 1)
   or a `notion-update-page` `update_content` search/replace pointed at the
   old value. That mapping is not in any doc; a different implementer would
   invent a different one, and nothing enforces one Notion representation.

3. **`update_content`'s search/replace needs the exact old value, which the
   mock never tracks as a round-trippable string.** I updated
   `config/athlete`'s `intake_cursor` from `22` to `23` with
   `content_updates: [{old_str: "- \`intake_cursor\`: 22", new_str: "..."}]`
   — it worked, but only because I still had the prior value in my own
   Python state. A caller that lost track of what it last wrote (a fresh
   chat, a dropped turn) cannot safely call `update_content`: `old_str` has
   to match exactly once or the call errors, and nothing about
   `config-write`'s contract says the caller must remember its own
   history to make an idempotent-looking write actually idempotent.

4. **Markdown round-tripping corrupts stored JSON, depending which read
   tool you use.** `config/athlete.notion_data_sources` is a JSON string
   containing `{` and `}`. Written verbatim, `notion-fetch` reads it back
   as:

       "notion_data_sources": \{"Sessions": "467c5a15-...", "Sets": "2ae01f48-..."\}

   with backslashes in front of both braces — `json.loads` on that fetched
   text fails immediately. The same corruption hits `write_key` and
   `Session`, which contain `:` and `|`: fetched or rows-mode text for
   `write_key` came back as
   `2026-09-06T09:15\:00-06\:00\|America/Denver\|...` (colons and the pipe
   all backslash-escaped). This breaks rule L9 idempotency directly:
   `write_key` is the `Sets` identity key, and a caller that reads it back
   through `notion-fetch` or rows-mode to check "does this key already
   exist" will never find a match against the literal value it is about to
   write. Plain `notion-query-data-sources` SQL mode is the only path
   that returned the unescaped literal. Wrapping the JSON body in a
   fenced ` ```json ` code block (rather than inline bullet text) avoided
   the corruption for `program/current.body` and
   `agent/progression-state.progression` — confirmed by fetching both back
   afterward and diffing byte-for-byte against what was sent. **Lesson: any
   JSON payload written to a config page must go in a fenced code block,
   and any identity/dedup key must be read back through SQL mode, never
   `fetch` or rows mode.**

5. **`Sessions.Title` is never written by any script, so every real Sessions
   row is untitled.** Nothing in `session_open.py`, `log_set.py`, or
   anywhere else sets the `Title` property the schema declares as the
   database's title column. The real create call
   (`notion-create-pages` with no title property) succeeded and returned
   `"Title": ""`. In the real Notion UI this database is unbrowsable by
   name: every row shows blank where its name would be.

6. **`log_set.py`'s `session_id` is a synthetic placeholder, not the real
   Notion page id the schema says `Sets.Session` should hold.**
   `session_open.py` invents `f"sessions-{session_seq}"` (e.g.
   `"sessions-1"`) as soon as a session opens, before any real Notion
   create has run, because the pure seam cannot know a real id in advance.
   The schema comment for `Session` says the field holds "the session page
   id the create call returned, as text" — but the seam's own output
   literally contains the string `"sessions-1"`. Nothing in any skill's
   docs tells the calling agent it must substitute the real returned
   Notion page id (`3d378d6f-98b6-810b-b689-cd34e1db71f0` in this run) for
   that placeholder before writing the `Sets` rows. I did the substitution
   by hand; a literal reading of the skill would write the fake string
   `"sessions-1"` into a real `Sets.Session` column, breaking any lookup
   that expects a real page id there.

7. **The `e1RM` formula is unreachable through the query surface most
   read verbs would use.** The formula computes fine (Notion accepted the
   DDL and shows `type: formula` on the property), but:
   - `notion-query-data-sources` SQL mode lists `e1RM` under
     `notAvailableInQuerySql` and omits it from every query.
   - `notion-fetch` and rows-mode both return an opaque reference instead
     of a number: `"e1RM": "formulaResult://2ae01f48-.../3d378d6f-.../SmRFPg"`.

   There is no read call in the MCP surface I found that returns e1RM as a
   usable number. `read_layer.e1rm` in the mock computes it in Python
   instead of reading the Notion formula, so this gap is invisible offline;
   against real Notion, the schema comment's claim that the Notion formula
   and `read_layer.e1rm` are "one answer" (`schema/notion-schema.json`,
   `Sets.e1RM` note) cannot currently be verified through any read call.

8. **`now` defaults to `""` in more than one place, and every fixture
   papers over it by always setting `@now`.** Finding 5 below is the
   `screen`/`clearance.py` instance; the same pattern exists in
   `program-design/scripts/design.py:_started_at` (`state.get("now", "")`)
   — I hit this by omitting `now` from a state dict once by accident and
   got `program/current.started_at = ""` with no error. Nothing in the
   architecture docs flags `now` as a value the calling agent must always
   supply; it is silently optional everywhere it is read.

## The 5 prior findings: confirmed or refuted

1. **CONFIRMED.** `starting_loads.resolve()` against the real `nsuns-lp`
   template raises `KeyError: 'exercise'` exactly as predicted, live:

       Traceback (most recent call last):
         File ".../starting_loads.py", line 40, in resolve
           baseline = on_file.get(block["exercise"])
                                  ~~~~~^^^^^^^^^^^^
       KeyError: 'exercise'

   `library/nsuns-lp.json`'s `start`-bearing blocks carry `sequence`, never
   `exercise`. This crashes the whole `design_turn` with an uncaught
   exception the instant nsuns-lp is picked for an athlete with any
   baseline on file — not a wrong answer, a hard stop with no writes and no
   confirm line.

2. **CONFIRMED.** Feeding the exact brief text, `"squat 185x5, bench 135x5,
   deadlift 225x5"`, to `baselines.parse()` returns
   `"Barbell Deadlift": (135.0, 5)` — bench's number, not deadlift's
   225x5 — because the nearest-`NxR`-by-string-position heuristic picks
   whichever number sits closest in the sentence, not the one after the
   matching lift name. This propagated into the real program-design run:
   PHUL's Deadlift block started at **105 lb**, computed from the wrong
   135x5 pairing, instead of a load derived from 225x5. A real athlete
   would be handed a deadlift working weight roughly half of what their
   stated baseline supports.

3. **CONFIRMED.** The real `program/current` write from that same run
   stored `"next_target": "105 lb"` — a string carrying its unit, as
   `program_page.py` writes it — inside `agent/progression-state`, which
   `rules.py`'s `bumped_value()`/`deload_target()` immediately treat as a
   number (`cfg["current"] + delta`). No arithmetic ran in this test
   because finding 4 blocked it first (see below), but the stored value
   itself, fetched back from the real page, is provably a string:
   `{"next_target": "105 lb", "training_max": 135.0}` — one field typed as
   a Python `str`, the sibling field typed as a `float`, in the same
   dict, on the same real Notion page.

4. **CONFIRMED, live.** Built `state` exactly as `hydrate.py` would
   (`state["progression"]` populated from the real
   `agent/progression-state` page fetched above) and called
   `adjust_turn("Barbell Bench Press - Medium Grip\t185x5x3", state)` with
   no prior `setup` line. Bench had just been logged at 185x5 for 3 sets
   against a stored target of 105 lb / training max 135 — a clear bump
   case. Result:

       SAY: Noted.
       WRITES: []

   `state["rules_by_exercise"]` was `{}` throughout: `load_adjust.py` only
   ever reads that key, and nothing populates it from `state["progression"]`
   anywhere in the codebase (confirmed by grep across every script in
   `load-adjust/scripts/` and `tools/mock-notion/hydrate.py`). Worth
   noting: `load_adjust.py`'s own module docstring already says "No
   upstream skill in this build writes a per-exercise progression rule
   into `state` yet" — so this is a documented gap, not a hidden
   regression, but the practical effect is exactly as described: right now
   nothing in production ever calls `load-adjust` with a hydrated
   progression rule, so no set is ever automatically bumped, held, or
   deloaded end to end.

5. **CONFIRMED.** `screen/scripts/clearance.py:72`'s `parq_date = now[:10]`
   with `state.get("now", "")` reproduced live: running the exact 7-NO
   PAR-Q+ pass through `intake_turn` with no `"now"` key in `state`
   produced `{'clearance': 'cleared', 'parq_date': ''}`. The main run (with
   `now` supplied) correctly wrote `parq_date: 2026-09-06`, confirming both
   the correct path and the failure mode side by side.

## New, only found live

- Config pages have no documented real-Notion shape (delta 2) — the single
  biggest gap, because every other config-write finding follows from it.
- `notion-fetch` and rows-mode both markdown-escape `:`, `|`, `{`, `}` in
  rich-text properties; SQL mode does not (delta 4). Whichever read verb
  `tools/mock-notion/reader.py`'s real counterpart ends up calling matters
  as much as what it reads.
- `Sessions.Title` is always blank in the real database (delta 5).
- `Sets.Session` needs a real-id substitution the docs never mention
  (delta 6).
- `e1RM` cannot be read back as a number through any query path tried
  (delta 7).
- `now` is silently optional in more than the one place `docs/limitations.md`
  might lead you to expect (delta 8).

## Ranked, what to fix first

1. **Write down one real Notion shape for config pages**, including how a
   single key gets updated without the caller memorizing prior content.
   Every other config-write finding here is downstream of this being
   undefined.
2. **Fix `baselines.parse()`'s pairing** (finding 2) before anyone runs
   program-design for real — it silently mis-prices a main lift, and a
   deadlift started at half its real working weight is a correctness bug
   with a direct safety angle (starting too heavy on the *next* correction
   is just as easy to get wrong the other way).
3. **Wire `hydrate.py`'s `state["progression"]` into whatever
   `load_adjust.py` actually reads**, or rename/document the gap loudly —
   right now the athlete-facing behavior is "log a great set, get told
   nothing, get no bump," silently, forever, in every real chat.
4. **Store `next_target` as a number plus a separate unit field** (finding
   3), and **thread the real Notion page id into `Sets.Session`** instead
   of the synthetic `sessions-N` placeholder (delta 6) — both are the kind
   of thing that works perfectly offline and corrupts data the first time
   a real Notion write happens.
5. Everything else (nsuns-lp's `KeyError`, `now` defaults, `e1RM`
   unreadability, blank `Sessions.Title`) before this ships to a second
   real user.

## Notion pages this test created (all under the scratch page, all
invented data)

- Sets database: `https://app.notion.com/p/31beffc3144a46f08a67c4cac2b102a4`
- Sessions database: `https://app.notion.com/p/cf7e119414f04c5086ad24c14400e21c`
- `config/athlete`: `https://app.notion.com/p/3d378d6f98b681fdb2bccb3547a64faf`
- `config/preferences`: `https://app.notion.com/p/3d378d6f98b68102bd61c4304539ed05`
- `config/limits`: `https://app.notion.com/p/3d378d6f98b68156a50ae9d665a7db4f`
- `program/current`: `https://app.notion.com/p/3d378d6f98b68158b904cf8b6f9f53e7`
- `agent/progression-state`: `https://app.notion.com/p/3d378d6f98b68131bbd6c9e933f92f31`
- One real Sessions row plus 6 real Sets rows, listed inline above.

## Deviations from the brief

- `program/current.body` was written as a truncated 2-block stand-in
  (Bench + Squat/Deadlift blocks only) rather than the full 5-block, 5
  634-byte PHUL template, to isolate the markdown-round-trip question
  (delta 4) from payload size in the limited number of real API calls this
  run budgeted. The full untruncated payload the real `design_turn`
  produced is on disk at
  `/tmp/claude-1000/-var-home-nicole-Projects-workout-log/67ac6b91-99ca-4697-9e3c-d8b0a1eee1fb/scratchpad/program_current_payload.json`
  for anyone who wants to replay the full write.
- Finding 5's broken-`now` case (empty `parq_date`) was reproduced by
  direct execution of the real `intake_turn` seam rather than written into
  the live Notion workspace, to avoid leaving a wrong record behind in the
  scratch page.
- I did not perform all ~25 individual `config_write` calls as separate
  real API round trips (one per intake question). I applied the merged
  final state in one `notion-create-pages` call per config page, then
  demonstrated one incremental `notion-update-page` `update_content` call
  to prove the single-key-write mechanism (delta 3) works. A faithful
  turn-by-turn run would be roughly 25 separate Notion API calls for
  intake alone; that chattiness, and whether it is acceptable, is itself
  worth a follow-up.
- pain-triage was not exercised (not required by ACCEPTANCE, and the
  brief's ordering put Notion-only scope on this run).
- The "obsidian vault" half of the user's ordering sentence is out of
  scope for this run; a different agent owns that per the brief.
