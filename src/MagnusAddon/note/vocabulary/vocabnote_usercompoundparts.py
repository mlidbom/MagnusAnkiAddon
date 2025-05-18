from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.note_constants import NoteFields
from note.notefields.comma_separated_strings_list_field import CommaSeparatedStringsListField
from note.sentences.sentence_configuration import SentenceConfiguration

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteUserCompoundParts(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        self._field: CommaSeparatedStringsListField = CommaSeparatedStringsListField(vocab, NoteFields.Vocab.user_compounds)

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    @property
    def _collection(self) -> JPCollection: return self._vocab.collection

    def get(self) -> list[str]: return self._field.get()
    def set(self, value: list[str]) -> None: self._field.set(value)

    def auto_generate(self) -> None:
        from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
        from note.vocabulary.vocabnote import VocabNote
        analysis = TextAnalysis(self._vocab.get_question(), SentenceConfiguration.from_incorrect_matches([WordExclusion.global_(form) for form in self._vocab.forms.all_set()]))
        compound_parts = [a.form for a in analysis.display_words if a.form not in self._vocab.forms.all_set()]
        if not len(compound_parts) > 1:  # time to brute force it
            word = self._vocab.get_question()
            all_substrings = [word[i:j] for i in range(len(word)) for j in range(i + 1, len(word) + 1) if word[i:j] != word]
            all_word_substrings = [w for w in all_substrings if DictLookup.is_dictionary_or_collection_word(w)]
            compound_parts = [segment for segment in all_word_substrings if not any(parent for parent in all_word_substrings if segment in parent and parent != segment)]

        segments_missing_vocab = [segment for segment in compound_parts if not self._collection.vocab.is_word(segment)]
        for missing in segments_missing_vocab:
            created = VocabNote.factory.create_with_dictionary(missing)
            created.suspend_all_cards()

        self.set(compound_parts)
