from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from sysutils import kana_utils

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


class StemRequirements(Slots):
    def __init__(self, vocab: VocabNote, stem: str) -> None:
        self.config = vocab.matching_rules
        self.are_fulfilled = True

        self.are_fulfilled = True
        if vocab.matching_rules.forbids_a_stem.is_set():
            self.are_fulfilled = self.are_fulfilled and (stem == "" or stem not in conjugator.a_stem_characters)
        if vocab.matching_rules.requires_a_stem.is_set():
            self.are_fulfilled = self.are_fulfilled and (stem != "" and stem in conjugator.a_stem_characters)
        if vocab.matching_rules.requires_e_stem.is_set():
            self.are_fulfilled = self.are_fulfilled and (stem != "" and (stem in conjugator.e_stem_characters or kana_utils.character_is_kanji(stem[-1])))
