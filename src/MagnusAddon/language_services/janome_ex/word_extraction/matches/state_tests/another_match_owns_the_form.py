from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

    pass

class ForbidsAnotherMatchOwnsTheForm(CustomForbids, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match, is_requirement_active=True)

    @property
    def vocab(self) -> VocabNote:
        return self.match.vocab

    @property
    @override
    def description(self) -> str: return "another_match_owns_the_form"

    @override
    def _internal_is_in_state(self) -> bool:
        if self.vocab.forms.is_owned_form(self.tokenized_form):
            return False

        if any(other_match for other_match in self.variant.vocab_matches  # noqa: SIM103
               if other_match != self.match
                  and other_match.vocab.forms.is_owned_form(self.tokenized_form)
                  and other_match.is_valid):
            return True
        return False
