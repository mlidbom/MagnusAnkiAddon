from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.collections.linq.l_iterable import LList
    from sysutils.weak_ref import WeakRef

class PerfectSynonyms(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: FieldSetWrapper[str]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._value: FieldSetWrapper[str] = data

    def notes(self) -> LList[VocabNote]: return app.col().vocab.with_any_question_in(list(self._value.get()))

    def push_answer_to_other_synonyms(self) -> None:
        pass

    def add_overwriting_the_answer_of_the_added_synonym(self, synonym_question: str) -> None:
        self._value.add(synonym_question)
        synonyms = app.col().vocab.with_question(synonym_question)
        if len(synonyms) == 0:
            raise ValueError(f"No synonym found with question '{synonym_question}'")
        for synonym in app.col().vocab.with_question(synonym_question):
            synonym.related_notes.perfect_synonyms._value.add(self._vocab().get_question())
            synonym.user.answer.set(self._vocab().user.answer.value)


    def remove(self, synonym_question: str) -> None:
        if synonym_question not in self._value(): return

        self._value.remove(synonym_question)
        (self.notes()
         .for_each(lambda syn: syn.related_notes.perfect_synonyms._value.remove(self._vocab().get_question())))

    @override
    def __repr__(self) -> str: return self._value.__repr__()
