from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.object_instance_tracker import ObjectInstanceTracker

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class TagFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], tag: str) -> None:
        self._instance_tracker: object | None = ObjectInstanceTracker.configured_tracker_for(self)
        self._note = note
        self.tag = tag

    def is_set(self) -> bool: return self._note().has_tag(self.tag)

    def set_to(self, set_: bool) -> None:
        if set_: self._note().set_tag(self.tag)
        else: self._note().remove_tag(self.tag)

    def __repr__(self) -> str: return "True" if self.is_set() else "False"
