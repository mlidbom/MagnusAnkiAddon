from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction import analysis_constants
from manually_copied_in_libraries.autoslot import Slots
from note.note_constants import NoteFields, Tags
from note.notefields.comma_separated_strings_set_field import MutableCommaSeparatedStringsSetField

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNotePartsOfSpeech(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        self._field: MutableCommaSeparatedStringsSetField = MutableCommaSeparatedStringsSetField(vocab, NoteFields.Vocab.parts_of_speech)

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

    def is_inflecting_word_type(self) -> bool:
        return self.is_godan() or self.is_ichidan()

    def is_suru_verb_included(self) -> bool:
        question = self._vocab.question.without_noise_characters
        return len(question) > 2 and question[-2:] == "する"

    _ga_suru_ni_suru_endings: set[str] = {"がする", "にする", "くする"}
    def is_ni_suru_ga_suru_ku_suru_compound(self) -> bool:
        question = self._vocab.question.without_noise_characters
        return len(question) > 3 and question[-3:] in self._ga_suru_ni_suru_endings

    def is_uk(self) -> bool: return self._vocab.has_tag(Tags.UsuallyKanaOnly)

    _transitive_string_values: list[str] = ["transitive", "transitive verb"]
    _intransitive_string_values: list[str] = ["intransitive", "intransitive verb"]
    def is_transitive(self) -> bool: return any(val for val in self._transitive_string_values if val in self.get())
    def is_intransitive(self) -> bool: return any(val for val in self._intransitive_string_values if val in self.get())

    def set_automatically_from_dictionary(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup

        lookup = DictLookup.lookup_vocab_word_or_name(self._vocab)
        if lookup.found_words():
            value = ", ".join(lookup.parts_of_speech())
            self.set_raw_string_value(value)
        elif self.is_suru_verb_included():
            question = self._vocab.question.without_noise_characters[:-2]
            readings = [reading[:-2] for reading in self._vocab.readings.get()]
            lookup = DictLookup.lookup_word_or_name_with_matching_reading(question, readings)
            pos = lookup.parts_of_speech() & {"transitive", "intransitive"}
            value1 = "suru verb, " + ", ".join(pos)
            self.set_raw_string_value(value1)

    # todo in terms of using this for yielding compounds, される is apt not to work since in for instance 左右されます, され is tokenized as する、れる so two tokens would need to be yielded, not one. How to fix?
    def is_passive_verb_compound(self) -> bool:
        compounds = self._vocab.compound_parts.primary()
        if len(compounds) == 0: return False
        return compounds[-1] in analysis_constants.passive_verb_endings


    def is_causative_verb_compound(self) -> bool:
        compounds = self._vocab.compound_parts.primary()
        if len(compounds) == 0: return False
        return compounds[-1] in analysis_constants.causative_verb_endings

    _na_adjective_tos_names: set[str] = {"な adjective", "na-adjective"}
    def is_complete_na_adjective(self) -> bool:
        return self.__vocab().question.raw.endswith("な") and any(na for na in self._na_adjective_tos_names if na in self.get())

    @override
    def __repr__(self) -> str: return self._field.__repr__()
