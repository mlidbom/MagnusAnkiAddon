from __future__ import annotations

from typing import TYPE_CHECKING

from jaslib.note.jpnote_data import JPNoteData

if TYPE_CHECKING:
    from anki.notes import Note


class JPNoteDataShim:
    @classmethod
    def from_note(cls, note: Note) -> JPNoteData:
        fields: dict[str, str] = {}
        for name in note._fmap:  # pyright: ignore [reportPrivateUsage]
            fields[name] = note[name]

        return JPNoteData(note.id, fields, note.tags)