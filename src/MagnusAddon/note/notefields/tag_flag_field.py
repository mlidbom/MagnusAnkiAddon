from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.tag import Tag
    from sysutils.weak_ref import WeakRef

class TagFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], tag: Tag) -> None:
        self._note: WeakRef[JPNote] = note
        self.tag: Tag = tag

    def is_set(self) -> bool:
        jp_note = self._note()
        return jp_note.tags.has_tag(self.tag)

    def set_to(self, set_: bool) -> None:
        if set_:
            jp_note = self._note()
            jp_note.tags.set_tag(self.tag)
        else:
            jp_note1 = self._note()
            jp_note1.tags.remove_tag(self.tag)

    @override
    def __repr__(self) -> str: return f"""{self.tag.name}: {self.is_set()}"""
