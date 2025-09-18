from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import AutoSlots
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class IntegerField(AutoSlots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._note: WeakRef[JPNote] = note
        self._field: MutableStringField = MutableStringField(note, field_name)

    # noinspection PyUnusedFunction
    def get(self) -> int:
        field = self._field
        return int(field.value) if self._field.has_value() else 0

    def set(self, value: int) -> None:
        self._field.set(str(value))
