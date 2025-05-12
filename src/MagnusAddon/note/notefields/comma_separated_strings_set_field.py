from __future__ import annotations

import typing

from note.notefields.string_field import StringField

if typing.TYPE_CHECKING:
    from note.jpnote import JPNote



class StringSetField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)
