# workout-log

A Notion-backed strength trainer built from seven Claude Agent Skills. You talk
to an AI agent, it writes your sets into Notion databases it creates in your own
workspace. No server, no account with anyone, no app.

This is one person's tool, published so other people can run their own copy. It
is not a product and it is not medical advice.

## Who it is for

Someone who already trains, uses Notion or is willing to, and would rather type
`135x5` into a chat than tap through a logging app. You need either Claude Code
on a paid plan, or a free claude.ai account.

## Quick start

1. Create a free Notion account and one blank page.
2. Install the skills as a Claude Code plugin, or upload the ZIP to claude.ai.
3. Grant the Notion connection access to that page.
4. Say "set me up". `intake` creates the databases and asks the profile questions.
5. Say "make me a plan", then log sets by typing lines like `135x5`.

Both install paths, step by step:

	docs/install.md

## The seven skills

Each is a folder under `.claude/skills/` holding a `SKILL.md` and its scripts.

- `trainer-core` gates every turn: no set while the session is halted, no session without clearance and a program, and it says once that it is an AI.
- `intake` creates the four databases from the schema, seeds the exercise catalog, and asks every profile question with no silent defaults.
- `screen` asks the seven PAR-Q+ health questions verbatim and writes the clearance state.
- `program-design` picks a template from `library/`, writes it to `program/current`, and swaps one exercise when a new restriction rules it out.
- `session-runner` opens a session, parses each set line, advances the cursor, and closes the session.
- `load-adjust` applies the program's progression rule after a set, an exercise, or a session to bump, hold, or deload.
- `pain-triage` maps pain and injury words to niggle or stop, halts the session on stop, and opens a dated `config/limits` entry.

## What it stores in Notion

Four databases, `Sets`, `Sessions`, `Exercises`, and `Locations`, plus the
config pages `config/athlete`, `config/preferences`, `config/limits`,
`program/current`, and `program/history/<date>`. Property names, types, and
enums all come from one file:

	schema/notion-schema.json

## Limits

- Codex loads the coaching text through `.agents/skills/`, but has no documented Notion MCP wiring, so a Codex user cannot write a set in release 1. No phase tests Codex.
- Nothing here has run against a live Notion workspace. Every proof in the repo replays a fixture against an offline mock writer. Your first run is the first real test.
- Notion Free allows roughly 3 requests per second, so seeding the 913-row catalog takes about 5 minutes. It happens once.
- `screen` runs PAR-Q+ and `pain-triage` refers you to a professional. Neither is a diagnosis, and none of this is medical advice.

## Licence and credit

Code and skills are MIT (`.claude-plugin/plugin.json`).

The exercise catalog is 913 rows: 876 vendored from
[yuhonas/free-exercise-db](https://github.com/yuhonas/free-exercise-db) under
the Unlicense, plus 24 written for this project. See `exercises/README.md`.

The ten program templates carry structure only, written in our own words from
freely published sources and credited by name in `library/README.md`. GZCLP,
PHUL, nSuns 5/3/1 LP, Easy Strength, Couch to 5k, the Otago Exercise Programme,
and the r/Fitness, r/bodyweightfitness, and r/kettlebell wiki routines. No
program text is copied.

## Run the offline proofs

	make check

That builds the catalog, validates every program template, replays all fixtures
under `fixtures/` through `tools/mock-notion`, checks the skill frontmatter, and
fails if personal data reached the packaging surface. No Notion, no network.
