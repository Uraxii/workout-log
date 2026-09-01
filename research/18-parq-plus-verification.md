# PAR-Q+ verification against the published form

Written 2026-09-01, for R17 (bd `workout-log-1z9`). Verifies
`.claude/skills/screen/references/parq-plus.md` against the current
published PAR-Q+ form. `screen.py` parses its seven questions from that
file and a fixture harness now pins the file byte for byte, so any wording
error in it is now locked in as "correct."

## Primary source

- PDF: https://eparmedx.com/wp-content/uploads/2025/01/PARQPlus2025Fillable.pdf
- Publisher: PAR-Q+ Collaboration, hosted at eparmedx.com, the group's own site
- Edition printed on every page footer: copyright 2025 PAR-Q+ Collaboration, form dated 01-11-2024
- Fetched 2026-09-01 by direct download (`curl`), sha256 `650300c7aab171e812e98b6c95b63358b2fadf5fb79afdbb22ec2ea5a7ca576f`
- Stored in the project kb: `.kb/sources/650300c7aab171e812e98b6c95b63358b2fadf5fb79afdbb22ec2ea5a7ca576f.pdf`, provenance sidecar `.toml` alongside it

Note on the sidecar: `llmwiki ingest` cannot fetch a PDF by URL directly
(the CLI rejects `content_type: application/pdf`), so the file was
downloaded to a local temp path and ingested from there. The sidecar's
`url` field records that local path, not the eparmedx.com URL. The raw
bytes and sha256 above are the real provenance; this file is the record
of the true source URL. Automatic summarization of the PDF also failed
(the CLI reads sources as UTF-8 text and the PDF is binary) — see
`.kb/log.md`, `[summarize] 650300c7...: dropped (cannot read source:
'utf-8' codec can't decode byte 0xe2...)`. That is a known limitation
of the kb tool with binary sources, not a problem with the source
itself; the bytes and sidecar are stored regardless, per the tool's own
contract ("ingest stores the raw bytes, writes provenance" happens before
summarization is attempted).

Text was extracted with `pdftotext -layout` and checked by hand against
the PDF's own page layout and question numbering.

## Per-question verdict: all seven match, verbatim

| # | `parq-plus.md` | Published PDF | Verdict |
|---|---|---|---|
| 1 | "Has your doctor ever said that you have a heart condition OR high blood pressure?" | Same. (PDF places the checkbox mid-line before the closing "?"; the printed words are identical.) | Match |
| 2 | "Do you feel pain in your chest at rest, during your daily activities of living, OR when you do physical activity?" | Same | Match |
| 3 | "Do you lose balance because of dizziness OR have you lost consciousness in the last 12 months? Please answer NO if your dizziness was associated with over-breathing (including during vigorous exercise)." | Same | Match |
| 4 | "Have you ever been diagnosed with another chronic medical condition (other than heart disease or high blood pressure)?" | Same question text. The PDF appends a field label, "PLEASE LIST CONDITION(S) HERE:", which is a form-input prompt, not part of the question sentence. | Match |
| 5 | "Are you currently taking prescribed medications for a chronic medical condition?" | Same question text, PDF appends "PLEASE LIST CONDITION(S) AND MEDICATIONS HERE:" (same field-label pattern as Q4) | Match |
| 6 | "Do you currently have (or have had within the past 12 months) a bone, joint, or soft tissue (muscle, ligament, or tendon) problem that could be made worse by becoming more physically active? Please answer NO if you had a problem in the past, but it does not limit your current ability to be physically active." | Same, PDF appends the same field-label pattern | Match |
| 7 | "Has your doctor ever said that you should only do medically supervised physical activity?" | Same | Match |

No wording differs anywhere in the seven questions. `parq-plus.md`
correctly omits the "PLEASE LIST..." field-label lines on Q4-6: those are
paper-form input prompts, not question text, and `screen.py` collects the
condition name through its own follow-up turn instead.

The outcome quotes in `parq-plus.md` are real PDF words, but one is
attributed to the wrong branch of the form (caught on cross-review, not
in the first pass):

- "you are cleared for physical activity... start slowly and build up gradually" is page 1's all-NO outcome, correctly elided.
- The 12-month expiry quote ("valid for a maximum of 12 months from the date it is completed and becomes invalid if my condition changes") matches the PDF's participant declaration word for word, page 1.
- The licence quote ("You are encouraged to photocopy the PAR-Q+. You must use the entire questionnaire and NO changes are permitted.") matches the PDF word for word, page 4 (`pdftotext` line 202, between the "3/4" and "4/4" footers). An earlier draft of this file misplaced it on page 3.
- **Misattributed**: `parq-plus.md`'s "Any YES, no clinician clearance yet" bullet quotes "you should seek further information before becoming more physically active... visit a qualified exercise professional." That sentence is real PDF text, but it is page 4's outcome for a YES on the *follow-up* questions (pages 2-3), not the outcome for a YES on the seven general questions. Page 1's actual instruction for a general YES is simply "COMPLETE PAGES 2 AND 3" (`pdftotext` line 46). `parq-plus.md` never quotes that line; it reaches past the entire follow-up tree and borrows the page-4 advisory as a stand-in for "any YES, unconfirmed." The quoted words are accurate, but the branch they are attached to in `parq-plus.md`'s model does not exist in the source in that shape. This is the same flattening described below, seen from the wording side rather than the structure side: because `screen` never asks the follow-up tree, it has nothing of its own to quote for that gate, and reaches for the page-4 line instead.

Also missing from `parq-plus.md`, found on cross-review: the all-NO
branch on page 1 carries a conditional caveat ("If you are over the age
of 45 yr and NOT accustomed to regular vigorous to maximal effort
exercise, consult a qualified exercise professional before engaging in
this intensity of exercise") and three "delay becoming more active"
conditions (temporary illness, pregnancy, a health change since
completing the form). None of the three delay conditions appear in
`parq-plus.md` or in `screen.py`'s logic; the 45yr+ caveat is likewise
absent. `clearance = cleared` on all-seven-NO is written flat, with no
path for these. Whether that is in scope for `screen`'s deliberately
narrow chat flow is a product call, not a wording defect, but it was not
in this file's first-pass findings and belongs alongside the follow-up
flattening below.

## Follow-up structure verdict: flattened

The published form's actual follow-up is not one line. Pages 2 and 3 are
a branching tree keyed to which of the seven general questions got a YES:

- Ten condition categories, each gated by its own question (1 arthritis/osteoporosis/back, 2 cancer, 3 heart or cardiovascular, 4 blood pressure, 5 metabolic, 6 mental health or learning, 7 respiratory, 8 spinal cord injury, 9 stroke, 10 any other condition or two-or-more conditions).
- Each category asks 2-4 sub-questions (labelled 1a-1c, 2a-2b, 3a-3d, and so on), each its own YES/NO, gated by "if NO, go to question N+1."
- Page 4 gives one of two outcomes depending on whether *any* sub-question anywhere was YES, not depending on which general question started the branch.

`parq-plus.md`'s "Follow-up" section replaces all of that with a single
invented line: "`screen` asks one follow-up line per YES: name the
condition, and say whether a clinician has already cleared exercise, with
a date." That line is not presented as a quote from the form (correctly:
it is not one), so this is not a wording defect against the acceptance
criteria's "differs" trigger. But it is a real flattening: the published
follow-up is a per-condition question tree that routes to ePARmed-X+ or a
professional, and `screen`'s replacement is a single ad hoc question that
never appears in the source. The form's own text for a YES never asks
about prior clinician clearance; that criterion is `screen`'s own
invention layered on top of the PAR-Q+ result, not a PAR-Q+ requirement.

Decision T3 (`research/00-synthesis-trainer.md:538`: "Verbatim, but
split: 7 questions at first run, follow-ups only on a YES. It is one
heavy interaction once a year") scopes the word "verbatim" to the seven
questions, not the follow-up pages, and does not itself say anything
about *how* the follow-up should be asked. That is weaker support than a
first pass of this file gave it credit for: T3 says *when* a follow-up
fires, not that a one-line stand-in is an acceptable replacement for the
form's own branching tree. `research/07-baselining-and-assessment.md` s2
field A2 frames the follow-up as routing out to the real tool ("Follow-ups
if any YES ... Routes to ePARmed-X+ or a clinician"), which is closer to
"hand the client to eparmedx.com" than to "ask one improvised question and
call it referred." Read this way, the flattening is plausible as an
intentional scope cut for a chat product, but it is not something T3 or
A2 explicitly signs off on. That is a call for whoever owns `screen`'s
design, not something this verification can settle on the wording alone.

## Licensing and attribution verdict: one open question worth a maintainer call

Confirmed licence text, PDF page 3: "You are encouraged to photocopy the
PAR-Q+. You must use the entire questionnaire and NO changes are
permitted." No separate "you must display this credit line in your
product" clause was found; the citation block on page 4 (Warburton DER,
Jamnik VK, Bredin SSD, and Gledhill N, *Health & Fitness Journal of
Canada* 4(2):3-23, 2011) is the form's suggested academic citation, which
this repo already reproduces in both `parq-plus.md` and
`research/07-baselining-and-assessment.md`.

The open question is what "the entire questionnaire, NO changes are
permitted" covers. Read narrowly, it governs photocopying the paper form
and does not reach a chat product that asks the same seven questions in
the same words. Read broadly, it could mean any reproduction of the
instrument has to carry all of it unmodified, in which case replacing the
follow-up pages with `screen`'s own one-line triage (verdict above) is a
change to "the questionnaire" as a whole, not just an implementation
shortcut. Nothing in the form resolves which reading is intended, and
this is a legal judgment call, not a wording check. It is a shipping
concern precisely because build-plan section 6 says "the repo is public."

## What this does and does not trigger

- Seven questions: verbatim match, no wording differs anywhere. Per this
  ticket's acceptance criteria, that means no fix ticket is filed — the
  trigger is wording differing, and none does.
- Follow-up flattening and the licence question above are real findings,
  not wording defects. They are recorded here and in the resolution
  comment on `workout-log-1z9` as flagged follow-ups for a maintainer to
  decide on, not filed as a ticket, since opening one was outside this
  ticket's scoped trigger.
