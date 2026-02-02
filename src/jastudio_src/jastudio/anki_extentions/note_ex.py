from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import NoteId as AnkiNoteId
from jastudio.anki_extentions.card_ex import CardEx
from jastudio.ankiutils import app

if TYPE_CHECKING:
    from anki.notes import Note
    from jaslib.note.jpnote import JPNote, JPNoteId

class NoteEx:
    def __init__(self, note: Note) -> None:
        self.note: Note = note

    @property
    def id(self) -> AnkiNoteId: return self.note.id

    def cards(self) -> list[CardEx]:
        return [CardEx(card) for card in self.note.cards()]

    def suspend_all_cards(self) -> None:
        for card in self.cards(): card.suspend()

    def un_suspend_all_cards(self) -> None:
        for card in self.cards(): card.un_suspend()

    def has_suspended_cards(self) -> bool:
        return any(_card for _card in self.cards() if _card.is_suspended())

    def has_active_cards(self) -> bool:
        return any(_card for _card in self.cards() if not _card.is_suspended())

    @classmethod
    def from_id(cls, note_id: JPNoteId) -> NoteEx:
        return NoteEx(app.anki_collection().get_note(AnkiNoteId(note_id)))

    @classmethod
    def from_anki_id(cls, note_id: AnkiNoteId) -> NoteEx:
        return NoteEx(app.anki_collection().get_note(note_id))

    @classmethod
    def from_anki_note(cls, note: Note) -> NoteEx:
        return NoteEx(note)

    @classmethod
    def from_note(cls, note: JPNote) -> NoteEx:
        return cls.from_id(note.get_id())
