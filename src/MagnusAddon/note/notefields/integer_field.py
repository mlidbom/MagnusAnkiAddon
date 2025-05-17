from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef


class IntegerField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._note = note
        self._field = StringField(note, field_name)

    # noinspection PyUnusedFunction
    def get(self) -> int:
        return int(self._field.get()) if self._field.has_value() else 0

    def set(self, value: int) -> None:
        self._field.set(str(value))
