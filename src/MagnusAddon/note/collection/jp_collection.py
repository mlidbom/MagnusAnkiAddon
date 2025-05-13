from __future__ import annotations

from asyncio import Future
from typing import TYPE_CHECKING

from note.collection.cache_runner import CacheRunner
from note.collection.kanji_collection import KanjiCollection
from note.collection.radical_collection import RadicalCollection
from note.collection.sentence_collection import SentenceCollection
from note.collection.vocab_collection import VocabCollection
from note.jpnote import JPNote
from note.note_constants import NoteTypes
from sysutils import app_thread_pool
from sysutils.timeutil import StopWatch

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import NoteId


class JPCollection:
    def __init__(self, anki_collection: Collection) -> None:
        self.anki_collection = anki_collection
        self.cache_manager = CacheRunner(anki_collection)

        with StopWatch.log_warning_if_slower_than(0.01, message="######################################### starting up collection #############################################"):
            # let's speed things up by running this in parallel
            vocab_future: Future[VocabCollection] = app_thread_pool.pool.submit(lambda: VocabCollection(anki_collection, self.cache_manager))
            kanji_future: Future[KanjiCollection] = app_thread_pool.pool.submit(lambda: KanjiCollection(anki_collection, self, self.cache_manager))
            sentences_future: Future[SentenceCollection] = app_thread_pool.pool.submit(lambda: SentenceCollection(anki_collection, self.cache_manager))
            radicals_future: Future[RadicalCollection] = app_thread_pool.pool.submit(lambda: RadicalCollection(anki_collection, self.cache_manager))

            self.vocab: VocabCollection = vocab_future.result()
            self.kanji: KanjiCollection = kanji_future.result()
            self.sentences: SentenceCollection = sentences_future.result()
            self.radicals: RadicalCollection = radicals_future.result()

        self.cache_manager.start()

    def unsuspend_note_cards(self, note: JPNote, name: str) -> None:
        print(f"Unsuspending {JPNote.get_note_type_name(note)}: {name}")
        self.anki_collection.sched.unsuspend_cards(note.card_ids())

    @classmethod
    def note_from_note_id(cls, note_id: NoteId) -> JPNote:
        from ankiutils import app
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
