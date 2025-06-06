from __future__ import annotations

from typing import TYPE_CHECKING

import mylog
from ankiutils import app
from autoslot import Slots
from note.collection.cache_runner import CacheRunner
from note.collection.kanji_collection import KanjiCollection
from note.collection.sentence_collection import SentenceCollection
from note.collection.vocab_collection import VocabCollection
from note.jpnote import JPNote
from note.note_constants import CardTypes, Mine
from sysutils import app_thread_pool
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.timeutil import StopWatch
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from collections.abc import Sequence

    from anki.collection import Collection
    from anki.notes import NoteId

class JPCollection(WeakRefable,Slots):
    def __init__(self, anki_collection: Collection) -> None:
        self._instance_tracker: ObjectInstanceTracker = ObjectInstanceTracker.tracker_for(self)
        mylog.info("JPCollection.__init__")
        app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)
        stopwatch = StopWatch()
        with StopWatch.log_warning_if_slower_than(5, "Full collection setup"):
            if not app.is_testing():
                self._instance_tracker.run_gc_and_assert_single_instance()
                app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)

            with StopWatch.log_warning_if_slower_than(5, "Core collection setup - no gc"):
                self.anki_collection = anki_collection
                self.cache_runner = CacheRunner(anki_collection)

                self.vocab: VocabCollection = VocabCollection(anki_collection, self.cache_runner)
                self.kanji: KanjiCollection = KanjiCollection(anki_collection, self.cache_runner)
                self.sentences: SentenceCollection = SentenceCollection(anki_collection, self.cache_runner)

            if not app.is_testing():
                self._instance_tracker.run_gc_and_assert_single_instance()

            self.cache_runner.start()
            app.get_ui_utils().tool_tip(f"{Mine.app_name} done loading in {str(stopwatch.elapsed_seconds())[0:4]} seconds.", milliseconds=6000)

            self._is_running = True
            self._populate_additional_caches_on_background_thread()

    def _populate_additional_caches_on_background_thread(self) -> None:
        def populate_caches() -> None:
            if not self._is_running: return
            from language_services.jamdict_ex.dict_lookup import DictLookup
            DictLookup.ensure_loaded_into_memory()

            with StopWatch.log_execution_time("Populating studying status cache"):
                def cache_notes_studying_status(notelist: Sequence[JPNote]) -> None:
                    for note in notelist:
                        if not self._is_running: return
                        note.is_studying(CardTypes.reading)
                        note.is_studying(CardTypes.listening)

                cache_notes_studying_status(self.vocab.all())
                cache_notes_studying_status(self.kanji.all())
                cache_notes_studying_status(self.sentences.all())

        app_thread_pool.pool.submit(populate_caches)

    @classmethod
    def note_from_note_id(cls, note_id: NoteId) -> JPNote:
        col = app.col()
        return (col.kanji.with_id_or_none(note_id)
                or col.vocab.with_id_or_none(note_id)
                or col.sentences.with_id_or_none(note_id)
                or JPNote(app.anki_collection().get_note(note_id)))

    def destruct_sync(self) -> None:
        self._is_running = False
        self.cache_runner.destruct()

    def flush_cache_updates(self) -> None: self.cache_runner.flush_updates()
