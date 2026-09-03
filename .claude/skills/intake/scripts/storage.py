"""Which stores this build can write to, and what happens when the
athlete names one it cannot.

One body of domain knowledge (docs/architecture.md "One script per skill"
splits by DOMAIN, never by execution step): what a store is, whether this
build has been proven against it, what it is called under the athlete's
page. Turning an answer into writes stays in `intake.py`; the ordered
question table stays in `questions.py`; reading a value out of a chat line
stays in `readers.py`.

The refusal is the point of this module. A store with no DDL behind it gets
refused before a single `database-create` is emitted, so a half built
workspace holding unreadable training data is not reachable. `is_proven`
gates `ddl.next_create_write` at create time and `hydrate.py` at cold
start, which is the same shape as `preconditions.no_sets_while_halted`:
the check sits at the chokepoint every write already routes through, so no
handler can forget it.
"""

from __future__ import annotations

from typing import Any


def named(state: dict[str, Any]) -> str | None:
    """The store the athlete named, or `None` before she has been asked.

    Read from `state`, not from the page, because `ddl.next_create_write`
    needs it on the same turn the answer lands (the same reason
    `notion_parent_page_id` carries a `state_key`).
    """
    return state.get("storage_platform")


# The only store this build has DDL and fixtures for
# (docs/storage-section-design.md "Where store-specific mapping lives").
PROVEN = frozenset({"notion"})


def is_proven(platform: str | None) -> bool:
    """Whether this build has a profile and fixtures for that store.

    `None` is not proven: an install that has not answered the question yet
    creates nothing, the same way a missing parent page id creates nothing
    today. Proven means a DDL renderer plus fixtures replaying against
    `tools/mock-notion`, never a claim in prose.
    """
    return platform in PROVEN


def refusal(platform: str) -> str:
    """The one line the athlete reads instead of the next question.

    Names the store she asked for, names the one that works, says her
    answer was recorded, and offers the way forward. Asserted byte for byte
    by `fixtures/13-storage-refusal`, so rewording it turns that fixture
    red.
    """
    name = platform.capitalize()
    return (
        f"I can't write to {name} yet. Notion is the only one I've been "
        f"proven against, and I'd rather say so now than build you half a "
        f"log. I've written down that you asked for {name}. Say 'notion' "
        f"and I'll set that up instead."
    )


def container_name(db: str, prefix: str) -> str:
    """The display title for one schema database under the athlete's page.

    `db` stays the internal id everywhere else: `notion_data_sources` maps
    it to the data source id the create returned, and every later
    `row-create` routes by that id. So the athlete's prefix touches exactly
    one place, `ddl.create_payload`'s `title`, and property names are never
    renameable (all 24 fixtures assert them).
    """
    ...  # TODO
