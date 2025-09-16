from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class TagFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], tag: str) -> None:
        self._note: WeakRef[JPNote] = note
        self.tag: str = tag
        self._value: bool = self._note().has_tag(self.tag)
        note().on_tag_updated(self.tag, self._on_tag_updated)

    def _on_tag_updated(self) -> None:
        self._value = self._note().has_tag(self.tag)

    def is_set(self) -> bool: return self._value

    def set_to(self, set_: bool) -> None:
        if set_: self._note().set_tag(self.tag)
        else: self._note().remove_tag(self.tag)
        self._value = set_

    @override
    def __repr__(self) -> str: return f"""{self.tag}: {self.is_set()}"""
