from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.tag_flag_field import TagFlagField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class RequireForbidFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], required_tag: str, forbidden_tag: str) -> None:
        self._required_field = TagFlagField(note, required_tag)
        self._forbidden_field = TagFlagField(note, forbidden_tag)

    @property
    def is_configured_required(self) -> bool: return self._required_field.is_set()
    @property
    def is_configured_forbidden(self) -> bool: return self._forbidden_field.is_set()

    @property
    def is_required(self) -> bool: return self.is_configured_required
    @property
    def is_forbidden(self) -> bool: return self.is_configured_forbidden

    def set_forbidden(self, value: bool) -> None:
        self._forbidden_field.set_to(value)
        if value: self._required_field.set_to(False)

    def set_required(self, value: bool) -> None:
        self._required_field.set_to(value)
        if value: self._forbidden_field.set_to(False)
