from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import NoteFields
from note.notefields.comma_separated_strings_field import CommaSeparatedStringsSetField
from note.notefields.string_field import StringField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteRelatedNotes:
    def __init__(self, vocab: VocabNote):
        self._vocab = vocab
        self._similar_meanings_field = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.Related_similar_meaning)
        self._ergative_twin_field = StringField(vocab, NoteFields.Vocab.Related_ergative_twin)
        self.derived_from = StringField(vocab, NoteFields.Vocab.Related_derived_from)
        self.confused_with = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.Related_confused_with)


    def similar_meanings(self) -> set[str]:
        return self._similar_meanings_field.get()


    def add_similar_meaning(self, new_similar: str, _is_recursive_call: bool = False) -> None:
        self._similar_meanings_field.add(new_similar)

        if not _is_recursive_call:
            for similar in self._vocab.collection.vocab.with_question(new_similar):
                similar.related_notes.add_similar_meaning(self._vocab.get_question())

    def ergative_twin(self) -> str:
        return self._ergative_twin_field.get()

    def set_ergative_twin(self, value: str) -> None:
        self._ergative_twin_field.set(value)

        from ankiutils import app
        for twin in app.col().vocab.with_question(value):
            twin.related_notes._ergative_twin_field.set(self._vocab.get_question())
