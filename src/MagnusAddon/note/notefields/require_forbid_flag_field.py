from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from note.tags import Tags  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from note.tag import Tag
    from sysutils.weak_ref import WeakRef

class RequireForbidFlagField(Slots):
    def __init__(self, note: WeakRef[JPNote], required_tag: Tag, forbidden_tag: Tag) -> None:
        self._note: WeakRef[JPNote] = note
        self._required_tag: Tag = required_tag
        self._forbidden_tag: Tag = forbidden_tag
        # Cache tag states during construction - invalidated when matching_configuration is recreated
        self._cached_is_required: bool = note().tags.contains(required_tag)
        self._cached_is_forbidden: bool = note().tags.contains(forbidden_tag)

    @property
    def is_configured_required(self) -> bool:
        return self._cached_is_required
    @property
    def is_configured_forbidden(self) -> bool:
        return self._cached_is_forbidden

    @property
    def name(self) -> str: return self._required_tag.name.replace(Tags.Vocab.Matching.Requires.folder_name, "")

    @property
    def is_required(self) -> bool: return self._cached_is_required
    @property
    def is_forbidden(self) -> bool: return self._cached_is_forbidden
    @property
    def is_active(self) -> bool: return self._cached_is_required or self._cached_is_forbidden

    def set_forbidden(self, value: bool) -> None:
        if value:
            self._note().tags.set(self._forbidden_tag)
            self._note().tags.unset(self._required_tag)
        else:
            self._note().tags.unset(self._forbidden_tag)

    def set_required(self, value: bool) -> None:
        if value:
            self._note().tags.set(self._required_tag)
            self._note().tags.unset(self._forbidden_tag)
        else:
            self._note().tags.unset(self._required_tag)

    @override
    def __repr__(self) -> str:
        return f"""{self.name} required: {self.is_required}, forbidden: {self.is_forbidden}"""
