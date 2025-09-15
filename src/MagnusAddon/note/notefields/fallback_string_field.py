from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class FallbackStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], primary_field: str, fallback_field: str) -> None:
        self._field: MutableStringField = MutableStringField(note, primary_field)
        self._fallback_field: MutableStringField = MutableStringField(note, fallback_field)

    def get(self) -> str: return self._field.get() or self._fallback_field.get()


