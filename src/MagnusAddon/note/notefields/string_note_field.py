from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.jpnote import JPNote

class StringField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._note = note
        self._field_name = field_name

    def get(self) -> str: return self._note.get_field(self._field_name).strip()
    def set(self, value: str) -> None: self._note.set_field(self._field_name, value.strip())

