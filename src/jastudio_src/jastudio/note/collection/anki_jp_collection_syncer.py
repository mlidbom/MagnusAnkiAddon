from __future__ import annotations

import threading
from typing import TYPE_CHECKING

import jaslib.app
from autoslot import Slots
from jaslib.note.jpnote import JPNote
from jaslib.note.kanjinote import KanjiNote
from jaslib.note.note_constants import Mine, NoteTypes
from jaslib.note.sentences.sentencenote import SentenceNote
from jaslib.note.vocabulary.vocabnote import VocabNote
from jaslib.sysutils.memory_usage import string_auto_interner
from jaslib.sysutils.timeutil import StopWatch
from jaslib.sysutils.typed import non_optional
from jaslib.sysutils.weak_ref import WeakRefable
from jastudio.anki_extentions.note_bulk_loader import NoteBulkLoader
from jastudio.ankiutils import app
from jastudio.note import noteutils
from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner
from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer
from jastudio.note.jpnotedata_shim import JPNoteDataShim
from jastudio.qt_utils.task_progress_runner import TaskRunner
from jastudio.sysutils import app_thread_pool
from jastudio.sysutils.memory_usage.ex_trace_malloc import ex_trace_malloc_instance

from jaslib import app as jaslibapp
from jaslib import mylog

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
        string_auto_interner.try_enable()
        mylog.info("AnkiJPCollection.__init__")
        if self._pending_init_timer is not None:
            self._pending_init_timer.cancel()
        ex_trace_malloc_instance.ensure_initialized()
        stopwatch = StopWatch()
        with StopWatch.log_warning_if_slower_than(5, "Full collection setup"):  # noqa: SIM117
            with TaskRunner.current(f"Loading {Mine.app_name}", "reading notes from anki",
                                    force_hide=not app.config().load_studio_in_foreground.get_value(),
                                    force_gc=not AnkiJPCollectionSyncer._is_inital_load,
                                    allow_cancel=False) as task_runner:
                if task_runner.is_hidden():
                    app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)

                with StopWatch.log_warning_if_slower_than(5, "Core collection setup - no gc"):
                    self._cache_runner = AnkiCollectionSyncRunner(self.anki_collection)

                    all_vocab = NoteBulkLoader.load_all_notes_of_type(self.anki_collection, NoteTypes.Vocab)
                    self._vocab: AnkiSingleCollectionSyncer[VocabNote] = AnkiSingleCollectionSyncer[VocabNote](all_vocab, VocabNote, VocabNote, jaslibapp.col().vocab.cache, self._cache_runner)

                    all_kanji = NoteBulkLoader.load_all_notes_of_type(self.anki_collection, NoteTypes.Sentence)
                    self._sentences: AnkiSingleCollectionSyncer[SentenceNote] = AnkiSingleCollectionSyncer[SentenceNote](all_kanji, SentenceNote, SentenceNote, jaslibapp.col().sentences.cache, self._cache_runner)

                    all_sentences = NoteBulkLoader.load_all_notes_of_type(self.anki_collection, NoteTypes.Sentence)
                    self._kanji: AnkiSingleCollectionSyncer[KanjiNote] = AnkiSingleCollectionSyncer[KanjiNote](all_sentences, KanjiNote, KanjiNote, jaslibapp.col().kanji.cache, self._cache_runner)

                self._cache_runner.start()

                if app.config().load_jamdict_db_into_memory.get_value():
                    from jaslib.language_services.jamdict_ex.dict_lookup import DictLookup
                    task_runner.run_on_background_thread_with_spinning_progress_dialog("Loading Jamdict db into memory", DictLookup.ensure_loaded_into_memory)

                studying_statuses = noteutils.fetch_card_studying_statuses(self.anki_collection)
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
        col = jaslib.app.col()
        return (col.kanji.with_id_or_none(note_id)
                or col.vocab.with_id_or_none(note_id)
                or col.sentences.with_id_or_none(note_id)
                or JPNote(JPNoteDataShim.from_note(app.anki_collection().get_note(note_id))))

    def destruct_sync(self) -> None:
        if self._pending_init_timer is not None: self._pending_init_timer.cancel()
        if self._is_initialized:
            self.cache_runner.destruct()
            self._is_initialized = False

    def flush_cache_updates(self) -> None: self.cache_runner.flush_updates()
