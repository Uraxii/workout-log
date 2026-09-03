# Install the workout trainer

By the end you have four Notion databases in your own workspace, a program, and
one logged set. Pick one flavour. Flavour A needs a terminal, a PC that stays
on, and a paid Claude plan. Flavour B runs on a free claude.ai account.

## Read this before you start

No step below has run against a live Notion workspace. Every proof in this repo
is an offline replay (`docs/architecture.md`), so treat your first run as the
first real test.

## Set up Notion first, either flavour

1. Create a free Notion account.

2. Create one blank Notion page. The agent builds all four databases inside
   this page.

3. Copy the page link and keep it. Click **Share**, then **Copy link**. You
   need the page id from that link, which is the long string of letters and
   digits at the end, before any `?`.

There are no API keys and no tokens to paste, in either flavour. Both sign in
to Notion in a browser instead.

## Flavour A: Claude Code plugin

1. Open Claude Code in the terminal and add the marketplace. The repo is
   private, so your GitHub account must be able to read it.

		/plugin marketplace add Uraxii/workout-log

2. Install the plugin. The marketplace is named `uraxii-plugins`.

		/plugin install workout-trainer@uraxii-plugins

3. Approve the `notion` MCP server when Claude Code asks. The plugin declares it
   in `.mcp.json` as the HTTP server at `https://mcp.notion.com/mcp`. Sign in to
   Notion in the browser window it opens.

4. In Notion, give that connection access to your blank page. Nothing works
   until the connection can see the page.

5. Start setup.

		set me up

   `intake` asks three questions about the tool before anything about you.

   It asks where to keep your training log first. Answer `notion`. Name
   anything else and it says it can't write there yet, records what you
   named, and creates nothing.

   Next it asks for the page: paste the link you copied in step 3, or the
   bare page id. Dashed or undashed, any case, both work.

   Last it asks your timezone, as an IANA name like `America/Los_Angeles`.

   `intake` creates `Exercises`, `Locations`, `Sessions`, and `Sets`, one
   database per turn, then starts the PAR-Q+ health questions, one per turn. It
   tells you the catalog seeding runs for about 5 minutes in the background.

6. Ask for a program.

		make me a plan

   `program-design` names the template it picked from `library/`, says why, and
   writes it to `program/current`.

7. Log your first set. Type the lift, then the numbers.

		bench 135x5

		60kg 3x8

		ohp 95 8/8/6

   The agent says a confirm line back and writes one row per set to `Sets`. Open
   the `Sets` database in Notion to see them.

## Flavour B: claude.ai ZIP upload

1. Go to **Settings > Capabilities** on claude.ai and turn on code execution.
   Skills do not run without it.

2. Connect Notion under your connector settings and sign in.

3. Build the skills ZIP yourself. There is nothing to download: `dist/` is
   gitignored (`.gitignore:18`), the repo publishes no release, and no workflow
   builds one. Clone the repo, then run:

		make skills

   That writes the file you upload in the next step:

		dist/workout-trainer-skills.zip

4. Go to **Customize > Skills**, click `+`, then **Create skill**, then
   **Upload a skill**, and upload the ZIP.

5. In Notion, give the Claude connector access to your blank page.

6. Start a new chat and run setup.

		set me up

   Same three questions first as flavour A: where to keep the log (answer
   `notion`), the page link or id, then your timezone. Same result after
   that: four databases, then the health questions, with the catalog
   seeding in the background.

7. Ask for a program.

		make me a plan

8. Log your first set.

		squat 225x5x3

		pullup bw+25

		135 5/5/4

   The agent confirms each line and writes the rows to `Sets`.

## Troubleshooting

**It refuses to log and names a missing precondition.** `trainer-core` blocks
every session until `screen` has recorded a clearance and `program/current`
exists. Finish "set me up", then "make me a plan".

**Every reply says `Status: halted`.** You reported pain, so `pain-triage`
halted the session. Only `pain-triage` clears it, and only after you
acknowledge the hand-off it gave you.

**It says it can't write to the store you named.** You answered the first
setup question with something other than `notion`. It records what you named
and creates nothing: no database, no catalog seed. Reply `notion` and setup
continues from the same question.

**Setup sits on the catalog for minutes.** Notion paces each connection to an
average of 3 requests per second, on every plan, and the catalog is 913 rows.
The limit that scales with your plan is a separate per-workspace one, and Notion
does not publish its numbers (`research/01-storage-options.md:61`,
`research/19-notion-database-create-api.md`). Answer the profile questions while
the catalog seeds.

**You ran "set me up" twice.** Nothing is duplicated. `intake` queries before it
creates, so a database of that name under your page is adopted, not rebuilt.

**claude.ai rejects the ZIP.** Nobody has tried this upload yet. The claude.ai
docs describe uploading one skill folder, and this ZIP holds seven folders at
the root. There is no fallback. Uploading each folder on its own does not work,
because `intake` imports `screen` and `load-adjust` imports `loads` from
`program-design`, so a lone folder fails at import with a
`ModuleNotFoundError`. Ticket `workout-log-ayf.14` holds the reproduction. Use
flavour A until that is settled.
