from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from autoslot import Slots
from JAStudio.Core import App, MyLog
from JAStudio.Core.Note import JPNote, KanjiNote, Mine, NoteTypes, SentenceNote, VocabNote
from JAStudio.Core.TaskRunners import TaskRunner
from jaspythonutils.sysutils.memory_usage import string_auto_interner
from jaspythonutils.sysutils.timeutil import StopWatch
from jaspythonutils.sysutils.typed import non_optional
from jaspythonutils.sysutils.weak_ref import WeakRefable
from jastudio.anki_extentions.note_bulk_loader import NoteBulkLoader
from jastudio.ankiutils import app
from jastudio.note import studing_status_helper
from jastudio.note.anki_backend_note_creator import AnkiBackendNoteCreator
from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner
from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer
from jastudio.note.jpnotedata_shim import JPNoteDataShim
from jastudio.sysutils import app_thread_pool
from jastudio.sysutils.memory_usage.ex_trace_malloc import ex_trace_malloc_instance

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import NoteId

class AnkiJPCollectionSyncer(WeakRefable, Slots):
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
        if app.config().load_studio_in_foreground.get_value():
            app_thread_pool.run_on_ui_thread_synchronously(self._initialize)
        else:
            self._initialize()

    def _initialize(self) -> None:
        if self._initialization_started:
            return
        self._initialization_started = True
        App.Reset(AnkiBackendNoteCreator())
        string_auto_interner.try_enable()
        MyLog.Info("AnkiJPCollection.__init__")
        if self._pending_init_timer is not None:
            self._pending_init_timer.cancel()
        ex_trace_malloc_instance.ensure_initialized()
        stopwatch = StopWatch()
        with StopWatch.log_warning_if_slower_than(5, "Full collection setup"):  # noqa: SIM117
            with TaskRunner.Current(f"Loading {Mine.app_name}", "reading notes from anki",
                                    forceHide=not app.config().load_studio_in_foreground.get_value(),
                                    forceGc=not AnkiJPCollectionSyncer._is_inital_load,
                                    allowCancel=False) as task_runner:
                if task_runner.IsHidden():
                    app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)

                with StopWatch.log_warning_if_slower_than(5, "Core collection setup - no gc"):
                    self._cache_runner = AnkiCollectionSyncRunner(self.anki_collection)

                    all_vocab = NoteBulkLoader.load_all_notes_of_type(self.anki_collection, NoteTypes.Vocab)
                    self._vocab = AnkiSingleCollectionSyncer[VocabNote](all_vocab, VocabNote, VocabNote, App.Col().Vocab.cache, self._cache_runner)

                    all_kanji = NoteBulkLoader.load_all_notes_of_type(self.anki_collection, NoteTypes.Sentence)
                    self._sentences = AnkiSingleCollectionSyncer[SentenceNote](all_kanji, SentenceNote, SentenceNote, App.Col().Sentences.cache, self._cache_runner)

                    all_sentences = NoteBulkLoader.load_all_notes_of_type(self.anki_collection, NoteTypes.Kanji)
                    self._kanji = AnkiSingleCollectionSyncer[KanjiNote](all_sentences, KanjiNote, KanjiNote, App.Col().Kanji.cache, self._cache_runner)

                self._cache_runner.start()

                if app.config().load_jamdict_db_into_memory.get_value():
                    from JAStudio.Core.LanguageServices.JamdictEx import DictLookup
                    task_runner.RunOnBackgroundThreadWithSpinningProgressDialog("Loading Jamdict db into memory", DictLookup.EnsureLoadedIntoMemory)

                studying_statuses = studing_status_helper.fetch_card_studying_statuses(self.anki_collection)
                self._vocab.set_studying_statuses([it for it in studying_statuses if it.note_type_name == NoteTypes.Vocab])
                self._sentences.set_studying_statuses([it for it in studying_statuses if it.note_type_name == NoteTypes.Sentence])
                self._kanji.set_studying_statuses([it for it in studying_statuses if it.note_type_name == NoteTypes.Kanji])

                ex_trace_malloc_instance.log_memory_delta("Done loading add-on")
                ex_trace_malloc_instance.stop()

                self._is_initialized = True
                AnkiJPCollectionSyncer._is_inital_load = False

            app.get_ui_utils().tool_tip(f"{Mine.app_name} done loading in {str(stopwatch.elapsed_seconds())[0:4]} seconds.", milliseconds=6000)

    @property
    def cache_runner(self) -> AnkiCollectionSyncRunner: return non_optional(self._initialized_self()._cache_runner)
    @property
    def is_initialized(self) -> bool: return self._is_initialized

    @classmethod
    def note_from_note_id(cls, note_id: NoteId) -> JPNote:
        col = App.Col()
        return (col.Kanji.WithIdOrNone(note_id)
                or col.Vocab.WithIdOrNone(note_id)
                or col.Sentences.WithIdOrNone(note_id)
                or JPNote(JPNoteDataShim.from_note(app.anki_collection().get_note(note_id))))

    def destruct_sync(self) -> None:
        if self._pending_init_timer is not None: self._pending_init_timer.cancel()
        if self._is_initialized:
            self.cache_runner.destruct()
            self._is_initialized = False

    def flush_cache_updates(self) -> None: self.cache_runner.flush_updates()
