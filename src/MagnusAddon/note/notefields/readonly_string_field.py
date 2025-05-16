from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils.object_instance_tracker import ObjectInstanceTracker
from sysutils.weak_ref import WeakRef

if TYPE_CHECKING:
    from note.jpnote import JPNote

class ReadOnlyStringField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._note = WeakRef(note)
        self._field_name = field_name
        self._instance_tracker = ObjectInstanceTracker(ReadOnlyStringField)


    def get(self) -> str: return self._note().get_field(self._field_name).strip()

    def has_value(self) -> bool: return self.get() != ""
