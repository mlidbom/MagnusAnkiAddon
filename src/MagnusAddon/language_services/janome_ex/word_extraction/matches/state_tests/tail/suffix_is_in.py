from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from typed_linq_collections.collections.q_set import QSet

class ForbidsSuffixIsIn(CustomForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector, suffixes: QSet[str]) -> None:
        super().__init__(inspector)
        self.suffixes: QSet[str] = suffixes

    @staticmethod
    def for_if(inspector: VocabMatchInspector, suffixes: QSet[str]) -> ForbidsSuffixIsIn | None:
        return ForbidsSuffixIsIn(inspector, suffixes) if suffixes else None

    @property
    @override
    def description(self) -> str: return f"""suffix_in:{",".join(self.suffixes)}"""

    @override
    def _internal_is_in_state(self) -> bool:
        if any(suffix for suffix in self.suffixes if self.inspector.suffix.startswith(suffix)):  # noqa: SIM103
            return True

        return False
