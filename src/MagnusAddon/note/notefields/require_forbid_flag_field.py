from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.tag import Tag
    from sysutils.weak_ref import WeakRef

class RequireForbidFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], required_tag: Tag, forbidden_tag: Tag) -> None:
        self._note: WeakRef[JPNote] = note
        self._required_tag: Tag = required_tag
        self._forbidden_tag: Tag = forbidden_tag

    @property
    def is_configured_required(self) -> bool:
        jp_note = self._note()
        return jp_note.tags.has_tag(self._required_tag)
    @property
    def is_configured_forbidden(self) -> bool:
        jp_note = self._note()
        return jp_note.tags.has_tag(self._forbidden_tag)

    @property
    def is_required(self) -> bool: return self.is_configured_required
    @property
    def is_forbidden(self) -> bool: return self.is_configured_forbidden

    def set_forbidden(self, value: bool) -> None:
        if value:
            jp_note = self._note()
            jp_note.tags.set_tag(self._forbidden_tag)
            jp_note1 = self._note()
            jp_note1.tags.remove_tag(self._required_tag)
        else:
            jp_note2 = self._note()
            jp_note2.tags.remove_tag(self._forbidden_tag)

    def set_required(self, value: bool) -> None:
        if value:
            jp_note = self._note()
            jp_note.tags.set_tag(self._required_tag)
            jp_note1 = self._note()
            jp_note1.tags.remove_tag(self._forbidden_tag)
        else:
            jp_note2 = self._note()
            jp_note2.tags.remove_tag(self._required_tag)

    @override
    def __repr__(self) -> str:
        return f"""{self._required_tag.name.replace("requires::", "")} required: {self.is_required}, forbidden: {self.is_forbidden}"""
