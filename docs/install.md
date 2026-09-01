# Install the workout trainer

By the end you have four Notion databases in your own workspace, a program, and
one logged set. Pick one flavour. Flavour A needs a terminal, a PC that stays
on, and a paid Claude plan. Flavour B runs on a free claude.ai account.

Both flavours start the same way: create a free Notion account and one blank
page. The agent builds everything inside that page.

No step below has run against a live Notion workspace yet. Every proof in this
repo is an offline replay (`docs/architecture.md`), so treat your first run as
the first real test.

## Flavour A: Claude Code plugin

1. Open Claude Code in the terminal and add the marketplace.

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

   `intake` creates `Sessions`, `Exercises`, `Locations`, and `Sets`, then starts
   the PAR-Q+ health questions, one per turn. It tells you the catalog seeding
   runs for about 5 minutes in the background.

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

2. Connect Notion under your connector settings and sign in. There are no API
   keys to paste.

3. Get the skills ZIP. Download it from the repo:

		dist/workout-trainer-skills.zip

   Or clone the repo and rebuild it:

		make skills

4. Go to **Customize > Skills**, click `+`, then **Create skill**, then
   **Upload a skill**, and upload the ZIP.

5. In Notion, give the Claude connector access to your blank page.

6. Start a new chat and run setup.

		set me up

   Same result as flavour A: four databases, then the health questions, with the
   catalog seeding in the background.

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

**Setup sits on the catalog for minutes.** Notion Free allows roughly 3 requests
per second and the catalog is 913 rows. Answer the profile questions while it
seeds.

**You ran "set me up" twice.** Nothing is duplicated. `intake` queries before it
creates, so a database of that name under your page is adopted, not rebuilt.

**claude.ai rejects the ZIP (unverified).** The upload is documented for a single
skill folder, and this ZIP holds seven at the root. If it is refused, zip each
folder under `.claude/skills/` on its own and upload seven skills.
