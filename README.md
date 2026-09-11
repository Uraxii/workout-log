# workout-trainer

In plain words: a personal trainer for Claude Code, written as eight skills and nothing else.
One coach wears seven hats, the same seven people a professional athlete would have.
The agent brings the judgment. The skills bring your standards and this person's facts.

## Install

```
/plugin marketplace add Uraxii/workout-log
/plugin install workout-trainer@uraxii-plugins
```

Then say what you want to train for. The `trainer` skill picks the hat.

## The hats

- `trainer`. The router. Which hat is on and when it changes.
- `head-coach`. What the training is for, and the intake interview.
- `strength-coach`. The program, and running a session.
- `sport-scientist`. Testing, logging, and what the numbers mean.
- `medical-screening`. Whether they should be training at all.
- `pain-and-injury`. Something hurts.
- `nutrition`. Food, as far as a coach's job goes.
- `mental-skills`. Keeping them turning up.

## Working on it

```
claude --plugin-dir .
```

Read `CLAUDE.md` before editing a skill. There is no code here on purpose, and it says why.
