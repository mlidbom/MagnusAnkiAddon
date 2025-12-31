from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsStartsWithGodanPotentialStemOrInflection(CustomRequiresOrForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector) -> None:
        super().__init__(inspector)

    @staticmethod
    def for_if(inspector: VocabMatchInspector) -> RequiresOrForbidsStartsWithGodanPotentialStemOrInflection | None:
        return RequiresOrForbidsStartsWithGodanPotentialStemOrInflection(inspector) if inspector.match.requires_forbids.godan_potential.is_active else None

    @property
    @override
    def is_required(self) -> bool:
        return self.inspector.match.requires_forbids.godan_potential.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.inspector.match.requires_forbids.godan_potential.is_forbidden

    @property
    @override
    def description(self) -> str: return "godan_potential"

    @property
    def has_godan_potential_part(self) -> bool:
        return self.inspector.word.start_location.token.is_godan_potential_inflection or self.inspector.word.start_location.token.is_godan_potential_stem

    @override
    def _internal_is_in_state(self) -> bool:
        if self.has_godan_potential_part:  # noqa: SIM103
            return True
        return False
