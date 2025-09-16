from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class RequireForbidFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], required_tag: str, forbidden_tag: str) -> None:
        self._note: WeakRef[JPNote] = note
        self._required_tag: str = required_tag
        self._forbidden_tag: str = forbidden_tag
        self._is_required: bool = note().has_tag(required_tag)
        self._is_forbidden: bool = note().has_tag(forbidden_tag)

    @property
    def is_configured_required(self) -> bool: return self._is_required
    @property
    def is_configured_forbidden(self) -> bool: return self._is_forbidden

    @property
    def is_required(self) -> bool: return self.is_configured_required
    @property
    def is_forbidden(self) -> bool: return self.is_configured_forbidden

    def set_forbidden(self, value: bool) -> None:
        self.set_required(not value)

    def set_required(self, value: bool) -> None:
        if value:
            self._note().set_tag(self._required_tag)
            self._note().remove_tag(self._forbidden_tag)
        else:
            self._note().set_tag(self._forbidden_tag)
            self._note().remove_tag(self._required_tag)

    @override
    def __repr__(self) -> str: return f"""{self._required_tag.replace("requires::", "")} required: {self.is_required}, forbidden: {self.is_forbidden}"""
