from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class CommaSeparatedStringsListFieldDeDuplicated(CommaSeparatedStringsListField, Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)

    def set(self, value: list[str]) -> None:
        super().set(ex_sequence.remove_duplicates_while_retaining_order(value))
