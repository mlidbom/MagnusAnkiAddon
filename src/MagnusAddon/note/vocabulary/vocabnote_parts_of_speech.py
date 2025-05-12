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


    def is_ichidan(self) -> bool:
        return "ichidan" in self.raw_string_value().lower()

    def is_godan(self) -> bool:
        return "godan" in self.raw_string_value().lower()

    def is_suru_verb_included(self) -> bool:
        question = self._vocab.get_question_without_noise_characters()
        return question[-2:] == "する"

    def set_automatically_from_dictionary(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup

        lookup = DictLookup.try_lookup_vocab_word_or_name(self._vocab)
        if lookup.found_words():
            value = ", ".join(lookup.parts_of_speech())
            self.set_raw_string_value(value)
        elif self.is_suru_verb_included():
            question = self._vocab.get_question_without_noise_characters()[:-2]
            readings = [reading[:-2] for reading in self._vocab.get_readings()]
            lookup = DictLookup.try_lookup_word_or_name(question, readings)
            pos = lookup.parts_of_speech() & {"transitive", "intransitive"}
            value1 = "suru verb, " + ", ".join(pos)
            self.set_raw_string_value(value1)