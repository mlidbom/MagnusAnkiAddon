from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import AutoSlots
from note.notefields.mutable_string_field import MutableStringField
from sysutils import ex_str

if TYPE_CHECKING:
    from collections.abc import Callable

    from note.jpnote import JPNote
    from sysutils.lazy import Lazy
    from sysutils.weak_ref import WeakRef

class MutableCommaSeparatedStringsListField(AutoSlots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        field = MutableStringField(note, field_name)
        self._field: MutableStringField = field
        self._value: Lazy[list[str]] = self._field.lazy_reader(lambda: ex_str.extract_comma_separated_values(field.value))

    def get(self) -> list[str]:
        return self._value()

    def remove(self, remove: str) -> None:
        self.set([item for item in self.get() if item != remove])

    def set(self, value: list[str]) -> None:
        self._field.set(", ".join(value))

    def raw_string_value(self) -> str:
        field = self._field
        return field.value

    def set_raw_string_value(self, value: str) -> None:
        self.set(ex_str.extract_comma_separated_values(value))

    def add(self, add: str) -> None:
        self.set(self.get() + [add])

    def lazy_reader[TValue](self, reader: Callable[[], TValue]) -> Lazy[TValue]: return self._field.lazy_reader(reader)

    @override
    def __repr__(self) -> str: return ", ".join(self.get())
