from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection(CustomRequiresOrForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def is_required(self) -> bool:
        return self.inspector.match.requires_forbids.ichidan_imperative.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.inspector.match.requires_forbids.ichidan_imperative.is_forbidden

    @property
    @override
    def description(self) -> str: return "ichidan_imperative"

    @property
    def has_godan_ichidan_imperative_part(self) -> bool:
        return self.inspector.word.start_location.token.is_ichidan_imperative_stem or self.inspector.word.start_location.token.is_ichidan_imperative_inflection

    @override
    def _internal_is_in_state(self) -> bool:
        if self.has_godan_ichidan_imperative_part:  # noqa: SIM103
            return True
        return False
