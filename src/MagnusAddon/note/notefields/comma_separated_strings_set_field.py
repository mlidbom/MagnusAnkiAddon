from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.notefields.comma_separated_strings_list_field import MutableCommaSeparatedStringsListField
from sysutils.lazy import Lazy
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class MutableCommaSeparatedStringsSetField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._field: MutableCommaSeparatedStringsListField = MutableCommaSeparatedStringsListField(note, field_name)
        field_with_no_reference_loop = self._field
        self._value: Lazy[QSet[str]] = Lazy(lambda: field_with_no_reference_loop.get().to_set())

    def get(self) -> QSet[str]:
        return self._value()

    def set(self, value: QSet[str]) -> None:
        self._value = Lazy[QSet[str]].from_value(value)
        self._field.set(list(value))

    def remove(self, value: str) -> None:
        self.set(self.get() - {value})

    def raw_string_value(self) -> str:
        return self._field.raw_string_value()

    def set_raw_string_value(self, value: str) -> None:
        self._field.set_raw_string_value(value)

    @override
    def __repr__(self) -> str: return self.raw_string_value()
