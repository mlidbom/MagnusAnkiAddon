from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from jastudio.language_services.janome_ex.word_extraction import analysis_constants
from jastudio.note.note_constants import NoteFields
from jastudio.note.tags import Tags
from jastudio.note.vocabulary.pos import POS
from jastudio.note.vocabulary.pos_set_interner import POSSetManager
from typed_linq_collections.collections.q_frozen_set import QFrozenSet
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from collections.abc import Iterable

    from jastudio.note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNotePartsOfSpeech(Slots):
    _field_name: str = NoteFields.Vocab.parts_of_speech
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        self.set_raw_string_value(self.raw_string_value())

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def raw_string_value(self) -> str: return self._vocab.get_field(VocabNotePartsOfSpeech._field_name)

    def set_raw_string_value(self, value: str) -> None:
        self._vocab.set_field(VocabNotePartsOfSpeech._field_name, POSSetManager.intern_and_harmonize(value))

    def set(self, value: Iterable[str]) -> None:
        self.set_raw_string_value(",".join(value))

    def get(self) -> frozenset[str]: return POSSetManager.get(self.raw_string_value())

    def is_ichidan(self) -> bool: return POS.ICHIDAN_VERB in self.get()
    def is_godan(self) -> bool: return POS.GODAN_VERB in self.get()

    def is_transitive(self) -> bool: return POS.TRANSITIVE in self.get()
    def is_intransitive(self) -> bool: return POS.INTRANSITIVE in self.get()

    def is_inflecting_word_type(self) -> bool: return self.is_godan() or self.is_ichidan()

    def is_suru_verb_included(self) -> bool:
        question = self._vocab.question.without_noise_characters
        return len(question) > 2 and question[-2:] == "する"

    _ga_suru_ni_suru_endings: QSet[str] = QSet(("がする", "にする", "くする"))
    def is_ni_suru_ga_suru_ku_suru_compound(self) -> bool:
        question = self._vocab.question.without_noise_characters
        return len(question) > 3 and question[-3:] in self._ga_suru_ni_suru_endings

    def is_uk(self) -> bool:
        return self._vocab.tags.contains(Tags.UsuallyKanaOnly)

    def set_automatically_from_dictionary(self) -> None:
        from jastudio.language_services.jamdict_ex.dict_lookup import DictLookup

        lookup = DictLookup.lookup_vocab_word_or_name(self._vocab)
        if lookup.found_words():
            value = ", ".join(lookup.parts_of_speech())
            self.set_raw_string_value(value)
        elif self.is_suru_verb_included():
            question = self._vocab.question.without_noise_characters[:-2]
            readings = [reading[:-2] for reading in self._vocab.readings.get()]
            lookup = DictLookup.lookup_word_or_name_with_matching_reading(question, readings)
            pos = lookup.parts_of_speech() & QFrozenSet({POS.TRANSITIVE, POS.INTRANSITIVE})
            value1 = POS.SURU_VERB + ", " + ", ".join(pos)
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

    def is_complete_na_adjective(self) -> bool:
        return self.__vocab().question.raw.endswith("な") and POS.NA_ADJECTIVE in self.get()

    @override
    def __repr__(self) -> str: return self.raw_string_value()
