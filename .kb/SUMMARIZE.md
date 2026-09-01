# Summarize

This knowledge base backs a personal workout-logging system driven by an AI agent: a log the agent reads and writes, preset routines, progression rules (when to raise or lower weight), and a stack a friend can replicate.

One source here is a research note, a vendor doc, a pricing page, an app export schema, a program author's rules, or a paper. Summarize it as an abstract a builder can act on: what it decides or proves, the concrete numbers and field names it gives, and what it leaves open.

Frontmatter fields, all required:
- `title`: short, specific, names the tool, scheme, or question.
- `kind: summary`
- `identifiers`: flat list of `key:value` strings using only the keys declared in `config.toml`. Tag every product, app, or service the source is about with `tool:<slug>`. Tag every training program or progression scheme with `scheme:<slug>`. If the source is one of the numbered research notes under `research/`, tag it `slice:<file-stem>`. Slugs are lowercase, hyphenated, no spaces. Omit a key when nothing in the source fits it; never invent a value.

Body: 5 to 12 sentences. Lead with the conclusion. Keep exact numbers, thresholds, plan names, prices, field names, and URLs. Say plainly when the source marks something as unverified.
