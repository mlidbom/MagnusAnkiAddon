from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import ex_str

if TYPE_CHECKING:
    from note.jpnote import JPNote

class StringField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._note = note
        self._field_name = field_name
        self._value = note.get_field(field_name)

    def set(self, value:str) -> None:
        self._note.set_field(self._field_name, value)

    def get(self) -> str: return self._note.get_field(self._field_name)

class StringListField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> list[str]: return ex_str.extract_comma_separated_values(self._field.get())
    def set(self, value:list[str]) -> None: self._field.set(ex_str.to_comma_separated_values(value))

class StringSetField:
    def __init__(self, note:JPNote, field_name:str) -> None:
        self._field = StringListField(note, field_name)

    def get(self) -> set[str]: return set(self._field.get())
    def set(self, value:set[str]) -> None: self._field.set(list(value))


