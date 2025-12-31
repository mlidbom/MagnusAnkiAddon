from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services import conjugator
from language_services.janome_ex.word_extraction.matches.requirements.custom_requires_or_forbids import CustomRequiresOrForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class RequiresOrForbidsHasAStem(CustomRequiresOrForbids, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match)

    @property
    @override
    def is_required(self) -> bool:
        return self.match.requires_forbids.a_stem.is_required

    @property
    @override
    def is_forbidden(self) -> bool:
        return self.match.requires_forbids.a_stem.is_forbidden

    @property
    @override
    def description(self) -> str: return "a_stem"

    @override
    def _internal_is_in_state(self) -> bool:
        if len(self.prefix) > 0 and self.prefix[-1] in conjugator.a_stem_characters:  # noqa: SIM103
            return True

        return False
