from __future__ import annotations

from typing import TYPE_CHECKING

from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.jpnote import JPNote

class AudioField:
    def __init__(self, note: JPNote, field_name: str) -> None:
        self._field = StringField(note, field_name)

    def has_audio(self) -> bool:
        return self._field.get().strip().startswith("[sound:")

    def first_audiofile_path(self) -> str:
        return self.audio_files_paths()[0] if self.has_audio() else ""

    def raw_walue(self) -> str: return self._field.get()

    def audio_files_paths(self) -> list[str]:
        if not self.has_audio(): return []

        stripped_paths = self._field.get().strip().replace("[sound:", "").split("]")
        stripped_paths = [path.strip() for path in stripped_paths]
        return stripped_paths



class WritableAudioField(AudioField):
    def __init__(self, note: JPNote, field_name: str) -> None:
        super().__init__(note, field_name)

    def set_raw_value(self, value: str) -> None: self._field.set(value)
    def set_single_file_path(self, value: str) -> None: self.set_multiple([value])
    def set_multiple(self, values: list[str]) -> None: self._field.set(''.join([f'[sound:{item}]' for item in values]))
