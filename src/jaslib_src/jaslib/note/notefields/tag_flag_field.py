from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots

if TYPE_CHECKING:
    from jaspythonutils.sysutils.weak_ref import WeakRef

    from jaslib.note.jpnote import JPNote
    from jaslib.note.tag import Tag

# noinspection PyUnusedFunction
class TagFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], tag: Tag) -> None:
        self._note: WeakRef[JPNote] = note
        self.tag: Tag = tag
        # Cache tag state during construction - invalidated when matching_configuration is recreated
        self._cached_is_set: bool = note().tags.contains(tag)

    def is_set(self) -> bool:
        return self._cached_is_set

    def set_to(self, set_: bool) -> None:
        if set_:
            self._note().tags.set(self.tag)
        else:
            self._note().tags.unset(self.tag)

    @override
    def __repr__(self) -> str: return f"""{self.tag.name}: {self.is_set()}"""
