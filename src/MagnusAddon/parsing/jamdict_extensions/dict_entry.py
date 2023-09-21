from typing import Sequence

from jamdict.jmdict import JMDEntry

from sysutils import kana_utils


class DictEntry:
    def __init__(self, entry: JMDEntry) -> None:
        self.entry = entry

    def is_kana_only(self) -> bool:
        return not self.entry.kanji_forms or any((sense for sense
                                                  in self.entry.senses
                                                  if 'word usually written using kana alone' in sense.misc))

    @classmethod
    def create(cls, entries: Sequence[JMDEntry]) -> list['DictEntry']:
        return [cls(entry) for entry in entries]

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return any(search == kana_utils.to_hiragana(form) for form in self.kana_forms())

    def is_default_kana_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return search == kana_utils.to_hiragana(self.kana_forms()[0])

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return any(search == kana_utils.to_hiragana(form) for form in self.kanji_forms())

    def is_default_kanji_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return search == kana_utils.to_hiragana(self.kanji_forms()[0])

    def kana_forms(self) -> list[str]: return [ent.text for ent in self.entry.kana_forms]
    def kanji_forms(self) -> list[str]: return [ent.text for ent in self.entry.kanji_forms]
    def valid_forms(self) -> set[str]:
        return set(self.kana_forms()) | set(self.kanji_forms()) if self.is_kana_only() else self.kanji_forms()
