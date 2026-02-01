from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.note.note_constants import NoteFields
from jastudio.note.notefields.audio_field import WritableAudioField

if TYPE_CHECKING:
    from jaslib.sysutils.weak_ref import WeakRef
    from jastudio.note.vocabulary.vocabnote import VocabNote

class VocabNoteAudio(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self.first: WritableAudioField = WritableAudioField(vocab, NoteFields.Vocab.Audio_b)
        self.second: WritableAudioField = WritableAudioField(vocab, NoteFields.Vocab.Audio_g)
        self.tts: WritableAudioField = WritableAudioField(vocab, NoteFields.Vocab.Audio_TTS)

    def get_primary_audio_path(self) -> str:
        return self.first.first_audiofile_path() or self.second.first_audiofile_path() or self.tts.first_audiofile_path() or ""

    def get_primary_audio(self) -> str:
        return self.first.raw_walue() or self.second.raw_walue() or self.tts.raw_walue() or ""

    @override
    def __repr__(self) -> str: return f"""first: {self.first}, second: {self.second}, tts: {self.tts}"""
