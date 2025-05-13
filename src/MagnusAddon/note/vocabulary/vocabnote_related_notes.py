from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from note.note_constants import NoteFields
from note.notefields.comma_separated_strings_set_field import CommaSeparatedStringsSetField
from note.notefields.string_field import StringField
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection
    from note.jpnote import JPNote
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteRelatedNotes:
    def __init__(self, vocab: VocabNote) -> None:
        self._vocab = vocab
        self._similar_meanings_field: CommaSeparatedStringsSetField = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.Related_similar_meaning)
        self._ergative_twin_field: StringField = StringField(vocab, NoteFields.Vocab.Related_ergative_twin)
        self.derived_from: StringField = StringField(vocab, NoteFields.Vocab.Related_derived_from)
        self.confused_with: CommaSeparatedStringsSetField = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.Related_confused_with)

    @property
    def _collection(self) -> JPCollection: return self._vocab.collection

    def similar_meanings(self) -> set[str]:
        return self._similar_meanings_field.get()

    def add_similar_meaning(self, new_similar: str, _is_recursive_call: bool = False) -> None:
        self._similar_meanings_field.add(new_similar)

        if not _is_recursive_call:
            for similar in self._collection.vocab.with_question(new_similar):
                similar.related_notes.add_similar_meaning(self._vocab.get_question(), _is_recursive_call=True)

    def ergative_twin(self) -> str:
        return self._ergative_twin_field.get()

    def set_ergative_twin(self, value: str) -> None:
        self._ergative_twin_field.set(value)

        for twin in app.col().vocab.with_question(value):
            twin.related_notes._ergative_twin_field.set(self._vocab.get_question())

    def in_compounds(self) -> list[VocabNote]:
        return self._collection.vocab.with_compound_part(self._vocab.get_question_without_noise_characters())

    def get_direct_dependencies(self) -> set[JPNote]:
        note = self._vocab
        return (set(self._collection.kanji.with_any_kanji_in(list(note.kanji.extract_main_form_kanji()))) |
                set(ex_sequence.flatten([self._collection.vocab.with_question(compound_part) for compound_part in self._vocab.compound_parts.get()])))

    def remove_similar_meaning(self, similar: str) -> None:
        self._similar_meanings_field.remove(similar)

    def remove_confused_with(self, confused_with: str) -> None:
        self.confused_with.remove(confused_with)
