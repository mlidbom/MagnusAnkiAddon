from __future__ import annotations

from typing import TYPE_CHECKING, override

from anki.notes import Note
from jaslib.note.backend_note_creator import IBackendNoteCreator
from jaslib.note.note_constants import NoteTypes
from jastudio.ankiutils import app
from jastudio.note.jpnotedata_shim import JPNoteDataShim

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNote, JPNoteId
    from jaslib.note.kanjinote import KanjiNote
    from jaslib.note.sentences.sentencenote import SentenceNote
    from jaslib.note.vocabulary.vocabnote import VocabNote

class AnkiBackendNoteCreator(IBackendNoteCreator):
    @classmethod
    def _create_note(cls, note: JPNote, note_type: str) -> JPNoteId:
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(note_type))
        JPNoteDataShim.set_note_data(backend_note, note.get_data())
        app.anki_collection().addNote(backend_note)
        return backend_note.id

    @override
    def create_kanji(self, note: KanjiNote) -> JPNoteId:
        return self._create_note(note, NoteTypes.Kanji)

    @override
    def create_vocab(self, note: VocabNote) -> JPNoteId:
        return self._create_note(note, NoteTypes.Vocab)

    @override
    def create_sentence(self, note: SentenceNote) -> JPNoteId:
        return self._create_note(note, NoteTypes.Sentence)
