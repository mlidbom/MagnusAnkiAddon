from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class ReadOnlyStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._note: WeakRef[JPNote] = note
        self._field_name: str = field_name
        def read_only_string_field_get_initial_value_for_caching() -> str: return note().get_field(field_name) # this method is interesting for profiling so we want a unuique name we can find in the trace
        self._value: Lazy[str] = Lazy(read_only_string_field_get_initial_value_for_caching)

    def get(self) -> str: return self._value()
    def has_value(self) -> bool: return self.get() != ""
