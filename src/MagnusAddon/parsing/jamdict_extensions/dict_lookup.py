from functools import lru_cache

from jamdict import Jamdict

from parsing.jamdict_extensions.dict_entry import DictEntry
from sysutils import kana_utils

class DictLookup:
    from note.wanivocabnote import WaniVocabNote

    _jamdict = Jamdict(memory_mode=True)

    def __init__(self, entries: list[DictEntry]):
        self.entries = entries

    def found_words_count(self) -> int: return len(self.entries)
    def found_words(self) -> bool: return len(self.entries) > 0

    def is_uk(self) -> bool: return any((ent for ent
                                         in self.entries
                                         if ent.is_kana_only()))

    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return set().union(*[entry.valid_forms(force_allow_kana_only) for entry in self.entries])

    @classmethod
    def try_lookup_vocab_word_or_name(cls, word: WaniVocabNote) -> 'DictLookup':
        return cls.try_lookup_word_or_name(word.get_question(), word.get_readings())

    @classmethod
    def lookup_word_or_name(cls, word: str, readings: list[str]) -> 'DictLookup':
        result = cls.try_lookup_word_or_name(word, readings)
        if not result.found_words():
            raise KeyError("No matching entries")
        return result

    @classmethod
    def try_lookup_word_or_name(cls, word: str, readings: list[str]) -> 'DictLookup':
        return cls._try_lookup_word_or_name(word, tuple(readings))

    @classmethod
    @lru_cache(maxsize=None)
    def _try_lookup_word_or_name(cls, word: str, readings: tuple[str]) -> 'DictLookup':
        def kanji_form_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.kanji_forms()
                    and ent.has_matching_kanji_form(word)]

        def any_kana_only_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.is_kana_only()]

        lookup = cls._lookup_word(word)
        if not lookup:
            lookup = cls._lookup_name(word)

        matching = any_kana_only_matches() if kana_utils.is_only_kana(word) else kanji_form_matches()

        return DictLookup(matching)

    @classmethod
    def lookup_word_shallow(cls, word: str) -> 'DictLookup':
        return DictLookup(cls._lookup_word(word))

    @classmethod
    @lru_cache(maxsize=None)  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_word(cls, word: str) -> list[DictEntry]:
        return DictEntry.create(cls._jamdict.lookup(word, lookup_chars=False, lookup_ne=False).entries)

    @classmethod
    @lru_cache(maxsize=None)  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_name(cls, word: str) -> list[DictEntry]:
        return DictEntry.create(cls._jamdict.lookup(word, lookup_chars=False).names)
