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
from note.note_constants import Mine, NoteTypes
from sysutils import app_thread_pool
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.timeutil import StopWatch

if TYPE_CHECKING:
    from asyncio import Future

    from anki.collection import Collection
    from anki.notes import NoteId

class JPCollection(Slots):
    __slots__ = ["__weakref__"]
    def __init__(self, anki_collection: Collection) -> None:
        self._instance_tracker: ObjectInstanceTracker = ObjectInstanceTracker.tracker_for(self)
        mylog.info("JPCollection.__init__")
        app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)
        with StopWatch.log_warning_if_slower_than(5, "Full collection setup"):
            if not app.is_testing():
                self._instance_tracker.run_gc_and_assert_single_instance()
                app.get_ui_utils().tool_tip(f"{Mine.app_name} loading", 60000)

            with StopWatch.log_warning_if_slower_than(5, "Core collection setup - no gc"):
                self.anki_collection = anki_collection
                self.cache_manager = CacheRunner(anki_collection)

                self.vocab: VocabCollection = VocabCollection(anki_collection, self.cache_manager)
                self.kanji: KanjiCollection = KanjiCollection(anki_collection, self.cache_manager)
                self.sentences: SentenceCollection = SentenceCollection(anki_collection, self.cache_manager)

            if not app.is_testing():
                self._instance_tracker.run_gc_and_assert_single_instance()

            self.cache_manager.start()
            app.get_ui_utils().tool_tip(f"{Mine.app_name} done loading.", milliseconds=6000)
            from language_services.jamdict_ex.dict_lookup import DictLookup
            app_thread_pool.pool.submit(DictLookup.ensure_loaded_into_memory)  # doesn't really belong here but it works to speed up loading for user experience

    @classmethod
    def note_from_note_id(cls, note_id: NoteId) -> JPNote:
        note = app.anki_collection().get_note(note_id)  # todo: verify wether calling get_note is slow, if so hack this into the in memory caches instead

        if JPNote.get_note_type(note) == NoteTypes.Kanji: return app.col().kanji.with_id(note.id)
        if JPNote.get_note_type(note) == NoteTypes.Vocab: return app.col().vocab.with_id(note.id)
        if JPNote.get_note_type(note) == NoteTypes.Sentence: return app.col().sentences.with_id(note.id)
        return JPNote(note)

    def destruct_sync(self) -> None:
        self.cache_manager.destruct()


    def flush_cache_updates(self) -> None: self.cache_manager.flush_updates()
    def pause_cache_updates(self) -> None: self.cache_manager.pause_data_generation()
    def resume_cache_updates(self) -> None: self.cache_manager.resume_data_generation()
