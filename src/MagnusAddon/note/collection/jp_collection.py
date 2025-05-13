from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from note.collection.cache_runner import CacheRunner
from note.collection.kanji_collection import KanjiCollection
from note.collection.radical_collection import RadicalCollection
from note.collection.sentence_collection import SentenceCollection
from note.collection.vocab_collection import VocabCollection
from note.jpnote import JPNote
from note.note_constants import NoteTypes
from sysutils import app_thread_pool
from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.timeutil import StopWatch

if TYPE_CHECKING:
    from asyncio import Future

    from anki.collection import Collection
    from anki.notes import NoteId


class JPCollection:
    def __init__(self, anki_collection: Collection) -> None:
        with StopWatch.log_warning_if_slower_than(5, "Full collection setup"):
            self.instance_tracker = ObjectInstanceTracker(JPCollection)

            if not app.is_testing():
                self.instance_tracker.run_gc_and_assert_single_instance()

            with StopWatch.log_warning_if_slower_than(5, "Core collection setup - no gc"):
                self.anki_collection = anki_collection
                self.cache_manager = CacheRunner(anki_collection)

                from language_services.jamdict_ex.dict_lookup import DictLookup
                dictlookup_loading:Future[None] = app_thread_pool.pool.submit(DictLookup.ensure_loaded_into_memory) #doesn't really belong here but it works to speed up loading for user experience

                self.vocab:VocabCollection = VocabCollection(anki_collection, self.cache_manager)
                self.kanji:KanjiCollection = KanjiCollection(anki_collection, self, self.cache_manager)
                self.sentences:SentenceCollection = SentenceCollection(anki_collection, self.cache_manager)
                self.radicals:RadicalCollection = RadicalCollection(anki_collection, self.cache_manager)

                dictlookup_loading.result()

            if not app.is_testing():
                self.instance_tracker.run_gc_and_assert_single_instance()

            self.cache_manager.start()

    def unsuspend_note_cards(self, note: JPNote, name: str) -> None:
        print(f"Unsuspending {JPNote.get_note_type_name(note)}: {name}")
        self.anki_collection.sched.unsuspend_cards(note.card_ids())

    @classmethod
    def note_from_note_id(cls, note_id: NoteId) -> JPNote:
        note = app.anki_collection().get_note(note_id) #todo: verify wether calling get_note is slow, if so hack this into the in memory caches instead

        if JPNote.get_note_type(note) == NoteTypes.Kanji: return app.col().kanji.with_id(note.id)
        elif JPNote.get_note_type(note) == NoteTypes.Vocab: return app.col().vocab.with_id(note.id)
        elif JPNote.get_note_type(note) == NoteTypes.Radical: return app.col().radicals.with_id(note.id)
        elif JPNote.get_note_type(note) == NoteTypes.Sentence: return app.col().sentences.with_id(note.id)
        return JPNote(note)

    def destruct(self) -> None: self.cache_manager.destruct()

    def flush_cache_updates(self) -> None: self.cache_manager.flush_updates()
    def pause_cache_updates(self) -> None: self.cache_manager.pause_data_generation()
    def resume_cache_updates(self) -> None: self.cache_manager.resume_data_generation()
