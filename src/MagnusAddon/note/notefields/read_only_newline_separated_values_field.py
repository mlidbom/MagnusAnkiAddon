from __future__ import annotations

from note.jpnote import JPNote
from note.notefields.string_note_field import StringField
from sysutils import ex_str

class ReadOnlyNewlineSeparatedValuesField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> list[str]: return ex_str.extract_newline_separated_values(self._field.get())
