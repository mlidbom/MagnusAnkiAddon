from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import NoteFields
from note.notefields.comma_separated_strings_field import CommaSeparatedStringsSetField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteRelatedNotes:
    def __init__(self, vocab: VocabNote):
        self._vocab = vocab
        self._similar_meanings = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.Related_similar_meaning)


    def similar_meanings(self) -> set[str]:
        return self._similar_meanings.get()


    def add_similar_meaning(self, new_similar: str, _is_recursive_call: bool = False) -> None:
        self._similar_meanings.add(new_similar)

        if not _is_recursive_call:
            for similar in self._vocab.collection.vocab.with_question(new_similar):
                similar1 = self._vocab.get_question()
                similar.related_notes.add_similar_meaning(similar1)

