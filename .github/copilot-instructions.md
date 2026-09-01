# Copilot instructions

workout-log is a Notion-backed strength trainer built from Claude Agent
Skills. Copilot reads skills from `.claude/skills/`, the same folders Claude
Code and Codex use. See AGENTS.md for the full picture.

## The one write path

Call only `config-write(page, key, value)` or `row-create(db, payload)` to
write data (docs/build-plan.md s6). No other write route.

## Before proposing a change

Run the offline proofs:

	make skills
	make check

Both glob the existing skill directories, so they run against whatever
subset of the seven skills (`trainer-core`, `intake`, `screen`,
`program-design`, `session-runner`, `load-adjust`, `pain-triage`) exists.

## No user data

Never write training logs, health answers, or personal identifiers into this
repo.
