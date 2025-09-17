from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from note.notefields.mutable_string_field import MutableStringField

if TYPE_CHECKING:
    from note.jpnote import JPNote
    from sysutils.weak_ref import WeakRef

class AudioField(ProfilableAutoSlots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        self._field: MutableStringField = MutableStringField(note, field_name)

    def has_audio(self) -> bool:
        field = self._field
        return field.value.strip().startswith("[sound:")

    def first_audiofile_path(self) -> str:
        return self.audio_files_paths()[0] if self.has_audio() else ""

    def raw_walue(self) -> str:
        field = self._field
        return field.value

    def audio_files_paths(self) -> list[str]:
        if not self.has_audio(): return []

        field = self._field
        stripped_paths = field.value.strip().replace("[sound:", "").split("]")
        return [path.strip() for path in stripped_paths]

    @override
    def __repr__(self) -> str: return self._field.__repr__()

class WritableAudioField(AudioField, ProfilableAutoSlots):
    def __init__(self, note: WeakRef[JPNote], field_name: str) -> None:
        super().__init__(note, field_name)

    def set_raw_value(self, value: str) -> None: self._field.set(value)
