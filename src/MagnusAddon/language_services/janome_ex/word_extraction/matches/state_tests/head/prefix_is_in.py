from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef
    from typed_linq_collections.collections.q_set import QSet

class ForbidsPrefixIsIn(CustomForbids, Slots):
    def __init__(self, match: WeakRef[VocabMatch], prefixes: QSet[str], is_requirement_active: bool = True) -> None:
        super().__init__(match, is_requirement_active)
        self.prefixes: QSet[str] = prefixes

    @property
    @override
    def description(self) -> str: return f"""prefix_in:{",".join(self.prefixes)}"""

    @override
    def _internal_is_in_state(self) -> bool:
        if any(prefix for prefix in self.prefixes if self.prefix.endswith(prefix)):  # noqa: SIM103
            return True
        return False


class RequiresPrefixIsIn(MatchRequirement, Slots):
    """Requires version of PrefixIsIn check."""
    def __init__(self, match: WeakRef[VocabMatch], prefixes: QSet[str], is_requirement_active: bool = True) -> None:
        self._match: WeakRef[VocabMatch] = match
        self.prefixes: QSet[str] = prefixes
        self.rule_active: bool = is_requirement_active
        self._cached_state: bool | None = None

    @property
    def is_in_state(self) -> bool:
        if self._cached_state is not None:
            return self._cached_state
        prefix = self._match().variant.word.start_location.previous().token.surface if self._match().variant.word.start_location.previous else ""
        self._cached_state = any(p for p in self.prefixes if prefix.endswith(p))
        return self._cached_state

    @property
    @override
    def is_fulfilled(self) -> bool:
        return not self.rule_active or self.is_in_state

    @property
    @override
    def failure_reason(self) -> str:
        return f"""requires::prefix_in:{",".join(self.prefixes)}""" if not self.is_fulfilled else ""
