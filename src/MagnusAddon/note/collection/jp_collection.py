from __future__ import annotations

import threading
from typing import TYPE_CHECKING

import mylog
from ankiutils import app
from autoslot import Slots
from note import noteutils
from note.collection.cache_runner import CacheRunner
from note.collection.kanji_collection import KanjiCollection
from note.collection.sentence_collection import SentenceCollection
from note.collection.vocab_collection import VocabCollection
from note.jpnote import JPNote
from note.note_constants import Mine
from qt_utils.task_runner_progress_dialog import TaskRunner
from sysutils import app_thread_pool
from sysutils.timeutil import StopWatch
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import NoteId

class JPCollection(WeakRefable, Slots):
    _is_inital_load: bool = True  # running the GC on initial load slows startup a lot but does not decrease memory usage in any significant way.
    def __init__(self, anki_collection: Collection, delay_seconds: float | None = None) -> None:
        from sysutils.object_instance_tracker import ObjectInstanceTracker
        self._instance_tracker: ObjectInstanceTracker = ObjectInstanceTracker.tracker_for(self)
        self.anki_collection: Collection = anki_collection
        self._is_initialized: bool = False
        self._initialization_started: bool = False
        self._cache_runner: CacheRunner | None = None

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
        if app.config().load_studio_in_foreground.get_value():
            app_thread_pool.run_on_ui_thread_synchronously(self._initialize)
        else:
            self._initialize()

    def _initialize(self) -> None:
        if self._initialization_started:
            return
        self._initialization_started = True
        mylog.info("JPCollection.__init__")
        if self._pending_init_timer is not None:
            self._pending_init_timer.cancel()
        app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)
        stopwatch = StopWatch()
        with StopWatch.log_warning_if_slower_than(5, "Full collection setup"):
            task_runner = TaskRunner.create(f"Loading {Mine.app_name}", "reading notes from anki", not app.is_testing() and app.config().load_studio_in_foreground.get_value())
            if not app.is_testing() and not JPCollection._is_inital_load:
                task_runner.set_label_text("Running garbage collection")
                self._instance_tracker.run_gc_if_multiple_instances_and_assert_single_instance_after_gc()
                app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)

            with StopWatch.log_warning_if_slower_than(5, "Core collection setup - no gc"):
                self._cache_runner = CacheRunner(self.anki_collection)

                self._kanji = KanjiCollection(self.anki_collection, self._cache_runner, task_runner)
                self._vocab = VocabCollection(self.anki_collection, self._cache_runner, task_runner)
                self._sentences = SentenceCollection(self.anki_collection, self._cache_runner, task_runner)

            self._cache_runner.start()

            if app.config().load_jamdict_db_into_memory.get_value():
                task_runner.set_label_text("Loading Jamdict db into memory")
                from language_services.jamdict_ex.dict_lookup import DictLookup
                DictLookup.ensure_loaded_into_memory()

            if app.config().pre_cache_card_studying_status.get_value():
                noteutils.initialize_studying_cache(self.anki_collection, task_runner)

            if not app.is_testing() and not JPCollection._is_inital_load:
                self._instance_tracker.run_gc_if_multiple_instances_and_assert_single_instance_after_gc()

            self._is_initialized = True
            JPCollection._is_inital_load = False

            task_runner.close()
            app.get_ui_utils().tool_tip(f"{Mine.app_name} done loading in {str(stopwatch.elapsed_seconds())[0:4]} seconds.", milliseconds=6000)

    @property
    def cache_runner(self) -> CacheRunner: return non_optional(self._initialized_self()._cache_runner)
    @property
    def is_initialized(self) -> bool: return self._is_initialized
    @property
    def vocab(self) -> VocabCollection: return non_optional(self._initialized_self()._vocab)
    @property
    def kanji(self) -> KanjiCollection: return non_optional(self._initialized_self()._kanji)
    @property
    def sentences(self) -> SentenceCollection: return non_optional(self._initialized_self()._sentences)

    @classmethod
    def note_from_note_id(cls, note_id: NoteId) -> JPNote:
        col = app.col()
        return (col.kanji.with_id_or_none(note_id)
                or col.vocab.with_id_or_none(note_id)
                or col.sentences.with_id_or_none(note_id)
                or JPNote(app.anki_collection().get_note(note_id)))

    def destruct_sync(self) -> None:
        if self._pending_init_timer is not None: self._pending_init_timer.cancel()
        if self._is_initialized:
            self.cache_runner.destruct()
            self._is_initialized = False

    def flush_cache_updates(self) -> None: self.cache_runner.flush_updates()
