from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TokenTextLocation
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class TailRequirements(Slots):
    def __init__(self, vocab: VocabNote, tail:WeakRef[TokenTextLocation]) -> None:
        self.config = vocab.matching_rules
        self.are_fulfilled = True
        if self.config.requires_sentence_end.is_set():
            self.are_fulfilled = self.are_fulfilled and (tail is None or tail().token.is_non_word_character)
