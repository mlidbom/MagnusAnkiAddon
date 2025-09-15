from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef


class StripHtmlOnReadStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._field: MutableStringField = MutableStringField(note, field_name)

    def get_raw(self) -> str: return self._field.get()

    def set(self, value: str) -> None: self._field.set(value)
    def empty(self) -> None: self.set("")
    def has_value(self) -> bool: return self._field.has_value()


