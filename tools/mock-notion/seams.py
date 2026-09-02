"""Which turn function each `@skill` in a transcript routes to.

One skill-side seam per row. Each is a pure function of `(line, state)`
returning `{"writes", <say key>, "state"}`; the say key differs because
`session-runner` names its user-facing line `confirm_line`
(docs/architecture.md "The script seam"). Importing them needs one
`sys.path` entry per skill, since a skill directory is not a package.
"""

from __future__ import annotations

import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[2] / ".claude" / "skills"

sys.path.insert(0, str(SKILLS_DIR / "session-runner" / "scripts"))
import log_set  # noqa: E402  (skill-side seam, phase 1 has one script)

sys.path.insert(0, str(SKILLS_DIR / "screen" / "scripts"))
sys.path.insert(0, str(SKILLS_DIR / "intake" / "scripts"))
import screen  # noqa: E402  (phase 5 seam)
import intake  # noqa: E402  (phase 5 seam)

sys.path.insert(0, str(SKILLS_DIR / "trainer-core" / "scripts"))
sys.path.insert(0, str(SKILLS_DIR / "pain-triage" / "scripts"))
import trainer_core  # noqa: E402  (phase 6 seam)
import pain_triage  # noqa: E402  (phase 6 seam)

sys.path.insert(0, str(SKILLS_DIR / "program-design" / "scripts"))
import design  # noqa: E402  (phase 4 seam)

sys.path.insert(0, str(SKILLS_DIR / "load-adjust" / "scripts"))
import load_adjust  # noqa: E402  (phase 6 seam)

SEAMS = {
    "session-runner": (log_set.log_set, "confirm_line"),
    "intake": (intake.intake_turn, "say"),
    "screen": (screen.screen_turn, "say"),
    "trainer-core": (trainer_core.gate_turn, "say"),
    "pain-triage": (pain_triage.triage_turn, "say"),
    "program-design": (design.design_turn, "say"),
    "load-adjust": (load_adjust.adjust_turn, "say"),
}
