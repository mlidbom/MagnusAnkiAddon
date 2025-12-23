from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.jamdict_ex.priority_spec import PrioritySpec

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
        return self.entries.select_many(lambda entry: entry.valid_forms(force_allow_kana_only)).to_set()  # set(ex_sequence.flatten([list(entry.valid_forms(force_allow_kana_only)) for entry in self.entries]))

    def parts_of_speech(self) -> QSet[str]:
        return self.entries.select_many(lambda entry: entry.parts_of_speech()).to_set()  # set(ex_sequence.flatten([list(ent.parts_of_speech()) for ent in self.entries]))

    def priority_spec(self) -> PrioritySpec:
        return PrioritySpec(self.entries.select_many(lambda entry: entry.priority_tags()).to_set())  # PrioritySpec(set(ex_iterable.flatten(entry.priority_tags() for entry in self.entries)))