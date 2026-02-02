from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import NoteId as AnkiNoteId
from jaslib.sysutils.typed import non_optional
from jastudio.anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from jastudio.ankiutils import app

if TYPE_CHECKING:
    from anki.notes import Note
    from jaslib.note.jpnote import JPNote, JPNoteId
    from jastudio.anki_extentions.card_ex import CardEx

class NoteEx:
    def __init__(self, note: Note) -> None:
        self.note: Note = note

    @property
    def id(self) -> AnkiNoteId: return self.note.id

    @property
    def note_type(self) -> NoteTypeEx:
        return NoteTypeEx.from_dict(non_optional(self.note.note_type()))

    def cards(self) -> list[CardEx]:
        from jastudio.anki_extentions.card_ex import CardEx
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
