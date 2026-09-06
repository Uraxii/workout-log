# CLAUDE.md

In plain words: this repo is a personal trainer built as three Claude skills.
They are markdown instruction files and nothing else. An agent reads them and
supplies the coaching judgment itself.

## Why markdown and not code

The hard part of coaching is judgment, and Python can only hold rules, so every
attempt to write the trainer as code turned into a decision table that was wrong
for the person standing in front of it.
The agent already has the judgment.
What it does not have is this person's facts and your standards, and markdown
delivers exactly those and nothing else.
Code also has to be trusted, so it needs tests, but a test of coaching judgment
is a test of the model, which is how 4,700 lines ended up existing to satisfy a
suite that proved nothing.

The research is the exception, and it ships with the skills.
It is what the agent reads when a branch needs depth the skill does not carry,
so a skill cites `research/` by path instead of reproducing it.
That is why a skill can stay short without going shallow.

## What is here

Three skills, in this order:

- `intake`. Learn who you are coaching. Written.
- `create-program`. Write this person a program. Written.
- `log-workout`. Run and record a session. Written.

`research/` holds 26 documents and 19 source tables behind those skills. `.kb/`
is a 647-page knowledgebase, gitignored and irreplaceable. `exercises/` holds
the exercise catalog. Read the research before writing a skill. Do not re-run it.

## How these skills are written

Read `.claude/skills/intake/SKILL.md` first. It is the worked example. It took
four rewrites to get to 47 lines and the earlier drafts were 321.

**Shape**

- One `SKILL.md` per skill. A reference file only when the content genuinely
  cannot live inline.
- Sections are the things you need to find out, in the order you ask them.
  Reading down the page gives the order of operations.
- Bullets. Questions only.
- Prose under a question only when the intent is not obvious. Say why the answer
  matters or what to do with it. If a competent agent already knows, the prose is
  noise, so most questions carry none.
- The description lives in the frontmatter and appears exactly once. Never
  restate it as a section in the body.
- Open with one or two lines starting "In plain words:".
- One sentence per line for whatever prose survives.

**Substance**

- This is a skill for an agent, not an app being deployed. No age gates, no
  consent machinery, no compliance apparatus, no routing a person to an external
  service the agent could handle itself.
- Trust the agent. Do not encode procedure it already has.
- Do not reproduce a research document. The research is exhaustive on purpose.
  The skill is not.
- Cut any question that would not change what gets written.
- Ask what a real person can answer. "Any numbers you already know" got back
  "numbers? like my weight?". "Any lifts or times you remember" works. A named
  gym is a complete answer; an equipment inventory is not.

**Prose**

- No em dashes, and no hyphen standing in for one.
- Sentence case headings.
- Cut adverbs. "Actually" and "really" are almost always filler.
- Say it once.

## Never do these

Each one has a history in this repo. All of it is in git.

- No Python, no shell, no executable code inside a skill. Reference data may be
  `.json` and nothing else.
- No fixtures, no mock store, no replay harness, no test of agent judgment. The
  first version of this repo was 4,700 lines of Python built so a test could
  gate it. The tests became the reason the code existed, and all of it was
  deleted at `ad98b0f`.
- No library of pre-built programs for the agent to pick from. The agent writes
  the program.
- Never commit training logs, health answers, or personal identifiers.

## How to work on this

Skeleton first. Get it approved. Then fill one section at a time and stop after
each. Do not fan the work out to parallel agents; this is small and it is a
writing task, and every attempt to parallelize it has produced something that
had to be deleted.
