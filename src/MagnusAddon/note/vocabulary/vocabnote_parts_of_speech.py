from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import NoteFields
from note.notefields.comma_separated_strings_set_field import CommaSeparatedStringsSetField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNotePartsOfSpeech:
    def __init__(self, vocab: VocabNote) -> None:
        self._vocab = vocab
        self._field: CommaSeparatedStringsSetField = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.parts_of_speech)


    def raw_string_value(self) -> str:
        return self._field.raw_string_value()

    def set_raw_string_value(self, value: str) -> None:
        self._field.set_raw_string_value(value)

    def get(self) -> set[str]:
        return self._field.get()
