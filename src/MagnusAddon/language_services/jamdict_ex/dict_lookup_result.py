from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils import ex_str, kana_utils

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

    def readings(self) -> QList[str]: return self.entries.select_many(lambda entry: entry.kana_forms).distinct().to_list()

    def parts_of_speech(self) -> QSet[str]:
        return self.entries.select_many(lambda entry: entry.parts_of_speech()).to_set()

    def try_get_godan_verb(self) -> DictEntry | None:
        return self.entries.first_or_none(lambda entry: "godan verb" in entry.parts_of_speech())

    def try_get_ichidan_verb(self) -> DictEntry | None:
        return self.entries.first_or_none(lambda entry: "ichidan verb" in entry.parts_of_speech())

    def format_answer(self) -> str:
        if self.entries.qcount() == 1: return self.entries[0].format_answer()

        def format_readings(readings: QList[str]) -> str:
            def format_reading(reading: str) -> str: return f"<read>{reading}</read>"
            return f"""{"|".join(readings.select(format_reading))}: """

        def _create_separating_description(entry: DictEntry) -> str:
            reading_diff = ""
            kanji_diff = ""
            other_entries = self.entries.where(lambda other_entry: other_entry != entry).to_list()

            kana_forms = entry.kana_forms.select(kana_utils.katakana_to_hiragana).to_set()
            other_kana_forms = (other_entries.select_many(lambda it: it.kana_forms)
                                .select(kana_utils.katakana_to_hiragana)
                                .to_set())

            if entry.kanji_forms.any() and entry.kanji_forms[0] != self.word:
                kanji_diff = f"""<tag><ja>{entry.kanji_forms[0]}</ja></tag>: """

            if entry.kana_forms[0] != self.word and kana_forms != other_kana_forms:
                reading_diff = format_readings(entry.kana_forms.select(kana_utils.katakana_to_hiragana).distinct().to_list())

            return f"""{reading_diff}{kanji_diff}"""

        return ex_str.newline.join(self.entries.select(lambda entry: f"""{_create_separating_description(entry)}{entry.format_answer()}"""))
