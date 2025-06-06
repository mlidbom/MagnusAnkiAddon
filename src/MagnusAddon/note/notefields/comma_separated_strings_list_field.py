from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.string_field import StringField
from sysutils import ex_str
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.jpnote import JPNote

class CommaSeparatedStringsListField(WeakRefable, Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._field = StringField(note, field_name)
        self_with_no_reference_loop = WeakRef(self)
        self._value: Lazy[list[str]] = Lazy(lambda: self_with_no_reference_loop()._extract_field_values())

    def get(self) -> list[str]:
        return self._value()

    def remove(self, remove: str) -> None:
        self.set([item for item in self.get() if item != remove])

    def set(self, value: list[str]) -> None:
        self._value = Lazy.from_value(value)
        self._field.set(", ".join(value))

    def raw_string_value(self) -> str:
        return self._field.get()

    def set_raw_string_value(self, value: str) -> None:
        self.set(ex_str.extract_comma_separated_values(value))

    def add(self, add: str) -> None:
        self.set(self.get() + [add])

    def _extract_field_values(self) -> list[str]:
        return ex_str.extract_comma_separated_values(self._field.get())
