# Where should the workout log live?

Researched 2026-08-31. Every price and plan claim was re-fetched from the vendor's own page on that date. Anything I could not confirm from a primary source is marked UNVERIFIED.

## TL;DR

**Recommended: Notion, on the Free plan.** The belief that agent access needs a $24/mo plan is wrong. Notion's own pricing comparison grid shows Public API and Webhooks with a checkmark on Free ([notion.com/pricing](https://www.notion.com/pricing), grid rows parsed from the page HTML on 2026-08-31). An internal integration token plus the REST API gives an agent unattended read and write for $0. Phone editing is a real native app, web is behind a login, sharing works through Publish (unlimited published pages on Free) or up to 10 external guests. A friend replicates it in about 4 steps.

**Runner-up: plain markdown or CSV in a private git repo,** with Claude Code committing to it and the GitHub web UI or mobile app for hand edits. Free, zero lock-in, agent write path is just `git commit`. It loses on phone editing speed and gains nothing over Notion unless you specifically want files.

**What I would drop:** the Obsidian vault + Obsidian Git plan you were considering. The plugin's own README says it is "very unstable" on mobile and the maintainer does not recommend it there ([github.com/Vinzent03/obsidian-git](https://github.com/Vinzent03/obsidian-git)). The mobile leg is the whole point, so this fails on its own terms. Obsidian Local REST API, the usual agent bridge, is desktop-only too, which means the agent can only reach the vault when your desktop happens to be running.

## Tradeoffs table

Scores are shorthand: **good** / **ok** / **poor**. Costs are the personal-use figure as of 2026-08-31.

| Option | Agent write path | Agent read path | Mobile edit | Web + auth | Sharing | Cost | Friend setup | Lock-in | Offline |
|---|---|---|---|---|---|---|---|---|---|
| **Notion Free** | REST API with internal integration token, or MCP over OAuth | Same | good, native app | good, notion.com login | good, Publish + 10 guests | $0 | ~4 steps, 10 min | medium, exports MD/CSV | poor, cache only |
| **Notion Plus $10/seat/mo** | Same as Free | Same | good | good | good, unlimited guests | $10/mo | ~4 steps | medium | poor |
| **Notion Business $20/seat/mo** | Same, plus Custom Agents included | Same | good | good | good | $20/mo | ~4 steps | medium | poor |
| **Markdown/CSV in private GitHub repo** | `git commit` from Claude Code, or contents REST API | filesystem or API | ok, GitHub mobile edit+commit | good, github.com login | good, invite collaborator or make public | $0 | ~5 steps, 15 min | none, plain text | good |
| **Same, on Codeberg** | git push | filesystem | poor, responsive web only | good | good | $0 | ~5 steps | none | good |
| **Obsidian vault + Obsidian Git** | git commit | filesystem | **poor, plugin unstable on mobile** | none, no browser UI | ok, via the repo | $0 | ~8 steps | none | good |
| **Obsidian Sync** | none by itself | none | good, native app | none | ok, shared vaults | $4-8/mo | ~3 steps | none | good |
| **Obsidian Publish** | none | none | n/a, read surface | good, supports password | good, that is its job | $8-10/mo | ~3 steps | none | n/a |
| **Obsidian Local REST API + MCP** | REST/MCP into a running desktop Obsidian | same | poor, desktop-only server | none | none | $0 | ~7 steps | none | good |
| **Google Sheets** | Sheets API v4, service account or OAuth | same | good, native app | good, Google login | good, link sharing with roles | $0 | ~7 steps | low, CSV/XLSX export | ok |
| **Airtable Free** | REST API, **1,000 API calls/workspace/month** | same | good, native app | good | good, shared views | $0 | ~5 steps | medium | poor |
| **Baserow self-host** | REST API | same | poor, responsive web | good, self-run | ok | server cost only | ~4 Docker steps | low, MIT | poor |
| **NocoDB self-host** | REST API | same | poor, responsive web | good, self-run | ok | server cost only | ~4 Docker steps | low-med, non-OSI licence | poor |
| **Supabase Free** | PostgREST or official MCP | same | poor, you build the UI | good, built-in auth | ok, RLS | $0, **pauses after 1 week idle** | ~5 steps + build a UI | low, plain Postgres | poor |
| **Cloudflare Workers + D1** | you write the API yourself | same | poor, you build the UI | you build it | you build it | $0 within free limits | high, needs code | medium | poor |
| **Cloudflare KV** | you write the API | same | poor | you build it | you build it | $0, **1,000 writes/day** | high | low | poor |
| **Tiny SQLite + FastAPI on Fly/Railway** | your own API or direct file access | same | poor unless you build a UI | you build it | you build it | ~$2/mo Fly, $5/mo Railway | high, clone + deploy | none | poor |
| **Datasette** | read-only by default, needs write plugins | good, SQL over HTTP | poor | plugin-based auth | good, that is its strength | hosting cost, Cloud pricing unpublished | medium-high | none, SQLite | poor |
| **GitHub Issues as the log** | Issues REST API or `gh` | Issues REST API | ok, mobile app | good | good, public repo = public | $0 | ~3 steps | medium, JSON export | poor |
| **Logseq** | filesystem, files are markdown | filesystem | ok, native app | none | ok, via git | $0 app, sync $5-15/mo donation beta | ~6 steps | none | good |
| **Anytype** | local API, UNVERIFIED | UNVERIFIED | good, native app | none | UNVERIFIED | UNVERIFIED | UNVERIFIED | low, local-first | good |
| **SiYuan** | kernel HTTP API, UNVERIFIED | UNVERIFIED | ok, LAN browser mode confirmed, native app UNVERIFIED | self-host | ok | $0 local, $64 one-time PRO, $148/yr sub | ~6 steps | low | good |
| **AFFiNE** | UNVERIFIED | UNVERIFIED | ok | good, cloud login | ok, 3 members free | $0 free tier, ~$6.75-8.9/mo Pro | ~4 steps cloud | medium | good |
| **Trilium / TriliumNext** | ETAPI REST with token | ETAPI | ok, responsive frontend | good, self-run | ok, share feature exists | server cost only | ~6 Docker steps | low | good |
| **Nextcloud Notes** | REST API | REST API | good, native Android/iOS apps | good | good, Nextcloud file sharing | server or host cost, UNVERIFIED | ~8 steps self-host | none, markdown files | good |
| **wger self-host** | REST API, auth model UNVERIFIED | REST API | good, native apps | good, self-run | UNVERIFIED | server cost, `docker compose up -d` | ~4 steps | low, AGPL | ok |
| **Liftosaur** | **no public API found** | none | good | good | ok | free tier + paid | ~2 steps to use, self-host is AWS-hard | high without an API | good |
| **Hevy** | REST API **gated behind Hevy Pro** | same | good | good | good, social feed | Pro price UNVERIFIED, ~$3/mo circulating | ~3 steps | high | good |
| **Strong** | **none, CSV export only, no re-import** | CSV export | good | poor | poor | app price not checked | ~2 steps | high | good |

## Notion plan gating, the four questions

I pulled `https://www.notion.com/pricing` as raw HTML on 2026-08-31 and parsed the comparison grid rows directly, because the rendered summary a fetch tool produces gets the checkmark columns wrong. Column order was confirmed against known-different rows: File uploads reads `Up to 5 MB / Unlimited / Unlimited / Unlimited` and External guest limit reads `10 / Unlimited / Unlimited / Unlimited`, so the columns are Free, Plus, Business, Enterprise.

Current prices on that page: Free $0, Plus $10 per member/month, Business $20 per member/month, Enterprise custom ([notion.com/pricing](https://www.notion.com/pricing)). **No tier costs $24.** The $24 figure matches nothing Notion currently sells.

### 1. Public API / internal integrations

**Available on Free.** The `Public API` grid row is a checkmark on all four plans, as is `Webhooks` ([notion.com/pricing](https://www.notion.com/pricing), parsed 2026-08-31).

Notion supports three auth models for the same REST API: internal connections with a static token, public connections over OAuth 2.0, and personal access tokens for scripts and CLI workflows ([developers.notion.com/guides/get-started/overview](https://developers.notion.com/guides/get-started/overview)). Only workspace owners can reach the Connections tab and create an integration ([notion.com/help/create-integrations-with-the-notion-api](https://www.notion.com/help/create-integrations-with-the-notion-api)), which is a non-issue in your own workspace.

Rate limits: about 3 requests per second per connection, plus a per-workspace limit "scaled to the workspace's plan," and a 1,000-block / 500 KB payload cap ([developers.notion.com/reference/request-limits](https://developers.notion.com/reference/request-limits)). The workspace-level limit is the one place your plan does affect API throughput, and Notion does not publish the numbers.

### 2. Notion MCP at mcp.notion.com

**No plan gate stated anywhere I could find.** The endpoints are `https://mcp.notion.com/mcp` (Streamable HTTP) and `https://mcp.notion.com/sse` (SSE fallback), authenticated by OAuth ([developers.notion.com/docs/get-started-with-mcp](https://developers.notion.com/docs/get-started-with-mcp)). Neither that page, [developers.notion.com/docs/mcp](https://developers.notion.com/docs/mcp), nor [notion.com/help/notion-mcp](https://www.notion.com/help/notion-mcp) mentions plans, Notion AI, or credits. The string "MCP" does not appear anywhere in the pricing page HTML.

One catch that matters for unattended agents: "Notion MCP currently requires you to complete the OAuth authorization flow," and non-interactive authorization is not supported ([developers.notion.com/docs/get-started-with-mcp](https://developers.notion.com/docs/get-started-with-mcp)). So MCP is fine for interactive Claude sessions, and the REST API with an internal integration token is the right path for a cron job or a GitHub Action.

Your session's data point fits this. `workspace_search` is the plain search path and needs no AI entitlement; `ai_search` would be the Notion-AI-backed one. UNVERIFIED: I found no Notion doc naming those two modes, so the read that `ai_search` is the AI-gated variant is inference from the tool's own response, not a cited fact.

### 3. Notion AI

**Gated.** `Notion Agent (chat, generate, autofill, translate)` reads `Limited Trial / Limited Trial / checkmark / checkmark`, so full Notion AI starts at Business ($20/seat/mo). `Custom Agents` is blank on Free and Plus, checkmark on Business and Enterprise. `Workers (Beta)` is blank on Free and Plus ([notion.com/pricing](https://www.notion.com/pricing)).

Notion credits, which power Custom Agents, "are only available on Business and Enterprise plans" ([notion.com/help/buy-and-track-notion-credits-for-custom-agents](https://www.notion.com/help/buy-and-track-notion-credits-for-custom-agents)), at roughly $10 per 1,000 credits.

**None of this is needed for your use case.** You want *Claude* writing to Notion, not Notion's own AI. Notion AI and the API are separate products with separate gates, and that distinction is almost certainly where the $24/mo belief came from.

### 4. The claude.ai Notion connector

Notion is one of the listed web connectors, and "Web connectors are available for all users on Claude, Cowork, Claude Desktop, and Claude Mobile (iOS and Android)" ([support.claude.com/en/articles/11176164](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)). Connectors write as well as read; that page's own examples include creating Linear issues and sending Slack messages, and connector permissions can be set per action to Always allow, Needs approval, or Blocked.

Custom connectors, meaning your own remote MCP server rather than a directory one, work on "Free, Pro, Max, Team, and Enterprise plans," with Free limited to one custom connector ([support.claude.com/en/articles/11175166](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)). Installing connectors on mobile is flagged as beta; desktop and web are the primary path for setting them up, after which they sync.

### Verdict

Read and write to Notion from an agent costs $0. Your current plan is not the blocker it was assumed to be.

## Notes on the options that need them

### The Obsidian cluster

Obsidian itself is free with no signup and no time limit; the $50/user/year commercial licence is optional and not required even for work use ([obsidian.md/pricing](https://obsidian.md/pricing)).

The Obsidian Git plugin works, but its README is blunt about mobile: "very unstable... I would not recommend using this plugin on mobile." No SSH auth on mobile, HTTPS only, no rebase, no submodules, and it can crash on clone or pull of a large repo ([github.com/Vinzent03/obsidian-git](https://github.com/Vinzent03/obsidian-git)). That is the plan you were considering, and mobile is the leg it breaks on.

Obsidian Sync is $4/mo annual or $5/mo monthly for Standard (1 vault, 1 GB), $8/mo annual or $10/mo monthly for Plus (10 vaults, 10 GB) ([obsidian.md/sync](https://obsidian.md/sync)). It solves phone sync but gives an agent nothing.

Obsidian Publish is $8/mo annual, $10/mo monthly, up to 4 GB, and it does support password protection, so it is not public-only ([obsidian.md/publish](https://obsidian.md/publish)). Good sharing surface, still no agent write path.

The Local REST API plugin is the usual agent bridge and it is genuinely good: full CRUD, targeted PATCH edits, JsonLogic search, and it now ships its own MCP endpoint at `/mcp/`. Auth is an API key plus a locally generated CA cert over `127.0.0.1:27124` ([github.com/coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api)). It binds to localhost inside a running Obsidian, so the agent can only reach your vault when your desktop is awake and Obsidian is open. For a phone-first log that is fatal.

Third-party Obsidian MCP servers split into two shapes: ones that go through the Local REST API plugin, such as [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian), and ones that read the vault directly off disk, such as [lstpsche/obsidian-mcp](https://github.com/lstpsche/obsidian-mcp) and [StevenStavrakis/obsidian-mcp](https://github.com/StevenStavrakis/obsidian-mcp). The direct-filesystem ones work headless. This corner of GitHub is churning; new repos appeared within a day of this research, so treat any pick as a moving target.

### The git-native runner-up

GitHub Free includes unlimited private repositories ([github.com/pricing](https://github.com/pricing)). The GitHub mobile app can edit a file and commit it: the docs list "Edit files in pull requests," and the changelog for editing from Browse Code says you can "Commit changes to code within your repo, create new branches and put up a new pull request to land those quick changes on-the-go" ([docs.github.com/en/get-started/using-github/github-mobile](https://docs.github.com/en/get-started/using-github/github-mobile), [github.blog changelog](https://github.blog/changelog/2022-11-15-github-for-ios-edit-files-from-browse-code/)). It works. It is slower than typing into a Notion database row, and typing a set-by-set log in a mobile code editor is not fun.

Codeberg is free and its Terms of Use allow private repos for "really small & personal stuff like your journal, config files, ideas or notes, but explicitly not as a personal cloud or media storage" ([Codeberg ToU](https://codeberg.org/Codeberg/org/raw/branch/main/TermsOfUse.md)). A workout log fits that carve-out. There is no first-party Codeberg mobile app that surfaced in any source checked, which pushes phone editing onto the responsive web UI.

GitHub Actions gives 2,000 free minutes a month, and those run on private repos ([GitHub Actions billing docs](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)). A push-triggered workflow on a personal log fits inside that comfortably.

### Databases and spreadsheets

Google Sheets is a strong dark horse. Native mobile app, real link sharing with viewer and editor roles ([support.google.com/docs/answer/2494822](https://support.google.com/docs/answer/2494822)), and the Sheets API v4 for the agent ([quickstart](https://developers.google.com/workspace/sheets/api/quickstart/nodejs)). The cost is setup friction: a GCP project, an enabled API, and service-account or OAuth credentials. There is no official Google Sheets MCP server, only community ones such as [domdomegg/google-sheets-mcp](https://github.com/domdomegg/google-sheets-mcp).

Airtable Free is disqualified by one number: **1,000 API calls per workspace per month** ([support.airtable.com/docs/airtable-plans](https://support.airtable.com/docs/airtable-plans)), about 33 a day. Also 1,000 records per base. An agent that reads before it writes burns that fast.

Supabase Free gives 500 MB of Postgres, unlimited API requests, and built-in auth, but **free projects pause after one week of inactivity** ([supabase.com/pricing](https://supabase.com/pricing)). Miss two weeks of the gym and your log is asleep. Its own MCP docs also warn "never connect the MCP server to production data" over prompt-injection risk ([supabase.com/docs/guides/getting-started/mcp](https://supabase.com/docs/guides/getting-started/mcp)).

Cloudflare's free tier is generous on paper: 100,000 Worker requests/day, D1 at 5 million rows read and 100,000 rows written per day, 5 GB storage ([Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/), [D1 pricing](https://developers.cloudflare.com/d1/platform/pricing/)). KV is stingier at 1,000 writes/day ([KV limits](https://developers.cloudflare.com/kv/platform/limits/)). Cloudflare's official MCP server manages your Cloudflare account, not your app's data ([github.com/cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)), so you would still write the data API yourself. That is the whole problem with this branch: you are building an app, and you already tried that with Jim.

Fly.io's pricing page shows no ongoing free allowance now, only a trial; cheapest always-on is shared-cpu-1x/256MB at $0.0028/hr, about $2.02/month ([fly.io/docs/about/pricing](https://fly.io/docs/about/pricing/)). Railway's floor is the $5/month Hobby plan after a one-time $5 30-day trial credit ([railway.com/pricing](https://railway.com/pricing)).

Baserow self-hosted is MIT and installs with one `docker run` ([baserow.io docs](https://baserow.io/docs/installation%2Finstall-with-docker)). NocoDB self-hosted is free forever on the community edition under a Sustainable Use License, with cloud from $12/user/month ([nocodb.com/pricing](https://nocodb.com/pricing)). Neither has a native mobile app, so phone editing is responsive web.

Datasette is read-only by default; writes need canned queries configured with `"write": true` or plugins ([docs.datasette.io authentication](https://docs.datasette.io/en/stable/authentication.html)). Datasette Cloud publishes no pricing at all, only a demo request form (checked [datasette.cloud](https://www.datasette.cloud/), 2026-08-31).

### Fitness-specific apps

wger is AGPL-3.0 and self-hosts with `docker compose up -d`, has a REST API, and ships native Android and iOS apps ([wger.readthedocs.io](https://wger.readthedocs.io/en/latest/), [github.com/wger-project/wger](https://github.com/wger-project/wger)). It is the best of this cluster and the one worth a second look if you want domain structure rather than free-form notes. The hosted wger.de instance could not be checked; it sits behind an Anubis bot-protection wall. UNVERIFIED: the API's auth model.

Hevy's public API exists at api.hevyapp.com but is gated behind Hevy Pro, and the Pro price could not be confirmed from a primary source (the pricing page is a JS shell and the help-center article returns 403). Figures circulating on secondary sites cluster around $3/mo, which the brief forbids me from treating as verified.

Liftosaur is AGPL-3.0 ([github.com/astashov/liftosaur](https://github.com/astashov/liftosaur)) but has no documented public API, and full self-hosting needs AWS Lambda, DynamoDB, S3 and CDK edits. No agent path.

Strong offers CSV export only, and exported files cannot be re-imported ([help.strongapp.io/article/235-export-workout-data](https://help.strongapp.io/article/235-export-workout-data)). No API. Dead end for an agent.

## How the phone triggers an agent

Ranked by how little you have to build.

1. **Claude mobile app with a connector.** Web connectors work on iOS and Android for all users ([support.claude.com/en/articles/11176164](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)). You talk to Claude, Claude writes to Notion. Zero infrastructure. This is the path that makes Notion win.
2. **Claude Code on the web.** "Run Claude Code in the cloud from your browser or phone. Connect a GitHub repository, submit a task, and review the PR without local setup." Available on Pro, Max and Team ([code.claude.com/docs/en/web-quickstart](https://code.claude.com/docs/en/web-quickstart)). This is what makes the git option viable from a phone. The same docs mention Routines, which run "on a schedule, via API call, or in response to GitHub events," which is the clean way to have a phone commit kick off an agent.
3. **GitHub Actions on push.** Free within 2,000 minutes/month on private repos. Commit from the mobile app, workflow fires, agent tidies up.
4. **A Telegram or Discord bot.** Both bot APIs are free. Most flexible, most to build and maintain. UNVERIFIED this session: I did not re-fetch either bot API doc.
5. **Direct Anthropic API from a small script.** Pay per token. UNVERIFIED: current per-token rates were not re-fetched from [anthropic.com/pricing](https://www.anthropic.com/pricing) during this research.

## Friend replicates it

### Option 1, Notion. 6 steps, about 15 minutes.

1. Sign up for a free Notion account at [notion.com](https://www.notion.com/pricing).
2. Duplicate your shared workout-log template into their workspace. One click from a published page.
3. In the Claude mobile or web app, open connector settings and connect Notion. OAuth, no keys to copy ([support.claude.com/en/articles/11176164](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)).
4. Grant the connector access to the workout-log page.
5. Optional, for unattended scripts: as workspace owner, open Settings, Connections, and create an internal integration; copy the token ([notion.com/help/create-integrations-with-the-notion-api](https://www.notion.com/help/create-integrations-with-the-notion-api)). Share the workout page with that integration.
6. Optional, for sharing with a coach or friend: Publish the page to web. Unlimited published pages on Free ([notion.com/pricing](https://www.notion.com/pricing)).

Steps 1 to 4 are the working minimum: **4 steps, about 10 minutes**, and no command line at any point. That is the number that decides this.

### Option 2, markdown in a private GitHub repo. 7 steps, about 25 minutes.

1. Create a free GitHub account. Private repos are unlimited on Free ([github.com/pricing](https://github.com/pricing)).
2. Create a private repo from your template, with the log file layout and a README explaining the format.
3. Install the GitHub mobile app, sign in.
4. Confirm the edit-and-commit flow: open the log file, Edit File, commit ([docs.github.com/en/get-started/using-github/github-mobile](https://docs.github.com/en/get-started/using-github/github-mobile)).
5. Install Claude Code locally, or use Claude Code on the web and connect the repo ([code.claude.com/docs/en/web-quickstart](https://code.claude.com/docs/en/web-quickstart)). Note the web path needs a Claude Pro, Max or Team plan, so this is not free for the friend if they lack one.
6. Optional: add a GitHub Action on push if you want an agent to react automatically. Free within 2,000 minutes/month.
7. Optional: share by adding a collaborator, or flip the repo public.

**Real cost of this option:** step 5 is where a non-technical friend falls off. It is 7 steps but two of them assume comfort with a terminal or a paid Claude plan.

## Open questions for the user

I could not ask these mid-task, so they are recorded here.

1. **How do you actually log, at the gym or after?** Set-by-set during the session needs a fast structured input, which is Notion database rows or a fitness app. A dictated summary afterwards works fine as markdown. This changes the answer more than any pricing detail does.
2. **What does "shared with others" mean concretely?** A read-only link to a coach, a friend who edits too, or a public page? Free Notion caps external guests at 10 but allows unlimited published pages. Public GitHub repos are all-or-nothing.
3. **Does the agent need to run unattended,** for example a nightly summary, or only when you talk to it? Unattended rules out Notion MCP, which requires interactive OAuth, and points at the REST API with an internal token instead.
4. **Is structured data worth losing free-form notes?** Notion databases and wger give you queryable sets, reps and weights. Markdown gives you "felt awful today, dropped to 3x8." You can fake either in the other, badly.
5. **What happens to the "Jim" app you built?** If the plan is to come back to it, Supabase or Cloudflare D1 become more attractive as a shared backend, and Notion becomes a stopgap you will have to migrate off.
6. **How much does lock-in actually bother you?** Notion exports to Markdown and CSV on every plan, but exports as blocks, not as your file layout. Git gives you exactly the bytes you wrote.
7. **Do you have or want a paid Claude plan?** Claude Code on the web needs Pro, Max or Team. The Notion connector does not. That difference decides whether the runner-up is free for a friend.

## Gaps and UNVERIFIED claims

- Notion's per-workspace API rate limit is stated to scale with plan, but the numbers are unpublished ([developers.notion.com/reference/request-limits](https://developers.notion.com/reference/request-limits)).
- The `workspace_search` versus `ai_search` distinction is inferred from tool output this session, not from any Notion doc.
- Hevy Pro's price: pricing page is a JS shell, help-center article returns 403. Not verified.
- wger.de hosted instance and the wger API's auth model: blocked by bot protection.
- Anytype pricing, self-host and local API: pricing page is a client-rendered app that returns no figures; the API doc URL 404s. Entirely unverified.
- SiYuan's kernel HTTP API and native mobile app: not confirmed from a fetched page. Prices are confirmed ([b3log.org/siyuan/en/pricing.html](https://b3log.org/siyuan/en/pricing.html)).
- AFFiNE lists both $6.75/mo and $8.9/mo for Pro on the same page without clear billing-cadence labels ([affine.pro/pricing](https://affine.pro/pricing)). Its self-host seat rules and API/MCP story are unchecked.
- Trilium's mobile story is a "Mobile Frontend" doc page, so probably responsive web rather than a native app; not resolved ([triliumnext.github.io/Docs](https://triliumnext.github.io/Docs/)). ETAPI is confirmed ([etapi docs](https://triliumnext.github.io/Docs/Wiki/etapi.html)).
- Nextcloud hosting cost: no pricing source checked. The software is free ([github.com/nextcloud/notes](https://github.com/nextcloud/notes)).
- Logseq's post-beta Sync price is not published anywhere found; the beta is $5 or $15/mo via Open Collective ([blog.logseq.com](https://blog.logseq.com/how-to-setup-and-use-logseq-sync/)).
- Datasette Cloud pricing is genuinely unpublished, not a fetch failure.
- Airtable paid-tier prices, native mobile app details, and the scope of [Airtable/airtable-mcp-cli](https://github.com/Airtable/airtable-mcp-cli) were not checked.
- Codeberg and Forgejo native mobile apps: none surfaced, but no official statement confirms their absence.
- Google Sheets mobile offline behaviour and "free with a personal account" were treated as common knowledge, not confirmed against a Google pricing page.
- Telegram and Discord bot APIs, and current Anthropic per-token pricing, were not re-fetched this session.
- The web search budget for this session ran out partway through, so a few of the above gaps could not be chased further.
