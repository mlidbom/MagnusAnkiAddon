from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from language_services.jamdict_ex.priority_spec import PrioritySpec
from sysutils.lazy import Lazy
from sysutils.timeutil import StopWatch
from sysutils.typed import str_

if TYPE_CHECKING:
    from jamdict.jmdict import JMDEntry
    from jamdict.util import LookupResult
    from note.vocabulary.vocabnote import VocabNote

import queue
import threading
from concurrent.futures import Future
from typing import Any, Callable, Generic, TypeVar

from jamdict import Jamdict
from language_services.jamdict_ex.dict_entry import DictEntry
from sysutils import ex_iterable, kana_utils

T = TypeVar("T")

class Request(Generic[T], Slots):
    def __init__(self, func: Callable[[Jamdict], T], future: Future[T]) -> None:
        self.func = func
        self.future = future

class JamdictThreadingWrapper(Slots):
    def __init__(self) -> None:
        self._queue: queue.Queue[Request[Any]] = queue.Queue()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._running = True
        self._thread.start()
        self.jamdict:Lazy[Jamdict] = Lazy(self.create_jamdict_and_log_loading_time)

    @staticmethod
    def create_jamdict_and_log_loading_time() -> Jamdict:
        with StopWatch.log_execution_time("Loading Jamdict into memory"):
            jamdict = Jamdict(memory_mode=True)
            jamdict.lookup("俺", lookup_chars=False, lookup_ne=True)
            return jamdict

    def _worker(self) -> None:
        while self._running:
            request = self._queue.get()
            if request is None:
                break
            try:
                result = request.func(self.jamdict.instance())
                request.future.set_result(result)
            except Exception as e:
                request.future.set_exception(e)

    def lookup(self, word: str, lookup_chars: bool, lookup_ne: bool) -> LookupResult:
        future: Future[LookupResult] = Future()

        def do_actual_lookup(jamdict: Jamdict) -> LookupResult:
            return jamdict.lookup(word, lookup_chars=lookup_chars, lookup_ne=lookup_ne)

        self._queue.put(Request(do_actual_lookup, future))
        return future.result()

    # def shutdown(self) -> None:
    #     self._running = False
    #     def null_op(jamdict:Jamdict) -> str: return ""
    #     self._queue.put(Request(null_op, Future()))#Prevents deadlock
    #     self._thread.join()

_jamdict_threading_wrapper = JamdictThreadingWrapper()

def _find_all_words() -> set[str]:
    with StopWatch.log_execution_time("Prepopulating all word forms from jamdict."):
        _jamdict = Jamdict(reuse_ctx=False)
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
    with StopWatch.log_execution_time("Prepopulating all name forms from jamdict."):
        _jamdict = Jamdict(reuse_ctx=False)
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

_all_word_forms = Lazy(_find_all_words)
_all_name_forms = Lazy(_find_all_names)

class DictLookup(Slots):
    def __init__(self, entries: list[DictEntry], lookup_word: str, lookup_reading: list[str]) -> None:
        self.lookup_word = lookup_word
        self.lookup_reading = lookup_reading
        self.entries = entries

    def found_words_count(self) -> int: return len(self.entries)
    def found_words(self) -> bool: return len(self.entries) > 0

    def is_uk(self) -> bool: return any(ent for ent
                                        in self.entries
                                        if ent.is_kana_only())

    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return set().union(*[entry.valid_forms(force_allow_kana_only) for entry in self.entries])

    def parts_of_speech(self) -> set[str]:
        return set().union(*[ent.parts_of_speech() for ent in self.entries])

    def priority_spec(self) -> PrioritySpec:
        return PrioritySpec(set(ex_iterable.flatten(entry.priority_tags() for entry in self.entries)))

    @classmethod
    def try_lookup_vocab_word_or_name(cls, vocab: VocabNote) -> DictLookup:
        return cls.try_lookup_word_or_name(vocab.get_question_without_noise_characters(), vocab.readings.get())

    @classmethod
    def try_lookup_word_or_name(cls, word: str, readings: list[str]) -> DictLookup:
        return cls._try_lookup_word_or_name(word, tuple(readings))

    @classmethod
    @cache
    def _try_lookup_word_or_name(cls, word: str, readings: tuple[str, ...]) -> DictLookup:
        if not cls.might_be_entry(word): return DictLookup([], word, [])

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
    @cache  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_word(cls, word: str) -> list[JMDEntry]:
        if not cls.might_be_word(word): return []

        entries = list(_jamdict_threading_wrapper.lookup(word, lookup_chars=False, lookup_ne=False).entries)
        return entries if not kana_utils.is_only_kana(word) else [ent for ent in entries if cls._is_kana_only(ent)]

    @classmethod
    @cache  # _lookup_word_shallow.cache_clear(), _lookup_word_shallow.cache_info()
    def _lookup_name(cls, word: str) -> list[JMDEntry]:
        if not cls.might_be_name(word): return []
        return list(_jamdict_threading_wrapper.lookup(word, lookup_ne=True, lookup_chars=False).names)

    @staticmethod
    def _is_kana_only(entry: JMDEntry) -> bool:
        return not entry.kanji_forms or any(sense for sense
                                            in entry.senses
                                            if "word usually written using kana alone" in sense.misc)

    @classmethod
    def might_be_word(cls, word: str) -> bool:
        # this method is a pure optimization to save on dictionary calls during real runtime. During tests populating all the words is a suboptimization, so just always return true when testing
        return app.is_testing() or word in _all_word_forms.instance()

    @classmethod
    def might_be_name(cls, word: str) -> bool:
        # this method is a pure optimization to save on dictionary calls during real runtime. During tests populating all the words is a suboptimization, so just always return true when testing
        return app.is_testing() or word in _all_name_forms.instance()

    @classmethod
    def might_be_entry(cls, word: str) -> bool:
        return cls.might_be_word(word) or cls.might_be_name(word)

    @classmethod
    @cache
    def is_word(cls, word: str) -> bool:
        return cls.might_be_word(word) and cls.lookup_word_shallow(word).found_words()

    @classmethod
    @cache
    def is_dictionary_or_collection_word(cls, word: str) -> bool:
        from ankiutils import app
        return app.col().vocab.is_word(word) or cls.is_word(word)

    @classmethod
    def ensure_loaded_into_memory(cls) -> None:
        cls._lookup_name("桜")
        cls._lookup_word("俺")
