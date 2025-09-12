from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.string_field import AutoStrippingStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class AudioField(Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._field: AutoStrippingStringField = AutoStrippingStringField(note, field_name)

    def has_audio(self) -> bool:
        return self._field.get().strip().startswith("[sound:")

    def first_audiofile_path(self) -> str:
        return self.audio_files_paths()[0] if self.has_audio() else ""

    def raw_walue(self) -> str: return self._field.get()

    def audio_files_paths(self) -> list[str]:
        if not self.has_audio(): return []

        stripped_paths = self._field.get().strip().replace("[sound:", "").split("]")
        return [path.strip() for path in stripped_paths]

class WritableAudioField(AudioField, Slots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)

    def set_raw_value(self, value: str) -> None: self._field.set(value)
    def set_multiple(self, values: list[str]) -> None: self._field.set("".join([f"[sound:{item}]" for item in values]))
