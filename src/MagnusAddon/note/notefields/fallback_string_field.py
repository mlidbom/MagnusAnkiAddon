from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.readonly_string_field import ReadOnlyStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class FallbackStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], primary_field: str, fallback_field: str) -> None:
        self._field: ReadOnlyStringField = ReadOnlyStringField(note, primary_field)
        self._fallback_field: ReadOnlyStringField = ReadOnlyStringField(note, fallback_field)

    def get(self) -> str:
        field = self._field
        string_field = self._fallback_field
        return field.value or string_field.value
