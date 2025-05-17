from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields
from note.notefields.audio_field import WritableAudioField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteAudio(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab = vocab
        self.first: WritableAudioField = WritableAudioField(vocab, NoteFields.Vocab.Audio_b)
        self.second: WritableAudioField = WritableAudioField(vocab, NoteFields.Vocab.Audio_g)

    def get_primary_audio_path(self) -> str:
        return self.first.first_audiofile_path() or self.second.first_audiofile_path() or ""

    def get_primary_audio(self) -> str:
        return self.first.raw_walue() or self.second.raw_walue()
