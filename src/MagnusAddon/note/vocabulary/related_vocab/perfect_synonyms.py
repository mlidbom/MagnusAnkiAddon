from __future__ import annotations

from typing import TYPE_CHECKING, override

from ankiutils import app
from ex_autoslot import AutoSlots
from sysutils.collections.linq.q_iterable import QSet

if TYPE_CHECKING:
    from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.collections.linq.q_iterable import QList
    from sysutils.weak_ref import WeakRef

class PerfectSynonyms(AutoSlots):
    def __init__(self, vocab: WeakRef[VocabNote], data: FieldSetWrapper[str]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._value: FieldSetWrapper[str] = data
        vocab().user.answer.on_change(self.push_answer_to_other_synonyms)

    def notes(self) -> QList[VocabNote]: return app.col().vocab.with_any_question_in(list(self._value.get()))

    def push_answer_to_other_synonyms(self) -> None:
        for synonym in self.notes():
            synonym.user.answer.set(self._vocab().user.answer.value)

    def get(self) -> set[str]: return self._value.get()

    def _remove_internal(self, synonym: str) -> None:
        self._value.discard(synonym)
        self._vocab().related_notes.synonyms.add(synonym)

    def _add_internal(self, synonym: str) -> None:
        if synonym == self._vocab().get_question(): return
        self._value.add(synonym)
        self._vocab().related_notes.synonyms.add(synonym)

    def _resolve_whole_web(self) -> QSet[VocabNote]:
        found: QSet[VocabNote] = QSet()
        def recurse_into(syn: VocabNote) -> None:
            found.add(syn)
            for related in syn.related_notes.perfect_synonyms.notes():
                if related not in found:
                    recurse_into(related)

        recurse_into(self._vocab())
        for syn in self.notes():
            recurse_into(syn)
        return found

    def _ensure_all_perfect_synonyms_are_connected(self) -> None:
        whole_web = self._resolve_whole_web()

        all_questions = whole_web.select(lambda syn: syn.get_question()).to_set()
        for synonym in whole_web:
            for question in all_questions:
                synonym.related_notes.perfect_synonyms._add_internal(question)

    def add_overwriting_the_answer_of_the_added_synonym(self, added_question: str) -> None:
        if added_question == self._vocab().get_question(): return
        self._add_internal(added_question)
        self._ensure_all_perfect_synonyms_are_connected()
        self.push_answer_to_other_synonyms()

    def remove(self, synonym_to_remove: str) -> None:
        for to_remove in app.col().vocab.with_question(synonym_to_remove):
            to_remove.related_notes.perfect_synonyms._value.clear()
        for syn in self._resolve_whole_web():
            syn.related_notes.perfect_synonyms._remove_internal(synonym_to_remove)

    @override
    def __repr__(self) -> str: return self._value.__repr__()
