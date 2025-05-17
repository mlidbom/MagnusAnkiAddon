from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class ReadOnlyStringField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._instance_tracker: ObjectInstanceTracker = ObjectInstanceTracker(self.__class__)
        self._note = note
        self._field_name = field_name


    def get(self) -> str: return self._note().get_field(self._field_name).strip()

    def has_value(self) -> bool: return self.get() != ""
