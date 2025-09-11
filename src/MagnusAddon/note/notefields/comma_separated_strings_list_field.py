from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypeVar

from autoslot import Slots
from note.notefields.string_field import StringField
from sysutils import ex_str

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.lazy import Lazy
    from sysutils.weak_ref import WeakRef

class CommaSeparatedStringsListField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        field = StringField(note, field_name)
        self._field = field
        self._value: Lazy[list[str]] = self._field.lazy_reader(lambda: ex_str.extract_comma_separated_values(field.get()))

    def get(self) -> list[str]:
        return self._value()

    def remove(self, remove: str) -> None:
        self.set([item for item in self.get() if item != remove])

    def set(self, value: list[str]) -> None:
        self._field.set(", ".join(value))

    def raw_string_value(self) -> str:
        return self._field.get()

    def set_raw_string_value(self, value: str) -> None:
        self.set(ex_str.extract_comma_separated_values(value))

    def add(self, add: str) -> None:
        self.set(self.get() + [add])

    TValue = TypeVar("TValue")
    def lazy_reader(self, reader: Callable[[], TValue]) -> Lazy[TValue]: return self._field.lazy_reader(reader)
