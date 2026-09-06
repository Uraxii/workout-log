"""Which stores this build can write to, and what happens when the
athlete names one it cannot.

One body of domain knowledge (docs/architecture.md "One script per skill"
splits by DOMAIN, never by execution step): what a store is, whether this
build has been proven against it, what it is called under the athlete's
page. Turning an answer into writes stays in `intake.py`; the ordered
question table stays in `questions.py`; reading a value out of a chat line
stays in `readers.py`.

`PROFILES` is the registry, and every store fact is derived from it.
`PROVEN` is `frozenset(PROFILES)` rather than a second list, the spoken
store names in `refusal` are rendered from it rather than written into a
sentence, and each profile supplies its own key so nothing here holds a
store-specific string. Adding a third store is one entry in the tuple
`PROFILES` is built from, and there is nowhere for a stale copy to hide.

The refusal is the point of this module. A store with no profile behind it
gets refused before a single `database-create` is emitted, so a half built
workspace holding unreadable training data is not reachable. `is_proven`
gates `next_create_write` at create time and `hydrate.py` at cold start,
which is the same shape as `preconditions.no_sets_while_halted`: the check
sits at the chokepoint every write already routes through, so no handler
can forget it.
"""

from __future__ import annotations

from types import ModuleType
from typing import Any

import ddl
import vault

# One entry per store this build has a profile and fixtures for. Keyed by
# each module's own `ID`, so a registry key cannot drift from the id the
# profile answers to.
PROFILES: dict[str, ModuleType] = {store.ID: store for store in (ddl, vault)}

PROVEN = frozenset(PROFILES)


def named(state: dict[str, Any]) -> str | None:
    """The store the athlete named, or `None` before she has been asked.

    Read from `state`, not from the page, because `next_create_write`
    needs it on the same turn the answer lands (the same reason
    `storage_root` carries a `state_key`).
    """
    return state.get("storage_platform")


def is_proven(platform: str | None) -> bool:
    """Whether this build has a profile and fixtures for that store.

    `None` is not proven: an install that has not answered the question yet
    creates nothing, the same way a missing store root creates nothing
    today. Proven means a profile module in `PROFILES` plus fixtures
    replaying against `tools/mock-notion`, never a claim in prose.
    """
    return platform in PROVEN


def profile(state: dict[str, Any]) -> ModuleType | None:
    """The store profile this install writes through, or `None`.

    `None` covers both the install that has not been asked yet and the one
    that named a store this build cannot write to, because neither may
    create anything and callers treat them the same way.
    """
    return PROFILES.get(named(state))


def _joined(words: list[str], conjunction: str) -> str:
    """An English list: two joined by the word, three or more by commas."""
    if len(words) < 3:
        return f" {conjunction} ".join(words)
    return f"{', '.join(words[:-1])}, {conjunction} {words[-1]}"


def proven_stores() -> str:
    """The registered store names as the athlete reads them, for the three
    spoken lines that have to name them: this module's refusal and the
    storage question's prompt and reask in `questions.py`. Rendered rather
    than written out, so a third store cannot leave a sentence stale."""
    return _joined([store_id.capitalize() for store_id in PROFILES], "and")


def refusal(platform: str) -> str:
    """The one line the athlete reads instead of the next question.

    Names the store she asked for, names the ones that work, says her
    answer was recorded, and offers the way forward. Asserted byte for byte
    by `fixtures/13-storage-refusal`, so rewording it turns that fixture
    red.
    """
    name = platform.capitalize()
    choices = _joined([f"'{store_id}'" for store_id in PROFILES], "or")
    return (
        f"I can't write to {name} yet. {proven_stores()} are the ones I've "
        f"been proven against, and I'd rather say so now than build you "
        f"half a log. I've written down that you asked for {name}. Say "
        f"{choices} and I'll set that up instead."
    )


def next_create_write(state: dict[str, Any]) -> list[dict[str, Any]]:
    """At most one `database-create` write: the next database still missing.

    One call per database, in schema declaration order, with the caller
    threading each returned id back into `state["databases"]` (ticket
    workout-log-29l) so a rerun adopts rather than duplicates.

    The loop lives here rather than in either profile because it is the
    same loop for every store: only `create_payload` differs, and the
    schema it reads is the log's shape, not Notion's. `ddl.load_schema`
    stays the one reader of that file.

    The store root is the athlete's, read from `state` under the key her
    store names. With no root there is nothing to create under and the
    questions still run.
    """
    store = profile(state)
    if store is None:
        # Gate 1 of two (docs/storage-section-design.md "Refusing a
        # store"). Not one `database-create` for a store this build has no
        # profile for, so nothing is created under the athlete's root.
        return []
    root = state.get(store.ROOT_KEY)
    if root is None:
        return []
    schema = ddl.load_schema()
    created = state.get("databases", {})
    for db in schema["databases"]:
        if db not in created:
            return [{"verb": "database-create", "target": db,
                     "payload": store.create_payload(db, root, schema)}]
    return []


def container_name(db: str, prefix: str) -> str:
    """The display title for one schema database under the athlete's page.

    `db` stays the internal id everywhere else: `notion_data_sources` maps
    it to the data source id the create returned, and every later
    `row-create` routes by that id. So the athlete's prefix touches exactly
    one place, `ddl.create_payload`'s `title`, and property names are never
    renameable (all 24 fixtures assert them).
    """
    ...  # TODO
