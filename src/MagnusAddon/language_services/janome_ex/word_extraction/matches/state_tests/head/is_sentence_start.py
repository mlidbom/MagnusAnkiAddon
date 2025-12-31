from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction import analysis_constants
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsIsSentenceStart(CustomRequiresOrForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def is_required(self) -> bool:
        return self.match.requires_forbids.sentence_start.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.match.requires_forbids.sentence_start.is_forbidden

    @property
    @override
    def description(self) -> str:
        return "sentence_start"

    @override
    def _internal_is_in_state(self) -> bool:
        if len(self.prefix) == 0 or self.prefix[-1] in analysis_constants.sentence_start_characters:  # noqa: SIM103
            return True
        return False
