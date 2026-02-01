from __future__ import annotations

from typing import TYPE_CHECKING, override

from jastudio.note.tag import Tag
from sysutils.bit_flags_set import BitFlagsSet
from sysutils.memory_usage import string_auto_interner
from typed_linq_collections.collections.q_dict import QDict
from typed_linq_collections.q_iterable import QIterable, query

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jastudio.note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class NoteTags(QIterable[Tag]):
    __slots__: tuple[str, ...] = ("_note", "_flags")
    """Manages tags for a note using a compact bitfield representation."""
    _flags: BitFlagsSet

    def __init__(self, note: WeakRef[JPNote]) -> None:
        self._note: WeakRef[JPNote] = note
        self._flags = BitFlagsSet()
        backend_note = self._note().backend_note

        for tag_name in backend_note.tags:
            self._flags.set_flag(Tag.from_name(tag_name).id)

        backend_note.tags = self.to_interned_string_list()

    def _persist(self) -> None:
        self._note().backend_note.tags = self.to_interned_string_list()
        self._note()._flush()  # pyright: ignore [reportPrivateUsage]
        self._note()._on_tags_updated()  # pyright: ignore [reportPrivateUsage]

    @override
    def contains(self, value: Tag) -> bool:
        return self._flags.contains_bit(value.bit)

    def set(self, tag: Tag) -> None:
        if not self.contains(tag):
            self._flags.set_flag(tag.id)
            self._persist()

    def unset(self, tag: Tag) -> None:
        if self.contains(tag):
            self._flags.unset_flag(tag.id)
            self._persist()

    def toggle(self, tag: Tag, on: bool) -> None:
        if on:
            self.set(tag)
        else:
            self.unset(tag)

    def __contains__(self, tag: Tag) -> bool:  # Support 'tag in tags' syntax.
        return self.contains(tag)

    @override
    def __iter__(self) -> Iterator[Tag]:
        yield from self._flags.select(Tag.from_id)

    _interned_string_lists: QDict[BitFlagsSet, list[str]] = QDict()
    def to_interned_string_list(self) -> list[str]:
        if self._flags not in self._interned_string_lists:
            sorted_name_list = query(self).select(lambda it: it.name).order_by(lambda it: it).to_list()
            self._interned_string_lists[self._flags] = string_auto_interner.auto_intern_qlist(sorted_name_list)

        return self._interned_string_lists[self._flags]
