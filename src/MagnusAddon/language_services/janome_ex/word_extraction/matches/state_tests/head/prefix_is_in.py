from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from typed_linq_collections.collections.q_set import QSet

class ForbidsPrefixIsIn(Slots):
    @staticmethod
    def apply_to(inspector: VocabMatchInspector, prefixes: QSet[str]) -> MatchRequirement | None:
        if prefixes and any(prefix for prefix in prefixes if inspector.prefix.endswith(prefix)):
            return FailedMatchRequirement.forbids(f"""prefix_in:{",".join(prefixes)}""")

        return None


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
