from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.readonly_string_field import ReadOnlyStringField

if TYPE_CHECKING:
    from collections.abc import Callable

    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class StringField(ReadOnlyStringField, Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)
        self._update_listeners: list[Callable[[], None]] = []

    def set(self, value: str) -> None:
        self._note().set_field(self._field_name, value.strip())
        self._value.reset()
        for callback in self._update_listeners: callback()

    def empty(self) -> None: self.set("")

    def on_update(self, *callbacks: Callable[[], None]) -> None: self._update_listeners.extend(callbacks)
