from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.match import Match
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils import typed

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_entry import DictEntry
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from sysutils.weak_ref import WeakRef

class DictionaryMatch(Match, Slots):
    def __init__(self, word_variant: WeakRef[CandidateWordVariant], dictionary_entry: DictEntry) -> None:
        super().__init__(word_variant,
                         validity_requirements=[],
                         display_requirements=[])
        self.dictionary_entry: DictEntry = dictionary_entry

    @property
    @override
    def answer(self) -> str: return self.dictionary_entry.generate_answer()
    @property
    @override
    def readings(self) -> list[str]: return [typed.str_(f.text) for f in self.dictionary_entry.entry.kana_forms]  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
