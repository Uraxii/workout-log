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

## The one write path

`config-write(page, key, value)` and `row-create(db, payload)` are the only
two write verbs a skill may call (docs/build-plan.md s6). No skill writes to
Notion, or to a fixture, through any other route.

## No user data

Do not commit training logs, health answers, or personal identifiers to this
repo. `make check` greps the packaging surface for that pattern; keep it
clean.

## Run the proofs

	make skills   # generate .agents/skills symlinks and dist/*.zip
	make check    # run every offline proof and validator, exit 0 on pass

Both targets glob `.claude/skills/*`, so they work with any subset of the
seven skills already written. Details: docs/build-plan.md s9.
