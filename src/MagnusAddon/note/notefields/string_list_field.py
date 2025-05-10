from __future__ import annotations

from note.jpnote import JPNote
from note.notefields.string_field import StringField
from sysutils import ex_str

class StringListField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> list[str]: return ex_str.extract_comma_separated_values(self._field.get())
    def set(self, value: list[str]) -> None: self._field.set(ex_str.to_comma_separated_values(value))
