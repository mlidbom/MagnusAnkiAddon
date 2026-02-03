from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from typed_linq_collections.q_iterable import query

from jaslib.note.notefields.comma_separated_strings_list_field import MutableCommaSeparatedStringsListField

if TYPE_CHECKING:
    from jaslib.note.jpnote import JPNote
    from jaslib.sysutils.weak_ref import WeakRef

class MutableCommaSeparatedStringsListFieldDeDuplicated(MutableCommaSeparatedStringsListField, Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)

    @override
    def set(self, value: list[str]) -> None:
        super().set(query(value).distinct().to_list())
