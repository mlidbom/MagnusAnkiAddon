from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from autoslot import Slots
from jaspythonutils.sysutils.memory_usage import string_auto_interner
from jaspythonutils.sysutils.timeutil import StopWatch
from jaspythonutils.sysutils.typed import non_optional
from jastudio import mylog
from jastudio.ankiutils import app
from JAStudio.Core.Note import Mine
from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner
from jastudio.sysutils import app_thread_pool
from jastudio.sysutils.memory_usage.ex_trace_malloc import ex_trace_malloc_instance
from jastudio.task_runners.task_progress_runner import TaskRunner
from jastudio.ui import dotnet_ui_root

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import NoteId
    from JAStudio.Core.Note import JPNote, KanjiNote, SentenceNote, VocabNote
    from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer

class AnkiJPCollectionSyncer(Slots):
    _is_inital_load: bool = True  # running the GC on initial load slows startup a lot but does not decrease memory usage in any significant way.

    def __init__(self, anki_collection: Collection, delay_seconds: float | None = None) -> None:
        from jastudio.sysutils.object_instance_tracker import ObjectInstanceTracker
        self._instance_tracker: ObjectInstanceTracker = ObjectInstanceTracker.tracker_for(self)
        self.anki_collection: Collection = anki_collection
        self._is_initialized: bool = False
        self._initialization_started: bool = False
        self._cache_runner: AnkiCollectionSyncRunner | None = None

        self._vocab: AnkiSingleCollectionSyncer[VocabNote] | None = None
        self._kanji: AnkiSingleCollectionSyncer[KanjiNote] | None = None
        self._sentences: AnkiSingleCollectionSyncer[SentenceNote] | None = None
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

    def _initialized_self(self) -> AnkiJPCollectionSyncer:
        if not self._is_initialized:
            self._initialize()
        return self

    def _initialize_wrapper(self) -> None:
        if app.config().LoadStudioInForeground.GetValue():
            app_thread_pool.run_on_ui_thread_synchronously(self._initialize)
        else:
            self._initialize()

    def _initialize(self) -> None:
        if self._initialization_started:
            return

        dotnet_ui_root.Start()
        self._initialization_started = True
        #todo migration
        #jaslibapp.reset(AnkiBackendNoteCreator())
        string_auto_interner.try_enable()
        mylog.info("AnkiJPCollection.__init__")
        if self._pending_init_timer is not None:
            self._pending_init_timer.cancel()
        ex_trace_malloc_instance.ensure_initialized()
        stopwatch = StopWatch()
        with StopWatch.log_warning_if_slower_than(5, "Full collection setup"):  # noqa: SIM117
            with TaskRunner.current(f"Loading {Mine.AppName}", "reading notes from anki",
                                    force_hide=not app.config().LoadStudioInForeground.GetValue(),
                                    force_gc=not AnkiJPCollectionSyncer._is_inital_load,
                                    allow_cancel=False) as task_runner:
                if task_runner.is_hidden():
                    app.get_ui_utils().tool_tip(f"{Mine.AppName} loading", 60000)

                with StopWatch.log_warning_if_slower_than(5, "Core collection setup - no gc"):
                    self._cache_runner = AnkiCollectionSyncRunner(self.anki_collection)


                    #todo migration hook in note syncing here
                    # self._vocab = AnkiSingleCollectionSyncer[VocabNote](VocabNote, VocabNote, jaslibapp.col().vocab.cache, self._cache_runner)
                    # self._sentences = AnkiSingleCollectionSyncer[SentenceNote](SentenceNote, SentenceNote, jaslibapp.col().sentences.cache, self._cache_runner)
                    # self._kanji = AnkiSingleCollectionSyncer[KanjiNote](KanjiNote, KanjiNote, jaslibapp.col().kanji.cache, self._cache_runner)

                self._cache_runner.start()

                ex_trace_malloc_instance.log_memory_delta("Done loading add-on")
                ex_trace_malloc_instance.stop()

                self._is_initialized = True
                AnkiJPCollectionSyncer._is_inital_load = False

            app.get_ui_utils().tool_tip(f"{Mine.AppName} done loading in {str(stopwatch.elapsed_seconds())[0:4]} seconds.", milliseconds=6000)

    @property
    def cache_runner(self) -> AnkiCollectionSyncRunner: return non_optional(self._initialized_self()._cache_runner)
    @property
    def is_initialized(self) -> bool: return self._is_initialized

    # noinspection PyTypeHints
    @classmethod
    def note_from_note_id(cls, note_id: NoteId) -> JPNote | None:
        dotnet_ui_root.Services.App.Collection.NoteFromNoteId(note_id)

    def destruct_sync(self) -> None:
        if self._pending_init_timer is not None: self._pending_init_timer.cancel()
        if self._is_initialized:
            self.cache_runner.destruct()
            dotnet_ui_root.ShutDown()
            self._is_initialized = False

    def flush_cache_updates(self) -> None: self.cache_runner.flush_updates()
