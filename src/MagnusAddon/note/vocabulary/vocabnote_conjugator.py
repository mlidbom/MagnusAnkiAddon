from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services import conjugator
from note.note_constants import Mine
from sysutils import ex_sequence

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteConjugator(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def _get_stems_for_form(self, form: str) -> list[str]:
        return [base for base in conjugator.get_word_stems(form,
                                                           is_ichidan_verb=self._vocab.parts_of_speech.is_ichidan(),
                                                           is_godan=self._vocab.parts_of_speech.is_godan()) if base != form]

    def get_stems_for_primary_form(self) -> list[str]:
        return ex_sequence.remove_duplicates_while_retaining_order(self._get_stems_for_form(self._vocab.get_question()))

    def get_text_matching_forms_for_primary_form(self) -> list[str]:
        return [self._vocab.question.without_noise_characters] + self._get_stems_for_form(self._vocab.question.without_noise_characters)

    def get_text_matching_forms_for_all_form(self) -> list[str]:
        return [self._strip_noise_characters(form) for form in self._vocab.forms.all_list() + self.get_stems_for_all_forms()]

    def get_stems_for_all_forms(self) -> list[str]:
        return ex_sequence.flatten([self._get_stems_for_form(form) for form in self._vocab.forms.all_set()])

    @staticmethod
    def _strip_noise_characters(string: str) -> str:
        return string.replace(Mine.VocabPrefixSuffixMarker, "")
