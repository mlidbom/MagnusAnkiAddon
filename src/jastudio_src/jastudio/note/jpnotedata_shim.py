from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.note.jpnote_data import JPNoteData
from jaslib.sysutils.typed import non_optional

if TYPE_CHECKING:
    from anki.notes import Note


class JPNoteDataShim:
    @classmethod
    def from_note(cls, note: Note) -> JPNoteData:  # pyright: ignore
        fields: dict[str, str] = {}
        for name in non_optional(note.note_type()):
            fields[name] = note[name]

        return JPNoteData(note.id, fields, note.tags)