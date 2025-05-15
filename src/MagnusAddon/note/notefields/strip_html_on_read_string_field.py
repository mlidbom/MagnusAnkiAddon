from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.string_field import StringField
from sysutils import ex_str

if TYPE_CHECKING:
    from note.jpnote import JPNote


class StripHtmlOnReadStringField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)

    def get(self) -> str: return ex_str.strip_html_markup(self._field.get())
    def set(self, value: str) -> None: self._field.set(value)
    def empty(self) -> None: self.set("")


