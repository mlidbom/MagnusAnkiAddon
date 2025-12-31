from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration
    from sysutils.weak_ref import WeakRef
    pass

class ForbidsIsPoisonWord(CustomForbids, Slots):
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match, is_requirement_active=True)

    @property
    def rules(self) -> VocabNoteMatchingConfiguration:
        return self.match.vocab.matching_configuration

    @property
    @override
    def description(self) -> str: return "poison_word"

    @override
    def _internal_is_in_state(self) -> bool:
        if self.rules.bool_flags.is_poison_word.is_set():  # noqa: SIM103
            return True
        return False
