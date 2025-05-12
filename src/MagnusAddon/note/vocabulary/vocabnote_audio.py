from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import NoteFields
from note.notefields.audio_field import WritableAudioField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


class VocabNoteAudio:
    def __init__(self, vocab : VocabNote):
        self._vocab = vocab
        self.first: WritableAudioField = WritableAudioField(vocab, NoteFields.Vocab.Audio_b)
        self.second: WritableAudioField = WritableAudioField(vocab, NoteFields.Vocab.Audio_g)


    def get_primary_audio_path(self) -> str:
        return self.first.file_path() or self.second.file_path() or ""

    def get_primary_audio(self) -> str:
        return self.first.get() or self.second.get()