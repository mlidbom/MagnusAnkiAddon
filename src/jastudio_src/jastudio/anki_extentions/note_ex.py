from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import NoteId

from jastudio.ankiutils import app

if TYPE_CHECKING:
    from anki.notes import Note

    from jastudio.anki_extentions.card_ex import CardEx

class NoteEx:
    def __init__(self, note: Note) -> None:
        self.note: Note = note

    @property
    def id(self) -> NoteId: return self.note.id

    def cards(self) -> list[CardEx]:
        from jastudio.anki_extentions.card_ex import CardEx
        return [CardEx(card) for card in self.note.cards()]

    def suspend_all_cards(self) -> None:
        for card in self.cards(): card.suspend()

    def un_suspend_all_cards(self) -> None:
        for card in self.cards(): card.un_suspend()

    @classmethod
    def from_id(cls, note_id: int) -> NoteEx:
        return NoteEx(app.anki_collection().get_note(NoteId(note_id)))
