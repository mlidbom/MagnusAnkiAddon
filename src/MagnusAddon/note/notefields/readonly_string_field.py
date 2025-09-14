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
        def get_field_value() -> str: return note().get_field(field_name)
        self._value: Lazy[str] = Lazy(get_field_value)

    def get(self) -> str: return self._value()
    def has_value(self) -> bool: return self.get() != ""
