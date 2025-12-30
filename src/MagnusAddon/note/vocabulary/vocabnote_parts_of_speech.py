from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.word_extraction import analysis_constants
from note.note_constants import NoteFields
from note.tags import Tags
from note.vocabulary.pos_set_interner import POSSetManager
from sysutils.bit_flags_set import BitFlagsSet
from typed_linq_collections.collections.q_frozen_set import QFrozenSet
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

_is_ichidan_flag = BitFlagsSet.flag_for(1)
_is_godan_flag = BitFlagsSet.flag_for(2)
_is_transitive_flag = BitFlagsSet.flag_for(3)
_is_intransitive_flag = BitFlagsSet.flag_for(4)
_is_inflecting_word_type_flag = BitFlagsSet.flag_for(5)
_is_suru_verb_included_flag = BitFlagsSet.flag_for(6)
_is_ni_suru_ga_suru_ku_suru_compound_flag = BitFlagsSet.flag_for(7)
_is_passive_verb_compound_flag = BitFlagsSet.flag_for(8)
_is_causative_verb_compound_flag = BitFlagsSet.flag_for(9)
_is_complete_na_adjective_flag = BitFlagsSet.flag_for(10)

class VocabNotePartsOfSpeech(Slots):
    _field_name: str = NoteFields.Vocab.parts_of_speech
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        self.__values: BitFlagsSet | None = None
        self.set_raw_string_value(self.raw_string_value())

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def raw_string_value(self) -> str: return self._vocab.get_field(VocabNotePartsOfSpeech._field_name)

    def set_raw_string_value(self, value: str) -> None:
        self._vocab.set_field(VocabNotePartsOfSpeech._field_name, POSSetManager.intern_and_harmonize(value))
        self.reset_cache()

    @property
    def _values(self) -> BitFlagsSet:
        if self.__values is None:
            self.__values = self._create_cache()

        return self.__values

    def _create_cache(self) -> BitFlagsSet:
        values = BitFlagsSet()
        values.toggle_flag(_is_ichidan_flag, "ichidan verb" in self.get())
        values.toggle_flag(_is_godan_flag, "godan verb" in self.get())
        values.toggle_flag(_is_transitive_flag, "transitive" in self.get())
        values.toggle_flag(_is_intransitive_flag, "intransitive" in self.get())
        values.toggle_flag(_is_inflecting_word_type_flag, "godan verb" in self.get() or "ichidan verb" in self.get())
        values.toggle_flag(_is_complete_na_adjective_flag, self.__vocab().question.raw.endswith("な") and "na-adjective" in self.get())
        values.toggle_flag(_is_suru_verb_included_flag, self._is_suru_verb_included())
        values.toggle_flag(_is_ni_suru_ga_suru_ku_suru_compound_flag, self._is_ni_suru_ga_suru_ku_suru_compound())
        values.toggle_flag(_is_passive_verb_compound_flag, self._is_passive_verb_compound())
        values.toggle_flag(_is_causative_verb_compound_flag, self._is_causative_verb_compound())
        return values

    def reset_cache(self) -> None: self.__values = None

    def get(self) -> QFrozenSet[str]: return POSSetManager.get(self.raw_string_value())
    def is_ichidan(self) -> bool: return self._values.contains(_is_ichidan_flag)
    def is_godan(self) -> bool: return self._values.contains(_is_godan_flag)
    def is_transitive(self) -> bool: return self._values.contains(_is_transitive_flag)
    def is_intransitive(self) -> bool: return self._values.contains(_is_intransitive_flag)
    def is_inflecting_word_type(self) -> bool: return self._values.contains(_is_inflecting_word_type_flag)
    def is_suru_verb_included(self) -> bool: return self._values.contains(_is_suru_verb_included_flag)
    def is_passive_verb_compound(self) -> bool: return self._values.contains(_is_passive_verb_compound_flag)
    def is_causative_verb_compound(self) -> bool: return self._values.contains(_is_causative_verb_compound_flag)
    def is_complete_na_adjective(self) -> bool: return self._values.contains(_is_complete_na_adjective_flag)
    def is_ni_suru_ga_suru_ku_suru_compound(self) -> bool: return self._values.contains(_is_ni_suru_ga_suru_ku_suru_compound_flag)
    def is_uk(self) -> bool: return self._vocab.tags.contains(Tags.UsuallyKanaOnly)

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
            pos = lookup.parts_of_speech() & QFrozenSet({"transitive", "intransitive"})
            value1 = "suru verb, " + ", ".join(pos)
            self.set_raw_string_value(value1)

    _ga_suru_ni_suru_endings: QSet[str] = QSet(("がする", "にする", "くする"))
    def _is_ni_suru_ga_suru_ku_suru_compound(self) -> bool:
        question = self._vocab.question.without_noise_characters
        return len(question) > 3 and question[-3:] in self._ga_suru_ni_suru_endings

    def _is_causative_verb_compound(self) -> bool:
        compounds = self._vocab.compound_parts.primary()
        if len(compounds) == 0: return False
        return compounds[-1] in analysis_constants.causative_verb_endings

    def _is_passive_verb_compound(self) -> bool:
        compounds = self._vocab.compound_parts.primary()
        if len(compounds) == 0: return False
        return compounds[-1] in analysis_constants.passive_verb_endings

    def _is_suru_verb_included(self) -> bool:
        question = self._vocab.question.without_noise_characters
        return len(question) > 2 and question[-2:] == "する"

    @override
    def __repr__(self) -> str: return self.raw_string_value()
