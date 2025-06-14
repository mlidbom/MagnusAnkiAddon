from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.match import Match

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_entry import DictEntry
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from sysutils.weak_ref import WeakRef

class DictionaryMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], dictionary_entry: DictEntry) -> None:
        super().__init__(word_variant, None)
        self.dictionary_entry: DictEntry = dictionary_entry
        self.answer: str = dictionary_entry.generate_answer()
        self.readings: list[str] = [f.text for f in dictionary_entry.entry.kana_forms]

    @property
    def is_secondary_match(self) -> bool: return True
