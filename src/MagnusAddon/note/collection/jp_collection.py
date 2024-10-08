from __future__ import annotations

from anki.collection import Collection
from anki.notes import NoteId

from note.collection.kanji_collection import KanjiCollection
from note.collection.radical_collection import RadicalCollection
from note.collection.sentence_collection import SentenceCollection
from note.collection.vocab_collection import VocabCollection
from note.jpnote import JPNote
from note.note_constants import NoteTypes
from sysutils import progress_display_runner

class JPCollection:
    def __init__(self, anki_collection: Collection):
        self.anki_collection = anki_collection

        spinner = progress_display_runner.open_spinning_progress_dialog("Loading caches")
        try:
            self.vocab:VocabCollection = VocabCollection(anki_collection)
            self.kanji:KanjiCollection = KanjiCollection(anki_collection, self)
            self.sentences:SentenceCollection = SentenceCollection(anki_collection)
            self.radicals:RadicalCollection = RadicalCollection(anki_collection)
        finally:
            spinner.close()

    def unsuspend_note_cards(self, note: JPNote, name: str) -> None:
        print("Unsuspending {}: {}".format(JPNote.get_note_type_name(note), name))
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

    def destruct(self) -> None:
        self.vocab.destruct()
        self.kanji.destruct()
        self.sentences.destruct()
        self.radicals.destruct()

    def flush_cache_updates(self) -> None:
        self.vocab.flush_cache_updates()
        self.kanji.flush_cache_updates()
        self.sentences.flush_cache_updates()
        self.radicals.flush_cache_updates()

    def pause_cache_updates(self) -> None:
        self.vocab.pause_cache_updates()
        self.kanji.pause_cache_updates()
        self.sentences.pause_cache_updates()
        self.radicals.pause_cache_updates()

    def resume_cache_updates(self) -> None:
        self.vocab.resume_cache_updates()
        self.kanji.resume_cache_updates()
        self.sentences.resume_cache_updates()
        self.radicals.resume_cache_updates()