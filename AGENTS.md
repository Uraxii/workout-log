# AGENTS.md

workout-log is a Notion-backed strength trainer: a logging grammar, a
progression engine, and seven Claude Agent Skills that turn a chat message
into Notion database writes.

## The seven skills

`.claude/skills/` holds `trainer-core`, `intake`, `screen`, `program-design`,
`session-runner`, `load-adjust`, and `pain-triage`. Each folder is a
self-contained `SKILL.md` per the Agent Skills spec (agentskills.io). Codex
reads the same folders through `.agents/skills/`. GitHub Copilot reads
`.github/copilot-instructions.md`. See docs/build-plan.md s8 for the full
layout.

## The write verbs and the read verbs

`config-write(page, key, value)` and `row-create(db, payload)` are the two
write verbs a coaching skill may call (docs/build-plan.md s6).
`database-create(db, payload)` is the third write verb, and `intake` alone
calls it, once per database, to build the two the schema declares, `Sets` and
`Sessions` (docs/build-plan.md s5.1). No skill writes to Notion, or to a
fixture, through any other route.

Notion holds logs only. Anything that is not a log is either a config page
(the athlete's own settings, her limits, her current program) or package
reference data the agent reads and never writes: `exercises/defaults.json`
and `library/*.json` are the whole of it. Nothing seeds a catalog into her
workspace, and no database points at another, so every stored value is a
string, number, date, select or checkbox.

Reads are not writes, so the rule above does not cover them. There are two read
verbs, `config-read(page)` and `row-query(db, where)`, both in
`tools/mock-notion/reader.py`. Each skill rebuilds its turn-1 state through
them. For the contract, see "Mock reader contract" in docs/architecture.md.

## No user data

Do not commit training logs, health answers, or personal identifiers to this
repo. `make check` greps the packaging surface for that pattern; keep it
clean.

## Run the proofs

	make skills   # generate .agents/skills symlinks and dist/*.zip
	make check    # run every offline proof and validator, exit 0 on pass

Both targets glob `.claude/skills/*`, so they work with any subset of the
seven skills already written. Details: docs/build-plan.md s9.
