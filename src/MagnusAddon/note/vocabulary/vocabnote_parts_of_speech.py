from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields, Tags
from note.notefields.comma_separated_strings_set_field import CommaSeparatedStringsSetField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNotePartsOfSpeech(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        self._field: CommaSeparatedStringsSetField = CommaSeparatedStringsSetField(vocab, NoteFields.Vocab.parts_of_speech)

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

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
        return self._vocab.question.without_noise_characters()[-2:] == "する"

    def is_uk(self) -> bool: return self._vocab.has_tag(Tags.UsuallyKanaOnly)

    _transitive_string_values = ["transitive", "transitive verb"]
    _intransitive_string_values = ["intransitive", "intransitive verb"]
    def is_transitive(self) -> bool: return any(val for val in self._transitive_string_values if val in self.get())
    def is_intransitive(self) -> bool: return any(val for val in self._intransitive_string_values if val in self.get())

    def set_automatically_from_dictionary(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup

        lookup = DictLookup.lookup_vocab_word_or_name(self._vocab)
        if lookup.found_words():
            value = ", ".join(lookup.parts_of_speech())
            self.set_raw_string_value(value)
        elif self.is_suru_verb_included():
            question = self._vocab.question.without_noise_characters()[:-2]
            readings = [reading[:-2] for reading in self._vocab.readings.get()]
            lookup = DictLookup.lookup_word_or_name_with_matching_reading(question, readings)
            pos = lookup.parts_of_speech() & {"transitive", "intransitive"}
            value1 = "suru verb, " + ", ".join(pos)
            self.set_raw_string_value(value1)
