from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.jpnote import JPNote

class FallbackStringField:
    def __init__(self, note: JPNote, primary_field: str, fallback_field: str) -> None:
        self._field = StringField(note, primary_field)
        self._fallback_field = StringField(note, fallback_field)

    def get(self) -> str: return self._field.get() or self._fallback_field.get()


