from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING, Any

from ankiutils import app
from ex_autoslot import AutoSlots
from language_services.jamdict_ex.priority_spec import PrioritySpec
from sysutils.collections.queryable.collections.q_list import QList
from sysutils.collections.queryable.q_iterable import query
from sysutils.lazy import Lazy
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional, str_

if TYPE_CHECKING:
    from collections.abc import Callable

    from jamdict.jmdict import JMDEntry  # pyright: ignore[reportMissingTypeStubs]
    from jamdict.util import LookupResult  # pyright: ignore[reportMissingTypeStubs]
    from note.vocabulary.vocabnote import VocabNote

import queue
import threading
from concurrent.futures import Future

from jamdict import Jamdict  # pyright: ignore[reportMissingTypeStubs]
from language_services.jamdict_ex.dict_entry import DictEntry
from sysutils import kana_utils


class Request[T](AutoSlots):
    def __init__(self, func: Callable[[Jamdict], T], future: Future[T]) -> None:
        self.func: Callable[[Jamdict], T] = func
        self.future: Future[T] = future

class JamdictThreadingWrapper(AutoSlots):
    def __init__(self) -> None:
        self._queue: queue.Queue[Request[Any]] = queue.Queue()  # pyright: ignore[reportExplicitAny]
        self._thread: threading.Thread = threading.Thread(target=self._worker, daemon=True)
        self._running: bool = True
        self._thread.start()
        self.jamdict: Lazy[Jamdict] = Lazy(self.create_jamdict_and_log_loading_time)

    @staticmethod
    def create_jamdict_and_log_loading_time() -> Jamdict:
        jamdict = Jamdict(memory_mode=True) \
            if (app.config().load_jamdict_db_into_memory.get_value()
                and not app.is_testing) \
            else Jamdict(reuse_ctx=True)
        jamdict.lookup("俺", lookup_chars=False, lookup_ne=True)  # pyright: ignore[reportUnknownMemberType]
        return jamdict

    def _worker(self) -> None:
        while self._running:
            request = self._queue.get()
            try:
                result = request.func(self.jamdict())  # pyright: ignore[reportAny]
                request.future.set_result(result)
            except Exception as e:
                request.future.set_exception(e)

    def lookup(self, word: str, include_names: bool) -> LookupResult:
        future: Future[LookupResult] = Future()

        def do_actual_lookup(jamdict: Jamdict) -> LookupResult:
            return jamdict.lookup(word, lookup_chars=False, lookup_ne=include_names)  # pyright: ignore[reportUnknownMemberType]

        self._queue.put(Request(do_actual_lookup, future))
        return future.result()

    def run_string_query(self, query: str) -> list[str]:
        def perform_query(jamdict: Jamdict) -> list[str]:
            result: list[str] = []
            for batch in non_optional(non_optional(jamdict.jmdict).ctx().conn).execute(query):  # pyright: ignore[reportAny]
                for row in batch:  # pyright: ignore[reportAny]
                    result.append(str_(row))  # noqa: PERF401  # pyright: ignore[reportAny]

            return result

        future: Future[list[str]] = Future()

        self._queue.put(Request(perform_query, future))
        return future.result()

_jamdict_threading_wrapper: JamdictThreadingWrapper = JamdictThreadingWrapper()

# noinspection SqlResolve
def _find_all_words() -> set[str]:
    with StopWatch.log_execution_time("Prepopulating all word forms from jamdict."):
        kanji_forms: set[str] = set(_jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM Kanji"))
        kana_forms: set[str] = set(_jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM Kana"))
    return kanji_forms | kana_forms

# noinspection SqlResolve
def _find_all_names() -> set[str]:
    with StopWatch.log_execution_time("Prepopulating all name forms from jamdict."):
        _jamdict = Jamdict(reuse_ctx=False)
        kanji_forms: set[str] = set(_jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM NEKanji"))
        kana_forms: set[str] = set(_jamdict_threading_wrapper.run_string_query("SELECT distinct text FROM NEKana"))
        return kanji_forms | kana_forms

_all_word_forms = Lazy(_find_all_words)
_all_name_forms = Lazy(_find_all_names)

# todo: This mixes up static querying with the results. Let's keep the two separate and readable huh?
class DictLookup(AutoSlots):
    def __init__(self, entries: QList[DictEntry], lookup_word: str, lookup_reading: QList[str]) -> None:
        self.word: str = lookup_word
        self.lookup_reading: QList[str] = lookup_reading
        self.entries: QList[DictEntry] = entries

    @staticmethod
    def _failed_for_word(word: str) -> DictLookup:
        return DictLookup(QList(), word, QList())

    def found_words_count(self) -> int: return len(self.entries)
    def found_words(self) -> bool: return len(self.entries) > 0

    def is_uk(self) -> bool: return any(ent for ent
                                        in self.entries
                                        if ent.is_kana_only())

    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return query(self.entries).select_many(lambda entry: entry.valid_forms(force_allow_kana_only)).to_set()  # set(ex_sequence.flatten([list(entry.valid_forms(force_allow_kana_only)) for entry in self.entries]))

    def parts_of_speech(self) -> set[str]:
        return query(self.entries).select_many(lambda entry: entry.parts_of_speech()).to_set()  # set(ex_sequence.flatten([list(ent.parts_of_speech()) for ent in self.entries]))

    def priority_spec(self) -> PrioritySpec:
        return PrioritySpec(self.entries.select_many(lambda entry: entry.priority_tags()).to_set())  #PrioritySpec(set(ex_iterable.flatten(entry.priority_tags() for entry in self.entries)))

    @classmethod
    def lookup_vocab_word_or_name(cls, vocab: VocabNote) -> DictLookup:
        if vocab.readings.get():
            return cls.lookup_word_or_name_with_matching_reading(vocab.question.without_noise_characters, vocab.readings.get())

        return cls.lookup_word_or_name(vocab.question.without_noise_characters)

    @classmethod
    def lookup_word_or_name_with_matching_reading(cls, word: str, readings: list[str]) -> DictLookup:
        if len(readings) == 0: raise ValueError("readings may not be empty. If you want to match without filtering on reading, use lookup_word_or_name instead")
        return cls._try_lookup_word_or_name_with_matching_reading(word, tuple(readings))

    @classmethod
    @cache
    def _try_lookup_word_or_name_with_matching_reading(cls, word: str, readings: tuple[str, ...]) -> DictLookup:  # needs to be a tuple to be hashable for caching
        if not cls.might_be_entry(word): return DictLookup._failed_for_word(word)

        def kanji_form_matches() -> QList[DictEntry]:
            return (lookup
                    .where(lambda entry: any(entry.has_matching_kana_form(reading) for reading in readings)
                                         and len(entry.kanji_forms()) > 0
                                         and entry.has_matching_kanji_form(word))
                    .to_list())
            # return [ent for ent in lookup
            #         if any(ent.has_matching_kana_form(reading) for reading in readings)
            #         and ent.kanji_forms()
            #         and ent.has_matching_kanji_form(word)]

        def any_kana_only_matches() -> QList[DictEntry]:
            return (lookup.where(lambda entry: any(entry.has_matching_kana_form(reading) for reading in readings)
                                               and entry.is_kana_only()).to_list())
            # return [ent for ent in lookup
            #         if any(ent.has_matching_kana_form(reading) for reading in readings)
            #         and ent.is_kana_only()]

        lookup: QList[DictEntry] = DictEntry.create(cls._lookup_word_raw(word), word, list(readings))
        if not lookup:
            lookup = DictEntry.create(cls._lookup_name_raw(word), word, list(readings))

        matching = any_kana_only_matches() if kana_utils.is_only_kana(word) else kanji_form_matches()

        return DictLookup(matching, word, QList(readings))

    @classmethod
    def lookup_word_or_name(cls, word: str) -> DictLookup:
        if not cls.might_be_entry(word): return DictLookup._failed_for_word(word)
        word_hit = cls.lookup_word(word)
        if word_hit.found_words():
            return word_hit
        return cls.lookup_name(word)

    @classmethod
    def lookup_word(cls, word: str) -> DictLookup:
        if not cls.might_be_word(word): return DictLookup._failed_for_word(word)
        entries = DictEntry.create(cls._lookup_word_raw(word), word, [])
        return DictLookup(entries, word, QList())

    @classmethod
    def lookup_name(cls, word: str) -> DictLookup:
        if not cls.might_be_word(word): return DictLookup._failed_for_word(word)
        entries = DictEntry.create(cls._lookup_name_raw(word), word, [])
        return DictLookup(entries, word, QList())

    @classmethod
    @cache  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_word_raw(cls, word: str) -> list[JMDEntry]:
        if not cls.might_be_word(word): return []

        entries = list(_jamdict_threading_wrapper.lookup(word, include_names=False).entries)
        return entries if not kana_utils.is_only_kana(word) else [ent for ent in entries if cls._is_kana_only(ent)]

    @classmethod
    @cache  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_name_raw(cls, word: str) -> list[JMDEntry]:
        if not cls.might_be_name(word): return []
        return list(_jamdict_threading_wrapper.lookup(word, include_names=True).names)

    @staticmethod
    def _is_kana_only(entry: JMDEntry) -> bool:
        return not entry.kanji_forms or any(sense for sense
                                            in entry.senses
                                            if "word usually written using kana alone" in sense.misc)  # pyright: ignore[reportUnknownMemberType]

    @classmethod
    def might_be_word(cls, word: str) -> bool:
        # this method is a pure optimization to save on dictionary calls during real runtime. During tests populating all the words is a suboptimization, so just always return true when testing
        return app.is_testing or word in _all_word_forms()

    @classmethod
    def might_be_name(cls, word: str) -> bool:
        # this method is a pure optimization to save on dictionary calls during real runtime. During tests populating all the words is a suboptimization, so just always return true when testing
        return app.is_testing or word in _all_name_forms()

    @classmethod
    def might_be_entry(cls, word: str) -> bool:
        return cls.might_be_word(word) or cls.might_be_name(word)

    @classmethod
    @cache
    def is_word(cls, word: str) -> bool:
        return cls.might_be_word(word) and cls.lookup_word(word).found_words()

    @classmethod
    @cache
    def is_dictionary_or_collection_word(cls, word: str) -> bool:
        from ankiutils import app
        return app.col().vocab.is_word(word) or cls.is_word(word)

    @classmethod
    def ensure_loaded_into_memory(cls) -> None:
        cls._lookup_name_raw("桜")
        cls._lookup_word_raw("俺")
