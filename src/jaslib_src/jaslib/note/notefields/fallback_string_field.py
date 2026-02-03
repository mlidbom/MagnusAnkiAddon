from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jaspythonutils.sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from jaslib.note.notefields.mutable_string_field import MutableStringField

class FallbackStringField(WeakRefable, Slots):
    def __init__(self, primary_field: MutableStringField, fallback_field: MutableStringField) -> None:
        self._field: MutableStringField = primary_field
        self._fallback_field: MutableStringField = fallback_field

    def get(self) -> str:
        return self._field.value or self._fallback_field.value
