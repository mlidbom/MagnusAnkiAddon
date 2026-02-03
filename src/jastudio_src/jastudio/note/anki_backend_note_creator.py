from __future__ import annotations

from typing import TYPE_CHECKING, override

from anki.notes import Note
from jaslib.note.backend_note_creator import IBackendNoteCreator
from jaslib.note.note_constants import NoteTypes
from jastudio.ankiutils import app
from jastudio.note import studing_status_helper
from jastudio.note.jpnotedata_shim import JPNoteDataShim

if TYPE_CHECKING:
    from collections.abc import Callable

    from jaslib.note.jpnote import JPNote
    from jaslib.note.kanjinote import KanjiNote
    from jaslib.note.sentences.sentencenote import SentenceNote
    from jaslib.note.vocabulary.vocabnote import VocabNote

class AnkiBackendNoteCreator(IBackendNoteCreator):
    @classmethod
    def _create_note(cls, note: JPNote, note_type: str, callback: Callable[[], None]) -> None:
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(note_type))
        JPNoteDataShim.sync_note_to_anki_note(note, backend_note)
        app.anki_collection().addNote(backend_note)
        note.set_id(backend_note.id)
        callback()
        studing_status_helper.update_note_in_studying_cache(backend_note)

    @override
    def create_kanji(self, note: KanjiNote, callback: Callable[[], None]) -> None:
        self._create_note(note, NoteTypes.Kanji, callback)

    @override
    def create_vocab(self, note: VocabNote, callback: Callable[[], None]) -> None:
        self._create_note(note, NoteTypes.Vocab, callback)

    @override
    def create_sentence(self, note: SentenceNote, callback: Callable[[], None]) -> None:
        self._create_note(note, NoteTypes.Sentence, callback)
