from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.readonly_string_field import ReadOnlyStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class StringField(ReadOnlyStringField):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)

    def set(self, value: str) -> None: self._note().set_field(self._field_name, value.strip())
    def empty(self) -> None: self.set("")

