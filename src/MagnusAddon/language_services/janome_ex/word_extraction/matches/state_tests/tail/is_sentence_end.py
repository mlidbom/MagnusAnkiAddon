from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction import analysis_constants
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsIsSentenceEnd(CustomRequiresOrForbids, Slots):

    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def is_required(self) -> bool:
        return self.inspector.match.requires_forbids.sentence_end.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.inspector.match.requires_forbids.sentence_end.is_forbidden

    @property
    @override
    def description(self) -> str: return "sentence_end"

    @override
    def _internal_is_in_state(self) -> bool:
        if len(self.inspector.suffix) == 0:
            return True

        if self.inspector.suffix[0].isspace():
            return True

        if self.inspector.suffix in analysis_constants.sentence_end_characters:  # noqa: SIM103
            return True

        return False
