from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots

from jaslib.note.notefields.caching_mutable_string_field import CachingMutableStringField
from jaslib.sysutils import ex_str

if TYPE_CHECKING:
    from collections.abc import Callable

    from typed_linq_collections.collections.q_list import QList
    from typed_linq_collections.collections.string_interning import QInterningList

    from jaslib.note.jpnote import JPNote
    from jaslib.sysutils.lazy import Lazy
    from jaslib.sysutils.weak_ref import WeakRef

class MutableCommaSeparatedStringsListField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        field = CachingMutableStringField(note, field_name)
        self._field: CachingMutableStringField = field
        self._value: Lazy[QInterningList] = self._field.lazy_reader(lambda: ex_str.extract_comma_separated_values(field.value))

    def get(self) -> QList[str]:
        return self._value()

    def remove(self, remove: str) -> None:
        self.set([item for item in self.get() if item != remove])

    def set(self, value: list[str]) -> None:
        self._field.set(", ".join(value))

    def raw_string_value(self) -> str:
        field = self._field
        return field.value

    def add(self, add: str) -> None:
        self.set(self.get() + [add])

    def lazy_reader[TValue](self, reader: Callable[[], TValue]) -> Lazy[TValue]: return self._field.lazy_reader(reader)

    @override
    def __repr__(self) -> str: return ", ".join(self.get())
