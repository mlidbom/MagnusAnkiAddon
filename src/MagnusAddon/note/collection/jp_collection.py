from __future__ import annotations

import threading

import mylog
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.collection.kanji_collection import KanjiCollection
from note.collection.sentence_collection import SentenceCollection
from note.collection.vocab_collection import VocabCollection
from sysutils.memory_usage import string_auto_interner
from sysutils.memory_usage.ex_trace_malloc import ex_trace_malloc_instance
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRefable


class JPCollection(WeakRefable, Slots):
    _is_inital_load: bool = True  # running the GC on initial load slows startup a lot but does not decrease memory usage in any significant way.

    def __init__(self, delay_seconds: float | None = None) -> None:
        from sysutils.object_instance_tracker import ObjectInstanceTracker
        self._instance_tracker: ObjectInstanceTracker = ObjectInstanceTracker.tracker_for(self)
        self._is_initialized: bool = False
        self._initialization_started: bool = False

        self._vocab: VocabCollection | None = None
        self._kanji: KanjiCollection | None = None
        self._sentences: SentenceCollection | None = None
        self._pending_init_timer: threading.Timer | None = None
        if delay_seconds is not None:
            self._pending_init_timer = threading.Timer(delay_seconds or 0, self._initialize_wrapper)
            self._pending_init_timer.start()
        else:
            self._initialize()

    def reshchedule_init_for(self, delay_seconds: float) -> None:
        if self._initialization_started: return
        if self._pending_init_timer is None: raise AssertionError("Pending init timer is None")
        self._pending_init_timer.cancel()
        self._pending_init_timer = threading.Timer(delay_seconds, self._initialize_wrapper)

    def _initialized_self(self) -> JPCollection:
        if not self._is_initialized:
            self._initialize()
        return self

    def _initialize_wrapper(self) -> None:
        self._initialize()

    def _initialize(self) -> None:
        if self._initialization_started:
            return
        self._initialization_started = True
        string_auto_interner.try_enable()
        mylog.info("JPCollection.__init__")
        if self._pending_init_timer is not None:
            self._pending_init_timer.cancel()
        ex_trace_malloc_instance.ensure_initialized()

        self._vocab = VocabCollection()
        self._sentences = SentenceCollection()
        self._kanji = KanjiCollection()

        ex_trace_malloc_instance.log_memory_delta("Done loading add-on")
        ex_trace_malloc_instance.stop()

        self._is_initialized = True
        JPCollection._is_inital_load = False

    @property
    def is_initialized(self) -> bool: return self._is_initialized
    @property
    def vocab(self) -> VocabCollection: return non_optional(self._initialized_self()._vocab)
    @property
    def kanji(self) -> KanjiCollection: return non_optional(self._initialized_self()._kanji)
    @property
    def sentences(self) -> SentenceCollection: return non_optional(self._initialized_self()._sentences)



    def destruct_sync(self) -> None:
        if self._pending_init_timer is not None: self._pending_init_timer.cancel()
        if self._is_initialized:
            self._is_initialized = False
