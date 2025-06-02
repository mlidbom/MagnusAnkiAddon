from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from sysutils import kana_utils

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class StemRequirements(Slots):
    def __init__(self, vocab: VocabNote, end_of_stem: WeakRef[TextAnalysisLocation] | None) -> None:
        self.config = vocab.matching_rules
        self.are_fulfilled = True

        self.are_fulfilled = True
        if vocab.matching_rules.forbids_a_stem.is_set():
            self.are_fulfilled = self.are_fulfilled and (end_of_stem is None or end_of_stem().token.surface[-1] not in conjugator.a_stem_characters)
        if vocab.matching_rules.requires_a_stem.is_set():
            self.are_fulfilled = self.are_fulfilled and (end_of_stem is not None and end_of_stem().token.surface[-1] in conjugator.a_stem_characters)
        if vocab.matching_rules.requires_e_stem.is_set():
            self.are_fulfilled = self.are_fulfilled and (end_of_stem is not None and (end_of_stem().token.surface[-1] in conjugator.e_stem_characters or kana_utils.character_is_kanji(end_of_stem().token.surface[-1])))
