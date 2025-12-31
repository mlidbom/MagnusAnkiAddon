from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsHasPastTenseStem(CustomRequiresOrForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def is_required(self) -> bool:
        return self.inspector.match.requires_forbids.past_tense_stem.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.inspector.match.requires_forbids.past_tense_stem.is_forbidden

    @property
    @override
    def description(self) -> str: return "past_tense_stem"

    @override
    def _internal_is_in_state(self) -> bool:
        if self.inspector.previous_location is None:
            return False

        if self.inspector.previous_location.token.is_past_tense_stem():
            return True

        if self.inspector.word.start_location.token.is_past_tense_marker():  # noqa: SIM103
            return True

        return False
