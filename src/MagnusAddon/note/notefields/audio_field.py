from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.jpnote import JPNote

class AudioField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)

    def file_path(self) -> str: return self._field.get()[7:-1]

    def get(self) -> str: return self._field.get()

class WritableAudioField(AudioField):
    def __init__(self, note: JPNote, field_name: str) -> None:
        super().__init__(note, field_name)

    def set(self, value: str) -> None: self._field.set(value)
