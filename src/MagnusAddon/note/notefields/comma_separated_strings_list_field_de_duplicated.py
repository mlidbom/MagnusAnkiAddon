from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from note.notefields.comma_separated_strings_list_field import MutableCommaSeparatedStringsListField
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class MutableCommaSeparatedStringsListFieldDeDuplicated(MutableCommaSeparatedStringsListField, ProfilableAutoSlots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)

    @override
    def set(self, value: list[str]) -> None:
        super().set(ex_sequence.remove_duplicates_while_retaining_order(value))
