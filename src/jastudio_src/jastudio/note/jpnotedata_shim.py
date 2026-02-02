from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anki.notes import Note
    from jaslib.note.jpnote_data import JPNoteData


class JPNoteDataShim:
    @classmethod
    def from_note(cls, note: Note) -> JPNoteData:  # pyright: ignore
        raise NotImplementedError()