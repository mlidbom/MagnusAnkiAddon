from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.lazy import Lazy
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class AutoStrippingReadOnlyStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self._note = note
        self._field_name = field_name
        self._value: Lazy[str] = Lazy(lambda: note().get_field(field_name).strip())

    def get(self) -> str: return self._value()
    def has_value(self) -> bool: return self.get() != ""
