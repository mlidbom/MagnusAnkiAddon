from __future__ import annotations

from note.jpnote import JPNote
from note.notefields.string_list_field import StringListField

class StringSetField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringListField(note, field_name)

    def get(self) -> set[str]: return set(self._field.get())
    def set(self, value: set[str]) -> None: self._field.set(list(value))
