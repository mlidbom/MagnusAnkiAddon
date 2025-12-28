from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils import ex_str

if TYPE_CHECKING:
    from language_services.jamdict_ex.dict_entry import DictEntry
    from typed_linq_collections.collections.q_list import QList
    from typed_linq_collections.collections.q_set import QSet

class DictLookupResult(Slots):
    def __init__(self, entries: QList[DictEntry], lookup_word: str, lookup_reading: QList[str]) -> None:
        self.word: str = lookup_word
        self.lookup_reading: QList[str] = lookup_reading
        self.entries: QList[DictEntry] = entries

    def found_words_count(self) -> int: return len(self.entries)
    def found_words(self) -> bool: return len(self.entries) > 0

    def is_uk(self) -> bool: return any(ent for ent
                                        in self.entries
                                        if ent.is_kana_only())

    def valid_forms(self, force_allow_kana_only: bool = False) -> QSet[str]:
        return self.entries.select_many(lambda entry: entry.valid_forms(force_allow_kana_only)).to_set()

    def parts_of_speech(self) -> QSet[str]:
        return self.entries.select_many(lambda entry: entry.parts_of_speech()).to_set()

    def try_get_godan_verb(self) -> DictEntry | None:
        return self.entries.first_or_none(lambda entry: "godan verb" in entry.parts_of_speech())

    def try_get_ichidan_verb(self) -> DictEntry | None:
        return self.entries.first_or_none(lambda entry: "ichidan verb" in entry.parts_of_speech())

    def format_answer(self) -> str:
        if self.entries.qcount() == 1: return self.entries[0].format_answer()

        return ex_str.newline.join(self.entries.select(lambda entry: entry.format_answer()))
