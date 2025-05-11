from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.strip_html_on_read_string_field import StripHtmlOnReadStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote

class AudioField(StripHtmlOnReadStringField):
    def __init__(self, note: JPNote, field_name: str) -> None:
        super().__init__(note, field_name)

    def file_path(self) -> str: return self.get()[7:-1]
