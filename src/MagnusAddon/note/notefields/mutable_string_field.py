from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from collections.abc import Callable

    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

# this field is used extremely much, so its design is crucial for both performance and memory usage, keep in mind when changing anything
# if a field is read-only, make sure to to use ReadOnlyStringField instead, which uses less memory
class MutableStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._note: WeakRef[JPNote] = note
        self._field_name: str = field_name
        self._reset_callbacks: list[Callable[[], None]] | None = None
        self._value: str = self._string_field_get_initial_value_for_caching()

    # this method is interesting for profiling so we want a unuique name we can find in the trace
    def _string_field_get_initial_value_for_caching(self) -> str: return self._note().get_field(self._field_name)

    @property
    def value(self) -> str: return self._value

    def set(self, value: str) -> None:
        new_value = value.strip()
        if new_value != self._value:
            self._note().set_field(self._field_name, value.strip())
            self._value = new_value
            if self._reset_callbacks is not None:
                for callback in self._reset_callbacks: callback()

    def has_value(self) -> bool: return self.value != ""
    def empty(self) -> None: self.set("")

    def lazy_reader[TValue](self, reader: Callable[[], TValue]) -> Lazy[TValue]:
        lazy = Lazy(reader)
        self.on_change(lazy.reset)
        return lazy

    def on_change(self, callback: Callable[[], None]) -> None:
        if self._reset_callbacks is None:
            self._reset_callbacks = []
        self._reset_callbacks.append(callback)
