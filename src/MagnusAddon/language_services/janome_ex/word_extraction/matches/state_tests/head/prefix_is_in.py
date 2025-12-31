from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from typed_linq_collections.collections.q_set import QSet

class ForbidsPrefixIsIn(CustomForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector, prefixes: QSet[str]) -> None:
        super().__init__(inspector)
        self.prefixes: QSet[str] = prefixes

    @staticmethod
    def for_if(inspector: VocabMatchInspector, prefixes: QSet[str]) -> ForbidsPrefixIsIn | None:
        return ForbidsPrefixIsIn(inspector, prefixes) if prefixes else None

    @property
    @override
    def description(self) -> str: return f"""prefix_in:{",".join(self.prefixes)}"""

    @override
    def _internal_is_in_state(self) -> bool:
        if any(prefix for prefix in self.prefixes if self.inspector.prefix.endswith(prefix)):  # noqa: SIM103
            return True
        return False


class RequiresPrefixIsIn(MatchRequirement, Slots):
    """Requires version of PrefixIsIn check."""
    def __init__(self, inspector: VocabMatchInspector, prefixes: QSet[str]) -> None:
        self.inspector: VocabMatchInspector = inspector
        self.prefixes: QSet[str] = prefixes
        self._cached_state: bool | None = None

    @staticmethod
    def for_if(inspector: VocabMatchInspector, prefixes: QSet[str]) -> RequiresPrefixIsIn | None:
        return RequiresPrefixIsIn(inspector, prefixes) if prefixes else None

    @property
    def is_in_state(self) -> bool:
        if self._cached_state is not None:
            return self._cached_state
        self._cached_state = any(prefix for prefix in self.prefixes if self.inspector.prefix.endswith(prefix))
        return self._cached_state

    @property
    @override
    def is_fulfilled(self) -> bool:
        return self.is_in_state

    @property
    @override
    def failure_reason(self) -> str:
        return f"""requires::prefix_in:{",".join(self.prefixes)}""" if not self.is_fulfilled else ""
