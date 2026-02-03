from __future__ import annotations

from typing import TYPE_CHECKING, cast

from anki.models import NotetypeDict
from autoslot import Slots
from jaslib.note.jpnote import JPNote
from jaslib.note.note_constants import NoteTypes
from jaspythonutils.sysutils.typed import str_
from jaspythonutils.sysutils.weak_ref import WeakRefable
from jastudio.note.jpnotedata_shim import JPNoteDataShim

if TYPE_CHECKING:
    from anki.cards import Card
    from anki.notes import Note

class AnkiJPNote(WeakRefable, Slots):
    @classmethod
    def note_from_card(cls, card: Card) -> JPNote:
        note = card.note()
        return cls.note_from_note(note)

    @classmethod
    def note_from_note(cls, note: Note) -> JPNote:
        from jaslib.note.kanjinote import KanjiNote
        from jaslib.note.sentences.sentencenote import SentenceNote
        from jaslib.note.vocabulary.vocabnote import VocabNote

        data = JPNoteDataShim.from_note(note)

        if cls.get_note_type(note) == NoteTypes.Kanji: return KanjiNote(data)
        if cls.get_note_type(note) == NoteTypes.Vocab: return VocabNote(data)
        if cls.get_note_type(note) == NoteTypes.Sentence: return SentenceNote(data)
        return JPNote(data)

    @classmethod
    def get_note_type(cls, note: Note) -> str:
        return str_(cast(NotetypeDict, note.note_type())["name"])  # pyright: ignore[reportAny]