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
        vocab().user.answer.on_change(self.push_answer_to_other_synonyms)

    def notes(self) -> LList[VocabNote]: return app.col().vocab.with_any_question_in(list(self._value.get()))

    def push_answer_to_other_synonyms(self) -> None:
        for synonym in self.notes():
            synonym.user.answer.set(self._vocab().user.answer.value)

    def get(self) -> set[str]: return self._value.get()

    def add_overwriting_the_answer_of_the_added_synonym(self, synonym_question: str) -> None:
        if synonym_question == self._vocab().get_question(): return
        if synonym_question not in self._value.get():
            self._value.add(synonym_question)

            answer = self._vocab().user.answer.value

            for synonym in app.col().vocab.with_question(synonym_question):
                synonym.related_notes.perfect_synonyms._value.add(self._vocab().get_question())
                synonym.user.answer.set(answer)
                for nested_synonym in (synonym.related_notes.perfect_synonyms.notes()
                        .where(lambda syn: syn.get_question() != self._vocab().get_question())):
                    self._value.add(nested_synonym.get_question())
                    nested_synonym.related_notes.perfect_synonyms._value.add(self._vocab().get_question())
                    nested_synonym.user.answer.set(answer)

    def remove(self, synonym_to_remove: str) -> None:
        self._value.discard(synonym_to_remove)
        (self.notes()
         .for_each(lambda syn: syn.related_notes.perfect_synonyms._value.discard(synonym_to_remove)))

        for to_remove in app.col().vocab.with_question(synonym_to_remove):
            to_remove.related_notes.perfect_synonyms._value.discard(self._vocab().get_question())
            for other_synonym in self.notes():
                other_synonym.related_notes.perfect_synonyms._value.discard(to_remove.get_question())
                to_remove.related_notes.perfect_synonyms._value.discard(other_synonym.get_question())

    @override
    def __repr__(self) -> str: return self._value.__repr__()
