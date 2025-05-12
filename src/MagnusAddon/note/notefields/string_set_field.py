from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.jpnote import JPNote


class StringSetField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)