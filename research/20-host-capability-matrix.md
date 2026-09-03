# What a packaged skill can do on each host

Reference doc. Facts captured 2026-09-03, against `f741e74`. Answers the owner
constraint, quoted verbatim: "implementation needs to survive adding this as a
skill to the chat-GPT and Claude code webapp chats."

Every claim below carries a vendor URL. Sources are captured in `.kb` and
listed in `research/sources/20-host-capability-matrix.tsv`. Nothing here comes
from model memory. Inferences are labelled INFERENCE and are not facts.

This note extends `research/13-plugin-packaging.md`, which settled where a
`SKILL.md` is read from on each harness. This one settles what the skill can
still do once it is read.

---

## TL;DR

1. **The file format travels. The runtime does not.** One skill folder is
   valid on all three hosts. Only Claude Code gives it a real machine.
2. **No host offers persistent local storage a skill can rely on.** Claude Code
   writes to the user's own working directory, which is the athlete's disk, not
   the skill's. Both web chats hand out a container that is thrown away. A local
   append-only JSON log therefore cannot be the system of record.
3. **Scripts run on all three, with a catch on each.** Claude Code runs them
   through Bash. claude.ai runs them in a container that must have code
   execution switched on. ChatGPT web runs code, but no vendor sentence says it
   runs a skill's bundled `scripts/`, so treat that as unproven.
4. **ChatGPT does have skills now, and calls them Skills.** Same open format.
   The catch: a bare skill folder never reaches chatgpt.com. Web chat only sees
   skills bundled inside a **plugin**.
5. **Nobody lets the skill author own the Notion connection.** On every host the
   athlete authenticates it herself, through MCP or a connector. The author
   ships config and instructions at most.
6. **Unattended runs exist on all three, none of them as a skill feature.** They
   are harness features (Claude Code routines, Claude Cowork scheduled tasks,
   ChatGPT scheduled tasks) that can invoke a skill.

The single fact that most constrains the design: **the normative rules must be
readable in the `SKILL.md` prose**, because the only host where script
execution is both certain and unconditional is the terminal.

---

## Capture metadata

| Field | Value |
|---|---|
| Facts captured | 2026-09-03 |
| Repo commit | `f741e74` |
| Sources | `research/sources/20-host-capability-matrix.tsv`, ingested to `.kb` |
| Vendor page dates seen | `support.claude.com/.../12512198` 2026-07-22, `support.claude.com/.../14503689` 2026-04-10, `learn.chatgpt.com/docs/whats-new` entries to 2026-08. `platform.claude.com` and `code.claude.com` pages carry no visible date. |
| Blocked | Every `help.openai.com` fetch returned HTTP 403. `code.claude.com/docs/en/settings-reference` exceeds the 5 MB ingest cap. Those three are read but not captured, and are logged in `research/sources/ingest-failures.tsv`. |

---

## The matrix

| | Claude Code (terminal) | claude.ai web app (skill ZIP) | ChatGPT web app |
|---|---|---|---|
| **Code execution** | Yes, through the Bash tool on the real machine. Sandbox off by default. Permission prompt unless `allowed-tools` grants it | Yes, in a per-user sandbox container, but only when code execution is enabled. Network access varies by setting | Code and shell run in a managed cloud environment. Whether it runs a skill's bundled `scripts/` is UNKNOWN |
| **Persistent storage** | The user's working directory, which is ordinary local disk. Plus `${CLAUDE_PLUGIN_DATA}` across sessions, deleted on uninstall | None across conversations. Files last "throughout your conversation". Container time is capped, number unpublished | None. The environment refreshes after a run. Project files and memory persist, neither is a filesystem |
| **Store access (Notion)** | MCP. Config ships in `.mcp.json` or a plugin; the user completes OAuth; secrets stay in the keychain | Connectors, backed by MCP, attached by the user. No documented way to ship one inside a skill ZIP | Connectors, backed by MCP. A plugin CAN bundle the MCP server, but the user still authenticates |
| **Package contents** | `SKILL.md` plus any files. `scripts/`, `references/`, `assets/`. Only six frontmatter fields travel to other hosts | Same ZIP, one top-level folder per skill, scripts and resources included. 30 MB per file. Total ZIP cap UNKNOWN | `SKILL.md` plus `scripts/`, `references/`, `assets/`, `agents/openai.yaml`. Standalone skills do not reach web chat; wrap them in a plugin |
| **Background execution** | Not from a skill. Routines run unattended in the cloud on a fresh clone; `/loop` and cron need an open session; hooks need a plugin | Not in claude.ai chat. Claude Cowork scheduled tasks run remotely and can use skills, on paid plans | Yes. Scheduled tasks run unattended and can invoke a skill with `$skill-name` |

---

## 1. Claude Code, terminal

### 1.1 Code execution

Bundled scripts are the documented shape. The skills doc shows the layout with
`scripts/` and the comment "helper.py (utility script - executed, not loaded)"
(https://code.claude.com/docs/en/skills). The runtime is not skill-owned: the
skill body tells Claude to run a path and Claude calls the Bash tool. The spec
is explicit that this is per-client: "Supported languages depend on the agent
implementation. Common options include Python, Bash, and JavaScript."
(https://agentskills.io/specification).

Three variables resolve a bundled path regardless of the working directory:
`${CLAUDE_SKILL_DIR}` is "The directory containing the skill's `SKILL.md`
file", `${CLAUDE_PROJECT_DIR}` is "The project root directory", and
`${CLAUDE_PLUGIN_ROOT}` is the "Absolute path to the plugin's installation
directory" (https://code.claude.com/docs/en/skills,
https://code.claude.com/docs/en/plugins-reference).

Execution is not automatic. Frontmatter `allowed-tools` names "Tools Claude can
use without asking permission during the turn that invokes this skill", and
"The grant clears when you send your next message". The documented pattern for
a prompt-free bundled script: "Using the same variable in both places lets a
skill run a bundled script without a permission prompt"
(https://code.claude.com/docs/en/skills).

Sandboxing is opt-in: `sandbox.enabled` has "Default: `false`"
(https://code.claude.com/docs/en/settings-reference). That page is the one
source here that could not be captured into `.kb`, because it exceeds the 5 MB
ingest cap, so the quote is read but not stored. So terminal Bash normally
touches the real filesystem.

### 1.2 Persistence

The working directory is the athlete's own disk, so anything a script writes
there survives. INFERENCE: no vendor sentence states this outright; it follows
from the terminal running unsandboxed on a local machine, and it is the
weakest-supported claim in this note.

The one documented store a package owns across sessions is the plugin data
directory: "The `${CLAUDE_PLUGIN_DATA}` directory resolves to
`~/.claude/plugins/data/{id}/`", and "A common use is installing language
dependencies once and reusing them across sessions and plugin updates". The
install directory is the wrong place: "`${CLAUDE_PLUGIN_ROOT}` changes when the
plugin updates... treat it as ephemeral and don't write state there". The data
directory "is deleted automatically when you uninstall the plugin from the last
scope where it is installed" (https://code.claude.com/docs/en/plugins-reference).

Within a conversation, the skill text itself persists: "the rendered `SKILL.md`
content enters the conversation as a single message and stays there across
later turns", trimmed by compaction to "the first 5,000 tokens of each" with
"a combined budget of 25,000 tokens" for re-attached skills
(https://code.claude.com/docs/en/skills).

### 1.3 Reaching Notion

MCP is the transport: "Claude Code can connect to hundreds of external tools and
data sources through the Model Context Protocol (MCP)". The user authenticates:
"Use the `/mcp` command within Claude Code... follow the steps in your browser
to log in." Credentials do not travel with the repo, but config does: "The
client secret is stored securely in your system keychain (macOS) or a
credentials file, not in your config", and "Check `.mcp.json` into version
control so everyone on your team gets the same MCP tools and services"
(https://code.claude.com/docs/en/mcp). A plugin can carry the same thing:
"Plugins can bundle Model Context Protocol (MCP) servers"
(https://code.claude.com/docs/en/plugins-reference).

One trap for the cross-host constraint: "MCP servers you added locally in the
CLI with `claude mcp add` are stored on your machine rather than your claude.ai
account, so they do not appear in the connectors list"
(https://code.claude.com/docs/en/routines). A terminal-side Notion connection
is invisible to the web app.

### 1.4 Package contents

"A skill directory may contain any files and directories beyond the required
`SKILL.md`", with `scripts/` for "executable code", `references/` for
"additional documentation", and `assets/` for "static resources". Frontmatter
caps: `name` "Max 64 characters", `description` "Max 1024 characters",
`compatibility` "Max 500 characters". Body size is guidance only, "Instructions
(< 5000 tokens recommended)" and "Keep your main `SKILL.md` under 500 lines"
(https://agentskills.io/specification).

Claude Code truncates harder than the spec cap: "the combined `description` and
`when_to_use` text is truncated at 1,536 characters in the skill listing to
reduce context usage" (https://code.claude.com/docs/en/skills).

Portability is a fixed field set. Claude Code's own error text names it:
"Allowed properties are: allowed-tools, compatibility, description, license,
metadata, name", which is what "claude.ai skill uploads, the Skills API, and
packaging with `package_skill.py`" accept. Claude-only fields (`when_to_use`,
`paths`, `shell`, `disable-model-invocation`, `disallowed-tools`,
`user-invocable`) do not travel (https://code.claude.com/docs/en/skills). That
list is the compatibility contract this repo has to write against.

### 1.5 Background execution

None of this belongs to a skill. Three harness features can invoke one.

`/loop` and the cron tools need the session open: "Tasks are session-scoped:
they live in the current conversation and stop when you start a new one", and
"Tasks only fire while Claude Code is running and idle". Recurring tasks
"automatically expire 7 days after creation". A gate that matters here: "A
scheduled fire only runs skills that Claude is allowed to invoke on its own"
(https://code.claude.com/docs/en/scheduled-tasks).

Routines are the unattended path: "Routines execute on Anthropic-managed cloud
infrastructure... so they keep working when your laptop is closed", and "The
session can run shell commands, use skills committed to the cloned repository,
and call any connectors you include". They are "available on Pro, Max, Team,
and Enterprise plans" and "in research preview". They get no local disk, only a
fresh clone, and the minimum interval is one hour
(https://code.claude.com/docs/en/routines).

Hooks fire outside a user turn, including `FileChanged` "When a watched file
changes on disk", but they are plugin-level, defined "in `hooks/hooks.json`"
(https://code.claude.com/docs/en/hooks). INFERENCE: a bare skill folder buys
none of these. Scheduling is a packaging decision, not a skill one.

---

## 2. claude.ai web app, skill uploaded as a ZIP

### 2.1 Code execution

Yes, and with a real filesystem inside the container: "Skills run in a code
execution environment where Claude has filesystem access, bash commands, and
code execution capabilities"
(https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

It is conditional. "This feature requires code execution to be enabled"
(https://support.claude.com/en/articles/12512180-use-skills-in-claude), switched
on under "Settings > Capabilities by toggling Code execution and file creation
on", though for Team and Enterprise "This capability is enabled by default at
the organization level"
(https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude).

Files inside the ZIP are readable and scripts are runnable: "When a Skill is
triggered, Claude uses bash to read SKILL.md from the filesystem... If those
instructions reference other files... Claude reads those files too", and "When
instructions mention executable scripts, Claude runs them through bash and
receives only the output" (platform overview URL above).

Isolation is per user: "Implemented sandbox isolation such that no sandbox
environments are ever shared between users". Network egress is not guaranteed:
"Depending on user/admin settings, Skills may have full, partial, or no network
access", with a default allowlist of "github.com, registry.npmjs.org, pypi.org,
files.pythonhosted.org, crates.io, archive.ubuntu.com, yarnpkg.com"
(support 12111783 and the platform overview).

### 2.2 Persistence

Inside one conversation, files hold: "Files remain available for download
throughout your conversation". Across conversations, no vendor statement grants
persistence, and the container is time-limited: Anthropic "Limited the duration
of tasks that can be completed by Claude and the length of time you can use a
single sandbox container", with no number published
(https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude).

The 30-day container lifetime and the container-id reuse knob belong to the
API's code execution tool, not to claude.ai chat: "Containers expire 30 days
after creation" and "Each request runs in a new container unless you pass an
earlier response's container ID back"
(https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool).
Chat exposes no such knob. Treat claude.ai storage as ephemeral.

### 2.3 Reaching Notion

Connectors, attached and authenticated by the athlete. "Connectors let Claude
access your apps and services, retrieve your data, and take actions within
connected services", reached by clicking "the '+' button in the lower left of
the chat interface", and "Claude inherits each person's permissions from the
connected service"
(https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities).
Auth is per user: "Connectors use delegated, per-user OAuth wherever possible"
(https://support.claude.com/en/articles/14503689-mcp-connectors, dated
2026-04-10 and scoped to Claude for Government, so read it as indicative).

Notion ships an official one: "Create, edit, search and organize Notion content
directly from Claude", used in "Claude, Claude desktop app, Claude mobile app,
Claude Code, Claude API" (https://claude.com/connectors/notion).

No documented way exists to ship a connector inside a skill ZIP. INFERENCE: the
skill can only instruct the athlete to connect Notion herself, which makes the
connection a setup step the skill must check for, not something it can assume.

### 2.4 Package contents and limits

More than prose ships. Skills are "folders of instructions, scripts, and
resources that Claude loads dynamically"
(https://support.claude.com/en/articles/12512176-what-are-skills), and the ZIP
shape is one top-level folder holding `skill.md` plus resources
(https://support.claude.com/en/articles/12512198-creating-custom-skills).

| Limit | Value | Source |
|---|---|---|
| `name` | "Maximum 64 characters" | platform overview |
| `description`, spec | "Maximum 1024 characters" | platform overview |
| `description`, claude.ai create form | "(200 characters maximum)" | support 12512198 |
| Per file | "The maximum file size is 30MB per file for both uploads and downloads" | support 12111783 |
| Bundled content | "No practical limit on bundled content" | platform overview |

The 200 against 1024 character conflict is unresolved. Both pages are vendor.
Writing every description under 200 characters satisfies both, so this repo
should do that rather than wait for a ruling.

Distribution is per person: "claude.ai does not support centralized admin
management or org-wide distribution of custom Skills", each member "must upload
separately", and "Skills uploaded to claude.ai must be separately uploaded to
the API" (platform overview).

### 2.5 Background execution

Not in claude.ai chat. The scheduling product is Cowork: "Scheduled tasks allow
you to delegate work to Claude Cowork by creating tasks that run automatically
on a recurring basis, or on demand", they "run remotely, so they run on their
cadence even when your computer is asleep", they have "access to the same
capabilities as regular Cowork tasks, including connected tools, skills, and
installed plugins", and they need a paid plan
(https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork).

### 2.6 Which plans

Two vendor pages disagree. The help centre says "Skills are available for users
on Free, Pro, Max, Team, and Enterprise plans" (support 12512180). The platform
docs say "Available on Pro, Max, Team, and Enterprise plans with code execution
enabled" (platform overview). Unresolved. It matters, because
`research/13-plugin-packaging.md` section 6 sold the ZIP path partly on it
running on Free.

---

## 3. ChatGPT

The owner asked about "the chat-GPT ... webapp chats". Two OpenAI hosts read a
`SKILL.md` and they are not the same product. Keep them apart.

### 3.1 The concept exists, and it is called Skills

"A skill packages instructions and supporting resources for a specific task or
workflow." A plugin is "an installable bundle that can include skills,
connectors, or both". Connectors "are backed by Model Context Protocol (MCP)
servers" (https://learn.chatgpt.com/docs/skills-and-plugins).

The sentence that decides the packaging:

> "Standalone skills are available in the ChatGPT desktop app, Codex CLI, and
> IDE extension. Skills bundled in plugins are also available in Chat and Work
> across ChatGPT on the web, desktop, and mobile."
> (https://learn.chatgpt.com/docs/build-skills)

So an athlete typing into chatgpt.com reaches plugin-bundled skills only. The
same page says to "package them as a plugin" to distribute a reusable skill.
Invocation is by mention: "ChatGPT supports `@` mentions, while Codex supports
`$` mentions for skills" (skills-and-plugins URL above).

Codex, the coding agent, is the other host and needs no upload: "Codex scans
`.agents/skills` in every directory from your current working directory up to
the repository root", plus `$HOME/.agents/skills` and `/etc/codex/skills`
(build-skills URL above). That is the path `research/13-plugin-packaging.md`
section 2 already covers. Note the docs moved:
`developers.openai.com/codex/skills` now 308-redirects to
`learn.chatgpt.com/docs/build-skills`, so note 13's URL is stale.

The format is shared. agentskills.io lists ChatGPT and Codex as clients and
states "The Agent Skills format was originally developed by Anthropic, released
as an open standard" (https://agentskills.io/). INFERENCE: one folder on disk
satisfies both vendors; only the delivery differs.

Custom GPTs, the GPT Store, and Actions are not the current answer. No vendor
page found positions them as the skill equivalent. Not disproven, just absent
from today's docs.

### 3.2 Code execution

"ChatGPT Work runs code and shell commands in a managed, isolated environment"
(https://learn.chatgpt.com/docs/sandboxing?surface=web), and Work "uses tools
like code/shell execution and the cloud browser to complete tasks". Network is
policy-gated: "Public internet access depends on the applicable workspace
policy and individual Work network setting", and the environment is remote:
"Work on the web can't directly access files, applications, or open browser tabs
on the user's computer"
(https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview). The local
sandbox belongs to the other surfaces: "ChatGPT web doesn't expose the local
Codex sandbox or approval-mode selector"
(https://learn.chatgpt.com/docs/sandboxing).

What is missing is the join. `scripts/` is labelled "Optional: executable code",
and web chat runs code, but no vendor sentence says web chat executes a skill's
bundled scripts. UNKNOWN, and it is the gap that decides whether this repo's
Python can be load-bearing on ChatGPT.

### 3.3 Persistence

The nearest vendor statement is the opposite of persistence: "Changes take
effect after the current code or shell run finishes and Work refreshes its
execution environment"
(https://learn.chatgpt.com/docs/sandboxing?surface=web).

What does persist is not a filesystem. Projects "carry project files and context
across related chats", though "A ChatGPT project doesn't provide direct access
to a folder on your computer" (https://learn.chatgpt.com/docs/projects). The
Library holds output: "eligible uploaded or generated files can be saved there"
(chatgpt-work-overview URL above). The memories page served is the Codex
variant, where "The main memory files live under `~/.codex/memories/`"
(https://learn.chatgpt.com/docs/customization/memories), which says nothing
about the web product.

### 3.4 Reaching Notion

A plugin author can ship the server, but not the login. "Installed plugins can
bundle MCP servers in their plugin manifest. Those servers are launched from the
plugin, so user config doesn't set their transport command"
(https://learn.chatgpt.com/docs/extend/mcp), declared in
`.codex-plugin/plugin.json`, where "skills, mcpServers, and hooks point to
bundled components relative to the plugin root"
(https://developers.openai.com/plugins/build/plugins).

The athlete still authenticates: "If the plugin needs a connector, connect it
when prompted. Some plugins ask you to authenticate during install", and
"Connections to external services use that service's own authentication and
access controls" (https://learn.chatgpt.com/docs/plugins). Supported methods are
"Bearer token authentication" and "OAuth authentication, including Client ID
Metadata Documents (CIMD) and Dynamic Client Registration (DCR)" (extend/mcp).
One trap: "Some plugins aren't available with API key authentication because
their connection flows require unsupported OAuth capabilities" (plugins URL).

This is the only host where the author gets to ship the MCP wiring rather than
just describe it.

### 3.5 Package contents and limits

"A skill is a directory with a `SKILL.md` file plus optional scripts and
references", and "The `SKILL.md` file must include `name` and `description`"
(https://learn.chatgpt.com/docs/build-skills). The layout is `SKILL.md`,
`scripts/` for executable code, `references/`, `assets/`, and an optional
`agents/openai.yaml` for appearance and dependencies.

The one numeric limit with a verbatim vendor quote is a discovery budget, not a
package cap: the skill list "uses at most 2% of the model's context window, or
8,000 characters when the context window is unknown" (build-skills). File-size
and file-count numbers circulating in search summaries of `help.openai.com`
could not be fetched, so they are excluded.

### 3.6 Background execution

"Scheduled tasks run unattended with your default sandbox settings", and
"Scheduled tasks can also use skills", triggered explicitly "by using
`$skill-name`". Web is in scope: "Scheduled tasks created with ChatGPT Work on
the web, or with ChatGPT Work or Codex in the desktop app, can use plugins"
(https://learn.chatgpt.com/docs/automations). Hooks are Codex-only: "Hooks are
an extensibility framework for Codex"
(https://learn.chatgpt.com/docs/hooks), with no stated web support.

---

## 4. What this constrains

Three findings, in the order they bite.

**The rules have to live in the prose.** Script execution is certain and
unconditional only in the terminal. On claude.ai it depends on a capability
toggle the athlete controls, and on ChatGPT web it is unproven. So `SKILL.md`
carries the normative rules and the scripts become an accelerator that must
agree with the prose. A rule that exists only inside a `.py` file is a rule that
silently disappears on two of three hosts.

**A local append-only JSON log cannot be the system of record.** Neither web
host promises a file survives to the next conversation, and the claude.ai
container is time-capped with the number unpublished. The record has to be the
external store, reached through a connector the athlete authenticates. That
matches where `docs/architecture.md` already points, and this note removes the
alternative rather than adding one.

**Packaging forks three ways for one source folder.** Claude Code takes
`.claude/skills/<name>/`, claude.ai takes the ZIP that
`tools/package/build_zip.py` already builds, and ChatGPT web needs a plugin
wrapper with `.codex-plugin/plugin.json` that this repo does not have. Only six
frontmatter fields survive the crossing, so any Claude-only field is a portability
bug waiting for the first ChatGPT upload.

---

## 5. Unknown, with what was searched

Marked unknown deliberately. None of these is filled with a guess.

1. **Whether ChatGPT web runs a skill's bundled `scripts/`.** Fetched
   `learn.chatgpt.com/docs/build-skills` twice, default and `?surface=web`, plus
   the two sandbox variants. `scripts/` is labelled executable, web chat runs
   code, and no sentence joins them.
2. **Which ChatGPT plans get Skills.** Every verbatim web-surface quote says
   "ChatGPT Work", the workspace product. `help.openai.com/en/articles/20001066`
   and `openai.com/academy/skills/` both returned HTTP 403 on every attempt. So
   whether a Free or Plus athlete can use skills at all is unverified, and it is
   the gap most likely to sink the ChatGPT half of the constraint.
3. **claude.ai container lifetime.** Vendor says the duration is limited and
   publishes no number. Searched support 12111783 including its anchors, plus
   site-scoped searches on container persistence and expiry.
4. **claude.ai ZIP total size cap, file count, skills per account.** The help
   article warns a ZIP can exceed "size limits" without stating one. Searched
   support 12512180, 12512198, 12512176, and the platform overview.
5. **claude.ai description limit, 200 or 1024.** Two vendor pages, both current,
   flat contradiction. Unresolved by fetching; would take an upload attempt.
6. **Claude Code `autoAllowBashIfSandboxed` default.** `sandboxing` says it
   "still defaults to `true`", `settings-reference` says false. Both vendor,
   unresolved.
7. **Claude Code desktop scheduled tasks.** Only the summary row from
   `scheduled-tasks` was captured. `code.claude.com/docs/en/desktop-scheduled-tasks`
   was not fetched. It is the only path offering scheduled runs with local file
   access, so it is worth a follow-up.
8. **Whether a skill author can ship a connector on claude.ai.** No vendor
   sentence found either way. Searched support 11176164, 14503689, and
   claude.com/connectors/notion.
9. **Whether skills uploaded at claude.ai work in the iOS and Android apps.**
   Still open from `research/13-plugin-packaging.md` section 9. Not settled here.
10. **Current status of Custom GPTs.** Whether they are deprecated, maintained,
    or repositioned against Skills. Both help-centre articles returned 403.
11. **ChatGPT per-skill size limits and scheduled-task recurrence caps.** Not
    stated on build-skills, build-plugins, or the plugin builder docs. The
    numbers in search summaries trace to `help.openai.com`, which is 403.

---

## 6. Open questions for the owner

This note cannot ask, so the questions live here.

1. **Is ChatGPT web a real target, or is Codex enough?** If the athlete or her
   friend types into chatgpt.com, the repo needs a plugin wrapper and unknown 2
   has to be settled first. If ChatGPT means Codex CLI, the existing
   `.agents/skills` path already covers it and no new packaging is needed.
2. **Does anything in this repo still assume a local file is the record?** The
   answer here says the store must be external on two of three hosts. Whether
   that changes an already-made decision is a call, not a finding.
3. **Do the seven skill descriptions get cut to 200 characters now?** It costs
   little and it removes a known claude.ai failure mode.
