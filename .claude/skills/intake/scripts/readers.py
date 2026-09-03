"""How one chat line turns into one field's value.

Split out of `questions.py` (house limit, docs/architecture.md "One script
per skill" splits by DOMAIN): reading a value out of a line is one body of
knowledge, and the ordered table of what gets asked, in what order, is
another.

Every reader returns `None` for the line that does not answer its field,
which is the whole re-ask rule (ticket workout-log-481): `None` is never a
value and never a default, and the caller re-enters the step instead of
advancing past it.
"""

from __future__ import annotations

import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def free_text(line: str) -> str | None:
    return line.strip() or None


_PAGE_ID_RE = re.compile(
    r"[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}", re.I)


def page_id(line: str) -> str | None:
    """The Notion page id in the line, normalised to dashed 8-4-4-4-12.

    Any 32-hex run answers, dashed or not, so a bare id and a pasted page
    URL both work: a Notion URL carries the id undashed at the end of its
    slug. Dashed is what gets stored, because it is the only form a
    documented `parent.page_id` request body shows
    (research/19-notion-database-create-api.md:209); the same file types
    the field as `idRequest`, a bare string, and constrains nothing else
    (:258), so nothing further is invented here. A line with no 32-hex run
    answers nothing and is re-asked rather than stored to fail at create
    time.
    """
    match = _PAGE_ID_RE.search(line)
    if match is None:
        return None
    digits = match.group(0).replace("-", "").lower()
    return "-".join((digits[:8], digits[8:12], digits[12:16],
                     digits[16:20], digits[20:]))


def timezone(line: str) -> str | None:
    """An IANA zone name the system tz database knows, or `None`.

    `Sessions.Timezone` is frozen at open (rule L3) and every later
    day-boundary check reads it back, so a zone that does not resolve must
    never be stored. `zoneinfo` is the tz database itself, so no list of
    zone names is kept here to drift.
    """
    name = line.strip()
    try:
        ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return None
    return name


def _bare_number(line: str) -> str | None:
    """A line that is only a number, which is what a direct reply to "how
    many days" or "how old are you" usually is."""
    m = re.fullmatch(r"\s*(\d{1,3})\s*", line)
    return m.group(1) if m else None


def units(line: str) -> str | None:
    m = re.search(r"\b(lbs?|pounds?|kgs?|kilos?|kilograms?)\b", line, re.I)
    if not m:
        return None
    return "kg" if m.group(1).lower().startswith(("kg", "kilo")) else "lb"


def days_in_sentence(line: str) -> str | None:
    m = re.search(r"\b(\d+)\s*days?\b", line, re.I)
    return m.group(1) if m else None


def age_in_sentence(line: str) -> str | None:
    m = (re.search(r"\b(\d{1,3})\s*(?:years?\s*old|yo)\b", line, re.I)
         or re.search(r"\bi'?m\s+(\d{1,3})\b", line, re.I))
    return m.group(1) if m else None


def nutrition(line: str) -> str | None:
    low = line.lower()
    for word in ("none", "general", "specific"):
        if word in low:
            return word
    return None


def days_answer(line: str) -> str | None:
    return days_in_sentence(line) or _bare_number(line)


def age_answer(line: str) -> str | None:
    return age_in_sentence(line) or _bare_number(line)


# --- SKELETON ONLY, docs/storage-section-design.md. TODO stubs, no logic. ---
# The storage section's three new readers. Same contract as every reader
# above: `None` for the line that does not answer this field, which re-asks
# the step and writes nothing (ticket workout-log-481).

_WORD_RE = re.compile(r"[a-zA-Z]+")


def platform(line: str) -> str | None:
    """The store the athlete named, lowercased, or `None`.

    An unrecognised store name is a PARSED answer, not a parse failure:
    "airtable" returns "airtable" and is refused downstream by
    `storage.refusal` with a reason. `None` is reserved for a line naming
    no place at all, because re-asking an athlete who answered correctly
    is the wrong failure.
    """
    match = _WORD_RE.search(line)
    return match.group(0).lower() if match else None


def container_choice(line: str) -> str | None:
    """`"reuse"` for a line meaning use the databases already there, or the
    prefix word for a line offering one. `None` otherwise.

    Only reached when the caller threaded a non-empty
    `state["storage_existing"]` in, so the question fires on an observed
    collision and never on a clean page.
    """
    ...  # TODO


def week_start(line: str) -> str | None:
    """`"monday"` or `"sunday"`, or `None`.

    Monday is ISO 8601 and the shipped default, but it is asked rather than
    assumed: `Sessions.week_index` is stored (rule L18) and a wrong week
    number is never repaired by a later read.
    """
    ...  # TODO


def date_order(line: str) -> str | None:
    """`"day_first"` or `"month_first"`, or `None`.

    Phase 3. It governs what the athlete may type and what she reads back,
    never what is stored: the store holds ISO 8601 because `hydrate.py`
    compares those strings lexically.
    """
    ...  # TODO
