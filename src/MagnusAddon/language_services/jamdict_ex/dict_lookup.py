from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.jamdict_ex.dict_lookup_result import DictLookupResult
from language_services.jamdict_ex.jamdict_threading_wrapper import JamdictThreadingWrapper
from sysutils.lazy import Lazy
from sysutils.memory_usage import string_auto_interner
from sysutils.timeutil import StopWatch
from typed_linq_collections.collections.q_list import QList

if TYPE_CHECKING:
    from jamdict.jmdict import JMDEntry  # pyright: ignore[reportMissingTypeStubs]
    from note.vocabulary.vocabnote import VocabNote
    from typed_linq_collections.q_iterable import QIterable

from language_services.jamdict_ex.dict_entry import DictEntry
from sysutils import kana_utils
from typed_linq_collections.collections.q_set import QSet

_jamdict_threading_wrapper: JamdictThreadingWrapper = JamdictThreadingWrapper()

# noinspection SqlResolve
def _find_all_words() -> QSet[str]:
    with StopWatch.log_execution_time("Prepopulating all word forms from jamdict."):
        kanji_forms: QIterable[str] = _jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM Kanji").select(string_auto_interner.auto_intern)
        kana_forms: QIterable[str] = _jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM Kana").select(string_auto_interner.auto_intern)
    return QSet.create(kanji_forms, kana_forms)

# noinspection SqlResolve
def _find_all_names() -> QSet[str]:
    with StopWatch.log_execution_time("Prepopulating all name forms from jamdict."):
        kanji_forms: QIterable[str] = _jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM NEKanji")
        kana_forms: QIterable[str] = _jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM NEKana")
        return QSet.create(kanji_forms, kana_forms)

_all_word_forms = Lazy(_find_all_words)
_all_name_forms = Lazy(_find_all_names)

class DictLookup(Slots):
    @classmethod
    def lookup_vocab_word_or_name(cls, vocab: VocabNote) -> DictLookupResult:
        if vocab.readings.get():
            return cls.lookup_word_or_name_with_matching_reading(vocab.question.without_noise_characters, vocab.readings.get())

        return cls.lookup_word_or_name(vocab.question.without_noise_characters)

    @classmethod
    def lookup_word_or_name_with_matching_reading(cls, word: str, readings: list[str]) -> DictLookupResult:
        if len(readings) == 0: raise ValueError("readings may not be empty. If you want to match without filtering on reading, use lookup_word_or_name instead")
        return cls._try_lookup_word_or_name_with_matching_reading(word, tuple(readings))

    @classmethod
    def _try_lookup_word_or_name_with_matching_reading(cls, word: str, readings: tuple[str, ...]) -> DictLookupResult:  # needs to be a tuple to be hashable for caching
        if not cls.might_be_entry(word): return DictLookupResult.failed()

        return cls._try_lookup_word_or_name_with_matching_reading_inner(word, readings)

    @classmethod
    @cache
    def _try_lookup_word_or_name_with_matching_reading_inner(cls, word: str, readings: tuple[str, ...]) -> DictLookupResult:  # needs to be a tuple to be hashable for caching
        def kanji_form_matches() -> QList[DictEntry]:
            return (lookup
                    .where(lambda entry: any(entry.has_matching_kana_form(reading) for reading in readings)
                                         and len(entry.kanji_forms) > 0
                                         and entry.has_matching_kanji_form(word))
                    .to_list())

        def any_kana_only_matches() -> QList[DictEntry]:
            return (lookup.where(lambda entry: any(entry.has_matching_kana_form(reading) for reading in readings)
                                               and entry.is_kana_only()).to_list())

        lookup: QList[DictEntry] = cls._lookup_word_raw(word)
        if not lookup:
            lookup = cls._lookup_name_raw(word)

        matching = any_kana_only_matches() if kana_utils.is_only_kana(word) else kanji_form_matches()

        return DictLookupResult(matching, word, QList(readings))

    @classmethod
    def lookup_word_or_name(cls, word: str) -> DictLookupResult:
        if not cls.might_be_entry(word): return DictLookupResult.failed()
        word_hit = cls.lookup_word(word)
        if word_hit.found_words():
            return word_hit
        return cls.lookup_name(word)

    @classmethod
    def lookup_word(cls, word: str) -> DictLookupResult:
        if not cls.might_be_word(word): return DictLookupResult.failed()
        entries = cls._lookup_word_raw(word)
        return DictLookupResult(entries, word, QList())

    @classmethod
    def lookup_name(cls, word: str) -> DictLookupResult:
        if not cls.might_be_word(word): return DictLookupResult.failed()
        entries = cls._lookup_name_raw(word)
        return DictLookupResult(entries, word, QList())

    @classmethod
    def _lookup_word_raw(cls, word: str) -> QList[DictEntry]:
        if not cls.might_be_word(word): return QList()
        return cls._lookup_word_raw_inner(word)

    @classmethod
    @cache  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_word_raw_inner(cls, word: str) -> QList[DictEntry]:
        entries = list(_jamdict_threading_wrapper.lookup(word, include_names=False).entries)
        transformed = entries if not kana_utils.is_only_kana(word) else [ent for ent in entries if cls._is_kana_only(ent)]
        return DictEntry.create(transformed)

    @classmethod
    def _lookup_name_raw(cls, word: str) -> QList[DictEntry]:
        if not cls.might_be_name(word): return QList()
        return cls._lookup_name_raw_inner(word)

    @classmethod
    @cache  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_name_raw_inner(cls, word: str) -> QList[DictEntry]:
        result = list(_jamdict_threading_wrapper.lookup(word, include_names=True).names)
        return DictEntry.create(result)

    @classmethod
    def _is_kana_only(cls, entry: JMDEntry) -> bool:
        return not entry.kanji_forms or any(sense for sense
                                            in entry.senses
                                            if "word usually written using kana alone" in sense.misc)  # pyright: ignore[reportUnknownMemberType]

    @classmethod
    def might_be_word(cls, word: str) -> bool:
        return app.is_testing or word in _all_word_forms()

    @classmethod
    def might_be_name(cls, word: str) -> bool:
        return app.is_testing or word in _all_name_forms()

    @classmethod
    def might_be_entry(cls, word: str) -> bool:
        return cls.might_be_word(word) or cls.might_be_name(word)

    @classmethod
    def is_word(cls, word: str) -> bool:
        if not cls.might_be_word(word):
            return False

        return cls._is_word_inner(word)

    @classmethod
    @cache
    def _is_word_inner(cls, word: str) -> bool:
        return cls.lookup_word(word).found_words()

    @classmethod
    def is_dictionary_or_collection_word(cls, word: str) -> bool:
        from ankiutils import app
        return app.col().vocab.is_word(word) or cls.is_word(word)

    # noinspection PyUnusedFunction
    @classmethod
    def ensure_loaded_into_memory(cls) -> None:
        cls._lookup_name_raw("桜")
        cls._lookup_word_raw("俺")
