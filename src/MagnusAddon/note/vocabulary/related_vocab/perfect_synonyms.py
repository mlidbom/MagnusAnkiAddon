from __future__ import annotations

from typing import TYPE_CHECKING

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

    def add(self, synonym_question: str) -> None:
        self._value.add(synonym_question)
        (app.col().vocab.with_question(synonym_question)
         .select_many(lambda synonym_note: synonym_note.related_notes.perfect_synonyms.notes())
         .for_each(lambda syn: syn.related_notes.perfect_synonyms._value.add(self._vocab().get_question())))

    def remove(self, synonym_question: str) -> None:
        self._value.remove(synonym_question)
        (self.notes()
         .for_each(lambda syn: syn.related_notes.perfect_synonyms._value.remove(self._vocab().get_question())))
      