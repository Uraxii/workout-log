# Packaging the workout-log skills for Claude, Codex and Copilot, plus the phone path

Written 2026-09-01. Answers the user order: "We need a git repo and make this a
plugin for common harnesses" / "Claude, codex, copilot" / phone path "Either RC
to my PC".

Sources: `research/sources/13-plugin-packaging.tsv`. All 14 ingested to `.kb`.

---

## TL;DR

1. **One SKILL.md format serves all three.** Agent Skills is a real open
   standard at agentskills.io, written by Anthropic, released open, and Claude
   Code, GitHub Copilot and Codex all list themselves as clients
   (https://agentskills.io/). Skill = folder + `SKILL.md` + frontmatter `name`
   and `description`. Write once.
2. **The dirs differ, not the format.** Claude Code reads `.claude/skills/`.
   Copilot reads `.github/skills`, `.claude/skills` **and** `.agents/skills`.
   Codex reads `.agents/skills` only. So `.claude/skills/` covers two of three
   harnesses with zero extra work; Codex needs one symlink.
3. **Skills do not need a plugin.** A plain `.claude/skills/<name>/SKILL.md` in
   the repo works in Claude Code. Plugin buys namespacing, versioning, one-command
   install, and the ability to ship agents + hooks + MCP config with the skills.
4. **Plugin = git repo with `.claude-plugin/plugin.json`.** Marketplace = git
   repo with `.claude-plugin/marketplace.json`. Same repo can be both. Install is
   `/plugin marketplace add owner/repo` then `/plugin install name@marketplace`.
5. **Remote Control is real and it does what the user wants.** Phone drives a
   Claude Code session running on her PC. Local filesystem, MCP servers (Notion
   included), and project config stay live. Needs **Pro or better** and the PC
   awake with `claude` running.
6. **The friend does not need a PC.** claude.ai Customize > Skills takes a ZIP
   upload, on **Free** and up, no terminal. That is the terminal-free path, and
   it beats the note-06 default of pasting skills into Notion child pages.

**The one thing that changes the plan:** open question 31 in
`00-synthesis-system.md` defaulted trainer skills to Notion child pages "so
replication is one click". A ZIP upload at claude.ai is also one click, and it
gets real skill semantics (progressive disclosure, model invocation) instead of
a page the agent has to be told to read. Section 6 argues for the switch.

---

## 1. Claude Code: plugin format, layout, install

### 1.1 Do skills need a plugin? No.

Four levels, all reading the same `SKILL.md`
(https://code.claude.com/docs/en/skills):

| Level | Path | Applies to |
|---|---|---|
| Enterprise | managed settings dir | all org users |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | all your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | this project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | where plugin enabled |

Precedence: enterprise over personal over project. Plugin skills are namespaced
`plugin-name:skill-name`, so they never collide.

Project skills load from `.claude/skills/` in the start directory and every
parent up to the repo root. Claude Code watches those dirs and picks up edits
mid-session, no restart, for `SKILL.md` text.

**A `<skill-name>` entry can be a symlink to a directory elsewhere on disk.**
Claude Code follows it and reads `SKILL.md` from the target. Same target reachable
twice loads once. This is the lever for the cross-harness layout in section 7.

### 1.2 Plugin manifest

`.claude-plugin/plugin.json`. Only `name` is required
(https://code.claude.com/docs/en/plugins-reference).

```json
{
  "name": "workout-trainer",
  "displayName": "Workout Trainer",
  "version": "1.0.0",
  "description": "Logging grammar, progression rules and coaching skills",
  "author": { "name": "Nicole" },
  "repository": "https://github.com/Uraxii/workout-log",
  "license": "MIT",
  "skills": "./skills/",
  "mcpServers": "./.mcp.json"
}
```

Path fields: `skills` **adds to** the default `skills/` scan. `commands`,
`agents`, `workflows`, `outputStyles` **replace** their defaults. `hooks`,
`mcpServers`, `lspServers` merge. Paths are relative to plugin root, start with
`./`, no `../` escape.

### 1.3 Directory layout

All component dirs sit at **plugin root**, never inside `.claude-plugin/`. The
docs call that the common mistake.

```
workout-trainer/
├── .claude-plugin/
│   └── plugin.json         # ONLY this file goes here
├── skills/
│   └── log-set/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── agents/                 # subagent .md definitions
├── hooks/hooks.json
├── .mcp.json               # MCP servers, e.g. Notion
├── settings.json           # only `agent` and `subagentStatusLine` honoured
└── bin/                    # added to Bash PATH while enabled
```

A one-skill plugin can put `SKILL.md` at plugin root and skip `skills/`.

### 1.4 Marketplace and install

Marketplace is a git repo carrying `.claude-plugin/marketplace.json`
(https://code.claude.com/docs/en/plugin-marketplaces):

```json
{
  "name": "uraxii-plugins",
  "owner": { "name": "Nicole", "email": "accounts@nicolepaul.net" },
  "plugins": [
    { "name": "workout-trainer", "source": "./", "description": "..." }
  ]
}
```

Source types: relative path, `github` (`{"source":"github","repo":"owner/repo","ref":"v2.0.0","sha":"..."}`),
`url` (any git URL), `git-subdir`, `npm`, `archive` (zip URL), `command`.

Per-user install, two commands:

```
/plugin marketplace add Uraxii/workout-log
/plugin install workout-trainer@uraxii-plugins
```

CLI equivalent:

```
claude plugin marketplace add Uraxii/workout-log
```

Team/repo auto-install, in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "uraxii-plugins": { "source": { "source": "github", "repo": "Uraxii/workout-log" } }
  },
  "enabledPlugins": { "workout-trainer@uraxii-plugins": true }
}
```

Anyone who trusts the folder gets it. Private repos work; auth is the user's
own git credentials.

Dev loop without installing:

```
claude --plugin-dir ./workout-trainer
claude plugin validate ./workout-trainer
```

`/reload-plugins` picks up changes without restart.

### 1.5 The lazy middle option

`claude plugin init my-tool` writes `~/.claude/skills/my-tool/` with a
`.claude-plugin/plugin.json` and a starter `SKILL.md`. It loads next session as
`my-tool@skills-dir`, no marketplace, no install step. Good for a plugin that is
only ever yours.

---

## 2. Codex CLI

Discovery order (https://learn.chatgpt.com/docs/build-skills):

| # | Location |
|---|---|
| 1 | `$CWD/.agents/skills` |
| 2 | `$CWD/../.agents/skills` (parents) |
| 3 | `$REPO_ROOT/.agents/skills` |
| 4 | `$HOME/.agents/skills` |
| 5 | `/etc/codex/skills` (admin) |
| 6 | bundled from OpenAI |

Note the dir is `.agents/skills`, **not** `.codex/skills`. Secondary write-ups
(Simon Willison, Dec 2025) report `~/.codex/skills` from the original
experimental PR; the current first-party doc says `.agents/skills`. Treating the
old path as superseded. **UNVERIFIED** whether `~/.codex/skills` still works as a
legacy alias.

`SKILL.md` frontmatter, both mandatory:

```yaml
---
name: skill-name
description: Explain exactly when this skill should and should not trigger.
---
```

Optional `agents/openai.yaml` inside the skill dir sets UI metadata and policy:

```yaml
interface:
  display_name: "Log a set"
  short_description: "..."
policy:
  allow_implicit_invocation: false
dependencies:
  tools:
    - type: "mcp"
```

Disable a skill in `~/.codex/config.toml`:

```toml
[[skills.config]]
path = "/path/to/skill/SKILL.md"
enabled = false
```

**Install path for a git repo:** clone it and put the skill dirs under
`.agents/skills` at repo root (per-project) or `$HOME/.agents/skills`
(per-user). There is no marketplace verb. The doc shows `$skill-installer <name>`
for OpenAI's curated set only. Codex auto-detects skill changes; restart if not.

**AGENTS.md:** Codex reads it. Repo root, nearest file in the directory tree
wins, plain Markdown, no required fields (https://agents.md/). That is the place
for the "how this repo works" text, not for skills.

---

## 3. GitHub Copilot: CLI and coding agent

### 3.1 Skills

Copilot loads agent skills across **Copilot cloud agent (the coding agent),
Copilot code review, Copilot CLI, the GitHub Copilot app, and agent mode in VS
Code and JetBrains**
(https://docs.github.com/en/copilot/concepts/agents/about-agent-skills).

| Scope | Directories |
|---|---|
| Project | `.github/skills`, `.claude/skills`, `.agents/skills` |
| Personal | `~/.copilot/skills`, `~/.agents/skills` |

**Copilot reading `.claude/skills` is the single most useful fact in this note.**
Nothing extra ships for Copilot if the skills live there.

Frontmatter (https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills):

| Field | Required | Note |
|---|---|---|
| `name` | yes | lowercase, hyphens for spaces |
| `description` | yes | what it does and when Copilot should use it |
| `license` | no | |
| `allowed-tools` | no | pre-approves tools such as `shell`, skips confirm prompts |

Install: drop the skill directory into a project or personal location, then
`/skills reload` (or restart), verify with `/skills info SKILL-NAME`. Copilot
picks up every file in the skill dir, so `scripts/` and `references/` come along.

### 3.2 Custom agents

`.agent.md` files, YAML frontmatter plus a Markdown body used as the system
prompt (https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli):

| Scope | Path |
|---|---|
| Repo | `.github/agents/<name>.agent.md` |
| Personal | `~/.copilot/agents/<name>.agent.md` |

Same name in both, the home one wins. Discovered at session start.

### 3.3 Instructions

Three kinds (https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions):

| File | Scope | Surfaces |
|---|---|---|
| `.github/copilot-instructions.md` | whole repo | Copilot on GitHub, code review |
| `.github/instructions/NAME.instructions.md` | path-matched | on GitHub.com, **cloud agent and code review only** |
| `AGENTS.md` (anywhere), or `CLAUDE.md`/`GEMINI.md` at root | nearest wins | AI agents generally |

Copilot recognising `CLAUDE.md` at root means the existing project CLAUDE.md is
already doing double duty.

---

## 4. Is there a cross-harness spec? Yes.

**Agent Skills**, https://agentskills.io. Originally Anthropic, released as an
open standard, now taking outside contributions
(https://github.com/agentskills/agentskills). The client list includes Claude
Code, Claude, GitHub Copilot, VS Code, ChatGPT & Codex, Cursor, Gemini CLI,
Goose, OpenCode, JetBrains Junie, and about 40 others.

Full frontmatter spec (https://agentskills.io/specification):

| Field | Required | Constraint |
|---|---|---|
| `name` | yes | 1-64 chars, lowercase `a-z0-9` and `-`, no leading/trailing/double hyphen, **must match the parent directory name** |
| `description` | yes | 1-1024 chars, says what it does *and* when to use it |
| `license` | no | license name or bundled file name |
| `compatibility` | no | max 500 chars, environment requirements |
| `metadata` | no | string-to-string map, client-specific extras |
| `allowed-tools` | no | space-separated tool list. Experimental, support varies |

Directory conventions: `scripts/`, `references/`, `assets/`. Progressive
disclosure in three stages: name+description at startup (~100 tokens), full
`SKILL.md` on activation (keep under 5000 tokens / 500 lines), bundled files on
demand. Validate with `skills-ref validate ./my-skill`.

Claude Code extends the standard with `disable-model-invocation`, subagent
execution and dynamic context injection; those fields are Claude-only and other
harnesses ignore them. Keep them out of any skill that has to travel.

**So: one dir of standard-conformant skill folders serves all three.** The only
per-harness work is where that dir sits.

---

## 5. Claude mobile app Remote Control

Source: https://code.claude.com/docs/en/remote-control.

**What it is.** The Claude iOS/Android app or claude.ai/code connects to a Claude
Code session **running on your machine**. The phone is a window into the local
session, not a cloud copy. Contrast with Claude Code on the web, which runs on
Anthropic infrastructure.

**Plan.** The page's own note says "available on all plans"; its Requirements
section says "available on Pro, Max, Team, and Enterprise plans. API keys are not
supported." Reading the two together: **Pro or better, not Free.** The "all
plans" line is about the admin toggle, not about Free. Flagged as an internal
inconsistency in the source, not resolved.

Other requirements: `/login` through claude.ai; `ANTHROPIC_BASE_URL` must be
unset or pointed at `api.anthropic.com`; not available on Bedrock, Google Cloud
Agent Platform or Microsoft Foundry; `DISABLE_TELEMETRY`, `DO_NOT_TRACK`,
`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` and `DISABLE_GROWTHBOOK` each break
the feature-flag check and must be unset; run `claude` once in the project dir to
accept workspace trust.

**Start it:**

```
claude remote-control          # server mode, prints a URL, spacebar for QR
claude --remote-control        # normal interactive session, also remote
/remote-control                # from inside a running session, keeps history
```

**Does local config load?** The doc names "your filesystem, MCP servers, tools,
and project configuration". Skills and plugins are not named in that sentence,
but two things imply they load: it is an ordinary local session, and
`/reload-plugins` is on the list of commands that work from mobile while
`/plugin` is local-CLI-only. So plugin skills run from the phone; you just cannot
install or enable a plugin from the phone. **UNVERIFIED**: no doc sentence states
"skills load in Remote Control" outright. One session on a phone settles it.

**Notion MCP specifically:** `/mcp` works from mobile from v2.1.166, returning a
text status summary instead of the picker, and `reconnect`/`enable`/`disable`
subcommands work. So the Notion connector configured on the PC is reachable and
recoverable from the gym.

**Offline / gym behaviour:**

| Situation | What happens |
|---|---|
| Laptop sleeps, or phone loses signal | Auto-reconnects when back online. Messages, permission prompts and subagent updates are queued and delivered on recovery |
| PC network outage, PC awake | Interactive mode keeps working locally and retries for the whole outage |
| Terminal closed / `claude` process killed | Session goes offline within seconds. Must be brought back from the PC. Use `tmux` or `screen` to survive an SSH drop |
| Phone has no signal | Nothing. The phone talks to the Anthropic API, not to the PC directly |

**Friend replication: yes, needs a PC.** The friend needs a machine running
`claude` continuously, a Pro-or-better plan, a claude.ai login, and workspace
trust accepted. That is a terminal, a always-on computer, and a subscription. It
is not the five-step no-command-line path in `00-synthesis-system.md` "Friend
replicates it".

---

## 6. Cheapest terminal-free path for the friend

**claude.ai skill upload.** Source: https://support.claude.com/en/articles/12512180-use-skills-in-claude.

- Go to **Customize > Skills** (claude.ai/customize/skills).
- Click `+`, then **`+ Create skill`**, then **Upload a skill**.
- Upload a **ZIP** of the skill folder.
- Available on **Free, Pro, Max, Team and Enterprise**.
- Prerequisite: **code execution enabled**, at Settings > Capabilities. Team and
  Enterprise admins gate it org-wide at Organization settings > Skills.
- **UNVERIFIED**: the help article does not say whether skills work in the iOS
  and Android apps, only that they attach to the account. Worth a 30-second test.

**Ranking of terminal-free options:**

| Option | Terminal? | PC? | Plan | Real skill semantics | Steps for friend |
|---|---|---|---|---|---|
| **claude.ai ZIP upload** | no | no | Free+ (code execution on) | yes: progressive disclosure, model invocation | 3 |
| Notion child pages read by the connector (S31 default) | no | no | Free | no: pages the agent must be told to read | 2, plus a prompt convention |
| Claude Project with instructions | no | no | Free | no: one static instruction blob | 2 |
| Claude Code on the web | no | no | **Pro/Max/Team** (note 01) | yes, plus repo `.claude/skills/` | 4 |
| Remote Control to a PC | **yes** | **yes** | **Pro+** | yes, everything local | many |

**Recommendation for the friend: claude.ai ZIP upload.** Same click count as the
Notion duplicate, no plan upgrade, and the skills behave as skills instead of as
pages. It does not replace the Notion store; the data still lives in Notion
through the connector. It replaces open question 31's answer about where the
*skill text* lives.

Caveat: uploaded skills are private to the account, so distribution is "hand them
the ZIP", not "install from a link". For one friend, fine.

---

## 7. Recommendation: one repo layout

Canonical dir is **`.claude/skills/`**, because Claude Code and every Copilot
surface read it natively. Codex is the only harness needing a bridge.

```
workout-log/                              # the git repo
├── AGENTS.md                             # Codex + Copilot + everyone: what this repo is
├── CLAUDE.md                             # already exists; Copilot reads it at root too
├── .claude/
│   ├── skills/                           # CANONICAL. Agent Skills spec, no Claude-only fields
│   │   ├── log-set/SKILL.md
│   │   ├── progression/SKILL.md
│   │   └── intake/SKILL.md
│   └── settings.json                     # extraKnownMarketplaces + enabledPlugins
├── .agents/
│   └── skills/                           # Codex bridge: symlinks per skill
│       ├── log-set -> ../../.claude/skills/log-set
│       └── ...
├── .github/
│   ├── copilot-instructions.md           # repo-wide Copilot instructions
│   └── agents/trainer.agent.md           # optional Copilot CLI custom agent
├── .claude-plugin/
│   ├── plugin.json                       # "skills": "./.claude/skills/"
│   └── marketplace.json                  # self-marketplace, source "./"
├── .mcp.json                             # Notion MCP, shipped with the plugin
└── dist/workout-trainer-skills.zip       # built artifact for the claude.ai upload path
```

Per-skill symlinks, not a whole-dir symlink: Claude Code documents symlink
support for a `<skill-name>` **entry**. Whole-directory symlinking of
`.agents/skills` is **UNVERIFIED** for both Codex and Claude Code. Per-skill
links are the documented shape. A three-line `make skills` target generates them
and the ZIP; do not maintain them by hand.

`plugin.json` pointing `skills` at `./.claude/skills/` is legal by the path rules
(relative, `./`-prefixed, inside the plugin root) but is **UNVERIFIED** for a
dotted directory. Fallback if it fails: make `skills/` the canonical dir and
symlink `.claude/skills/<name>` at it instead. Same total link count.

### Tradeoffs

| Layout | Claude Code | Codex | Copilot | Plugin install | Cost |
|---|---|---|---|---|---|
| **Canonical `.claude/skills/` + `.agents/skills` symlinks** (recommended) | native | via symlink | native | `skills` field in plugin.json | 1 symlink per skill, generated |
| Canonical `.agents/skills/` + `.claude/skills` symlinks | via symlink | native | native | `skills` field | same link count, but the harness she uses most needs the indirection |
| Canonical `skills/` at plugin root, symlink both others | via symlink | via symlink | via symlink | native, zero config | 2 links per skill. Most "correct", most churn |
| Duplicate copies in all three dirs | native | native | native | native | drift. Rejected: three copies of one truth is the bug this repo is trying to avoid |
| Plugin only, no plain dirs | needs install | broken | broken | native | Codex and Copilot see nothing. Rejected |
| No repo, claude.ai ZIP only | via sync | no | no | n/a | zero infrastructure. Right answer if she never uses Codex or Copilot |

### Sequencing

1. Write the skills to the Agent Skills spec in `.claude/skills/`. No
   `disable-model-invocation`, no Claude-only frontmatter, in any skill that
   travels. Validate with `skills-ref validate`.
2. `AGENTS.md` and `.github/copilot-instructions.md` next: cheapest coverage,
   no format risk.
3. Add `.claude-plugin/plugin.json` and `marketplace.json` when a second person
   wants a one-command install. Not before.
4. Codex symlinks and the ZIP build target only when a Codex user or a
   no-terminal friend actually exists.

Step 3 and 4 are speculative until someone asks. Steps 1 and 2 are the whole job
for a single user on Claude Code.

---

## 8. Open questions for the user

The global instruction says to ask when unclear. This note cannot ask, so the
questions live here.

1. **Which harnesses do you actually use?** The brief names Claude, Codex and
   Copilot. If it is only Claude Code plus the phone, sections 2, 3 and most of 7
   are dead weight and step 1 above is the entire build.
2. **Do you have a Claude plan?** `00-synthesis-system.md` open question 2
   defaults to "assume no paid plan", and that assumption is why Notion won over
   git. Remote Control needs **Pro or better**. If the answer is still no, the
   phone path stays "Claude mobile app plus the Notion connector" and Remote
   Control is off the table.
3. **Does open question 31 change?** It defaulted trainer skills to Notion child
   pages. Section 6 says the claude.ai ZIP upload is the same click count, runs
   on Free, and gives real skill semantics. Overriding S31 is a decision, not a
   research finding, so it is left to you.
4. **Repo public or private?** A public repo makes `/plugin marketplace add
   Uraxii/workout-log` work for anyone with no auth. Private works too, on the
   installer's own git credentials. Training logs in a public repo is a privacy
   call, and note 10's data-handling rules apply if any medical intake text ends
   up in a skill file.
5. **Is the friend's device the only device?** If she has no always-on PC, drop
   Remote Control from her instructions entirely and give her the ZIP.

---

## 9. What is unverified

- Skills loading inside a Remote Control session: implied by
  `/reload-plugins` working from mobile and `/plugin` not, never stated.
- Whether skills uploaded at claude.ai are usable from the iOS and Android apps.
- Whether `~/.codex/skills` still works as a legacy Codex path.
- Whether a whole-directory symlink at `.agents/skills` is followed by Codex, or
  by Claude Code at `.claude/skills`.
- Whether `plugin.json`'s `skills` field accepts a dotted path like
  `./.claude/skills/`.
- The Remote Control plan requirement: the source page states "all plans" and
  "Pro, Max, Team, and Enterprise" in two places. Read as Pro-and-up here.
- Codex marketplace-style installation: the doc shows `$skill-installer <name>`
  for OpenAI's curated skills only. No first-party mechanism found for
  installing a third-party skill repo beyond cloning it into `.agents/skills`.
