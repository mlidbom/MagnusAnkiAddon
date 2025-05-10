from __future__ import annotations

from note.jpnote import JPNote
from note.notefields.strip_html_on_read_string_field import StripHtmlOnReadStringField

class AudioField(StripHtmlOnReadStringField):
    def __init__(self, note: JPNote, field_name: str) -> None:
        super().__init__(note, field_name)

    def file_path(self) -> str: return self.get()[7:-1]
