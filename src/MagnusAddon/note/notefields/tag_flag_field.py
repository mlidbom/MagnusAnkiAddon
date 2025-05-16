from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.jpnote import JPNote

class TagFlagField:
    def __init__(self, note: JPNote, tag: str) -> None:
        self._note = note
        self.tag = tag

    @property
    def is_set(self) -> bool: return self._note.has_tag(self.tag)

    def set_to(self, set_: bool) -> None:
        if set_: self._note.set_tag(self.tag)
        else: self._note.remove_tag(self.tag)
