from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.tag import Tag
from sysutils.bit_flags_set import BitFlagsSet
from sysutils.memory_usage import string_auto_interner
from typed_linq_collections.collections.q_dict import QDict
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from collections.abc import Iterator

    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef


class NoteTags(Slots):
    """Manages tags for a note using a compact bitfield representation."""
    _flags: BitFlagsSet

    def __init__(self, note: WeakRef[JPNote]) -> None:
        self._note: WeakRef[JPNote] = note
        self._flags = BitFlagsSet()
        backend_note = self._note().backend_note

        for tag_name in backend_note.tags:
            self._flags.set_flag(Tag.from_name(tag_name).id)

        backend_note.tags = self.to_interned_string_list()

    def _sync_to_backend(self) -> None:
        self._note().backend_note.tags = self.to_interned_string_list()

    def has_tag(self, tag: Tag) -> bool:
        return self._flags.has(tag.id)

    def set_tag(self, tag: Tag) -> None:
        if not self.has_tag(tag):
            self._flags.set_flag(tag.id)
            self._sync_to_backend()
            self._note()._flush()  # pyright: ignore [reportPrivateUsage]

    def remove_tag(self, tag: Tag) -> None:
        if self.has_tag(tag):
            self._flags.unset_flag(tag.id)
            self._sync_to_backend()
            self._note()._flush()  # pyright: ignore [reportPrivateUsage]

    def toggle_tag(self, tag: Tag, on: bool) -> None:
        if on:
            self.set_tag(tag)
        else:
            self.remove_tag(tag)

    def get_all(self) -> list[Tag]:
        return list(self)

    def __contains__(self, tag: Tag) -> bool:  # Support 'tag in tags' syntax.
        return self.has_tag(tag)

    def __iter__(self) -> Iterator[Tag]:
        for bit_pos in self._flags.all_flags():
            yield Tag.from_id(bit_pos)

    _interned_string_lists: QDict[int, list[str]] = QDict()
    def to_interned_string_list(self) -> list[str]:
        bitfield = self._flags.bitfield
        if bitfield not in self._interned_string_lists:
            sorted_name_list = query(self).select(lambda it: it.name).order_by(lambda it: it).to_list()
            self._interned_string_lists[bitfield] = string_auto_interner.auto_intern_qlist(sorted_name_list)

        return self._interned_string_lists[bitfield]
