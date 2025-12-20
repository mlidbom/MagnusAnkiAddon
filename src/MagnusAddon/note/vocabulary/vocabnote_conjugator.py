from __future__ import annotations

from typing import TYPE_CHECKING

from language_services import conjugator
from manually_copied_in_libraries.autoslot import Slots
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef
    from typed_linq_collections.collections.q_list import QList

class VocabNoteConjugator(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    def _get_stems_for_form(self, form: str) -> QList[str]:
        return (query(conjugator.get_word_stems(form, is_ichidan_verb=self._vocab.parts_of_speech.is_ichidan(), is_godan=self._vocab.parts_of_speech.is_godan()))
                .where(lambda stem: stem != form)
                .to_list())

    def get_stems_for_primary_form(self) -> QList[str]:
        return (self._get_stems_for_form(self._vocab.get_question())
                .distinct()
                .to_list())  # ex_sequence.remove_duplicates_while_retaining_order(self._get_stems_for_form(self._vocab.get_question()))

    def get_stems_for_all_forms(self) -> QList[str]:
        return self._vocab.forms.all_set().select_many(self._get_stems_for_form).distinct().to_list()  # ex_sequence.flatten([self._get_stems_for_form(form) for form in self._vocab.forms.all_set()])
