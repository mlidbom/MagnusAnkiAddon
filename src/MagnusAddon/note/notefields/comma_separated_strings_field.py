from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField

if TYPE_CHECKING:
    from note.jpnote import JPNote

class CommaSeparatedStringsSetField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = CommaSeparatedStringsListField(note, field_name)

    def get(self) -> set[str]:
        return set(self._field.get())

    def set(self, value: set[str]) -> None:
        self._field.set(list(value))

    def add(self, value: str) -> None:
        self.set(self.get() | {value})
