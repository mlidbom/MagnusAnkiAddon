from __future__ import annotations

from typing import TYPE_CHECKING

from JAStudio.Core.Note import JPNoteData

if TYPE_CHECKING:
    from anki.notes import Note
    from JAStudio.Core.Note import JPNote

class JPNoteDataShim:
    @classmethod
    def from_note(cls, note: Note) -> JPNoteData:
        fields: dict[str, str] = {}
        for name in note._fmap:  # pyright: ignore [reportPrivateUsage]
            fields[name] = note[name]

        return JPNoteData(note.id, fields, note.tags)


    @classmethod
    def sync_note_to_anki_note(cls, jp_note: JPNote, note: Note) -> None:
        data = jp_note.GetData()
        note.tags = data.tags
        for field_name, field_value in data.fields.items():
            note[field_name] = field_value
