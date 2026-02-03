from __future__ import annotations

from typing import TYPE_CHECKING, override

from anki.notes import Note
from jaslib.note.backend_note_creator import IBackendNoteCreator
from jaslib.note.note_constants import NoteTypes
from jastudio.anki_extentions.note_ex import NoteEx
from jastudio.ankiutils import app

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNoteId
    from jaslib.note.kanjinote import KanjiNote
    from jaslib.note.sentences.sentencenote import SentenceNote
    from jaslib.note.vocabulary.vocabnote import VocabNote

class AnkiBackendNoteCreator(IBackendNoteCreator):
    @override
    def create_kanji(self, note: KanjiNote) -> JPNoteId:
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Kanji))
        app.anki_collection().add_note(backend_note, NoteEx(backend_note).note_type.deck_id)
        return backend_note.id

    @override
    def create_vocab(self, note: VocabNote) -> JPNoteId:
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        app.anki_collection().add_note(backend_note, NoteEx(backend_note).note_type.deck_id)
        return backend_note.id

    @override
    def create_sentence(self, note: SentenceNote) -> JPNoteId:
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Sentence))
        app.anki_collection().add_note(backend_note, NoteEx(backend_note).note_type.deck_id)
        return backend_note.id
