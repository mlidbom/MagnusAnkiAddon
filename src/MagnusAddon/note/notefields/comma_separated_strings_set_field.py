from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef


class CommaSeparatedStringsSetField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._field = CommaSeparatedStringsListField(note, field_name)

    def get(self) -> set[str]:
        return set(self._field.get())

    def set(self, value: set[str]) -> None:
        self._field.set(list(value))

    def add(self, value: str) -> None:
        self.set(self.get() | {value})

    def remove(self, value: str) -> None:
        self.set(self.get() - {value})

    def raw_string_value(self) -> str:
        return self._field.raw_string_value()

    def set_raw_string_value(self, value:str) -> None:
        self._field.set_raw_string_value(value)
