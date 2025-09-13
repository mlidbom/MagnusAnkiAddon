from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.readonly_string_field import AutoStrippingReadOnlyStringField
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from collections.abc import Callable

    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class AutoStrippingStringField(AutoStrippingReadOnlyStringField, Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)
        self._reset_callbacks: list[Callable[[], None]] = []

    def set(self, value: str) -> None:
        self._note().set_field(self._field_name, value.strip())
        self._value.reset()
        for callback in self._reset_callbacks: callback()

    def empty(self) -> None: self.set("")

    def lazy_reader[TValue](self, reader: Callable[[], TValue]) -> Lazy[TValue]:
        lazy = Lazy(reader)
        self._reset_callbacks.append(lazy.reset)
        return lazy
