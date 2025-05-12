from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.string_field import StringField
from sysutils import ex_str

if TYPE_CHECKING:
    from note.jpnote import JPNote

class CommaSeparatedStringsListField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> list[str]:
        return ex_str.extract_comma_separated_values(self._field.get())

    def set(self, value: list[str]) -> None:
        self._field.set(", ".join(value))

    def get_raw_string(self) -> str:
        return self._field.get()
