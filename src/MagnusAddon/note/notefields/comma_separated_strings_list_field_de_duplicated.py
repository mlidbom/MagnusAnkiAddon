from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import AutoSlots
from note.notefields.comma_separated_strings_list_field import MutableCommaSeparatedStringsListField
from sysutils.collections.linq.q_iterable import query

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class MutableCommaSeparatedStringsListFieldDeDuplicated(MutableCommaSeparatedStringsListField, AutoSlots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)

    @override
    def set(self, value: list[str]) -> None:
        super().set(query(value).unique().to_list())
