from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from jamdict.jmdict import JMDEntry

from language_services.jamdict_ex.priority_spec import PrioritySpec
from sysutils.lazy import BackgroundInitialingLazy
from sysutils.typed import str_

if TYPE_CHECKING:
    from note.vocabnote import VocabNote

from jamdict import Jamdict

from language_services.jamdict_ex.dict_entry import DictEntry
from sysutils import ex_iterable, kana_utils

_jamdict = Jamdict(reuse_ctx=False)

def _find_all_words() -> set[str]:
    kanji_forms: set[str] = set()
    kana_forms: set[str] = set()

    with _jamdict.jmdict.ctx() as ctx:
        for batch in ctx.conn.execute("SELECT distinct text FROM Kanji"):
            for row in batch:
                kanji_forms.add(str_(row))

    with _jamdict.jmdict.ctx() as ctx:
        for batch in ctx.conn.execute("SELECT distinct text FROM Kana"):
            for row in batch:
                kana_forms.add(str_(row))

    return kanji_forms | kana_forms

def _find_all_names() -> set[str]:
    kanji_forms: set[str] = set()
    kana_forms: set[str] = set()

    with _jamdict.jmdict.ctx() as ctx:
        for batch in ctx.conn.execute("SELECT distinct text FROM NEKanji"):
            for row in batch:
                kanji_forms.add(str_(row))

    with _jamdict.jmdict.ctx() as ctx:
        for batch in ctx.conn.execute("SELECT distinct text FROM NEKana"):
            for row in batch:
                kana_forms.add(str_(row))

    return kanji_forms | kana_forms

_all_word_forms = BackgroundInitialingLazy(_find_all_words)
_all_name_forms = BackgroundInitialingLazy(_find_all_names)

class DictLookup:
    def __init__(self, entries: list[DictEntry], lookup_word: str, lookup_reading: list[str]):
        self.lookup_word = lookup_word
        self.lookup_reading = lookup_reading
        self.entries = entries

    def found_words_count(self) -> int: return len(self.entries)
    def found_words(self) -> bool: return len(self.entries) > 0

    def is_uk(self) -> bool: return any((ent for ent
                                         in self.entries
                                         if ent.is_kana_only()))

    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return set().union(*[entry.valid_forms(force_allow_kana_only) for entry in self.entries])

    def parts_of_speech(self) -> set[str]:
        return set().union(*[ent.parts_of_speech() for ent in self.entries])

    def priority_spec(self) -> PrioritySpec:
        return PrioritySpec(set(ex_iterable.flatten((entry.priority_tags() for entry in self.entries))))

    @classmethod
    def try_lookup_vocab_word_or_name(cls, vocab: VocabNote) -> DictLookup:
        return cls.try_lookup_word_or_name(vocab.get_question(), vocab.get_readings())

    @classmethod
    def try_lookup_word_or_name(cls, word: str, readings: list[str]) -> DictLookup:
        return cls._try_lookup_word_or_name(word, tuple(readings))

    @classmethod
    @lru_cache(maxsize=None)
    def _try_lookup_word_or_name(cls, word: str, readings: tuple[str, ...]) -> DictLookup:
        if not cls.might_be_entry(word): return DictLookup([], word,[])

        def kanji_form_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.kanji_forms()
                    and ent.has_matching_kanji_form(word)]

        def any_kana_only_matches() -> list[DictEntry]:
            return [ent for ent in lookup
                    if any(ent.has_matching_kana_form(reading) for reading in readings)
                    and ent.is_kana_only()]

        lookup: list[DictEntry] = DictEntry.create(cls._lookup_word(word), word, list(readings))
        if not lookup:
            lookup = DictEntry.create(cls._lookup_name(word), word, list(readings))

        matching = any_kana_only_matches() if kana_utils.is_only_kana(word) else kanji_form_matches()

        return DictLookup(matching, word, list(readings))

    @classmethod
    def lookup_word_shallow(cls, word: str) -> DictLookup:
        if not cls.might_be_word(word): return DictLookup([], word, [])
        entries = DictEntry.create(cls._lookup_word(word), word, [])
        return DictLookup(entries, word, [])

    @classmethod
    @lru_cache(maxsize=None)  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_word(cls, word: str) -> list[JMDEntry]:
        if not cls.might_be_word(word): return []

        entries = list(_jamdict.lookup(word, lookup_chars=False, lookup_ne=False).entries)
        return entries if not kana_utils.is_only_kana(word) else [ent for ent in entries if cls._is_kana_only(ent)]

    @classmethod
    @lru_cache(maxsize=None)  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_name(cls, word: str) -> list[JMDEntry]:
        if not cls.might_be_name(word): return []
        return list(_jamdict.lookup(word, lookup_chars=False).names)

    @staticmethod
    def _is_kana_only(entry: JMDEntry) -> bool:
        return not entry.kanji_forms or any((sense for sense
                                             in entry.senses
                                             if 'word usually written using kana alone' in sense.misc))

    @classmethod
    def might_be_word(cls, word:str) -> bool:
        return word in _all_word_forms.instance()

    @classmethod
    def might_be_name(cls, word:str) -> bool:
        return word in _all_name_forms.instance()

    @classmethod
    def might_be_entry(cls, word:str) -> bool:
        return cls.might_be_word(word) or cls.might_be_name(word)

    @classmethod
    def is_word(cls, word:str) -> bool:
        return cls.might_be_word(word) and cls.lookup_word_shallow(word).found_words()
