from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class RequiresOrForbidsStartsWithGodanImperativeStemOrInflection(CustomRequiresOrForbids, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match)

    @property
    @override
    def is_required(self) -> bool:
        return self.match.requires_forbids.godan_imperative.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.match.requires_forbids.godan_imperative.is_forbidden

    @property
    @override
    def description(self) -> str: return "godan_imperative"

    @property
    def has_godan_imperative_part(self) -> bool:
        return self.word.start_location.token.is_godan_imperative_inflection or self.word.start_location.token.is_godan_imperative_stem

    @override
    def _internal_is_in_state(self) -> bool:
        if self.has_godan_imperative_part:  # noqa: SIM103
            return True
        return False
