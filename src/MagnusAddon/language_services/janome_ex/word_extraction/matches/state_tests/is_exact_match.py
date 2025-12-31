from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from note.vocabulary.vocabnote import VocabNote

class RequiresOrForbidsIsExactMatch(CustomRequiresOrForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @staticmethod
    def for_if(inspector: VocabMatchInspector) -> RequiresOrForbidsIsExactMatch | None:
        return RequiresOrForbidsIsExactMatch(inspector) if inspector.match.requires_forbids.exact_match.is_active else None

    @property
    @override
    def is_required(self) -> bool:
        return self.inspector.match.requires_forbids.exact_match.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.inspector.match.requires_forbids.exact_match.is_forbidden

    @property
    def vocab(self) -> VocabNote:
        return self.inspector.match.vocab

    @property
    @override
    def description(self) -> str: return "exact_match"

    @override
    def _internal_is_in_state(self) -> bool:
        if not self.inspector.variant.is_surface:
            return False

        if self.inspector.variant.form in self.vocab.forms.all_set():  # noqa: SIM103
            return True
        return False
