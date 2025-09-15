from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from sysutils.linq.l_iterable import linq

if TYPE_CHECKING:
    from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class PerfectSynonyms(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: FieldSetWrapper[str]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._value: FieldSetWrapper[str] = data

    def notes(self) -> list[VocabNote]: return app.col().vocab.with_any_question_in(list(self._value.get()))

    def add(self, synonym: str) -> None:
        self._value.add(synonym)
        (linq(app.col().vocab.with_question(synonym))
         .select(lambda syn: syn.related_notes.perfect_synonyms)
         .for_single_or_none(lambda other_synonyms: other_synonyms._value.add(self._vocab().get_question())))

    def remove(self, to_remove: str) -> None:
        self._value.remove(to_remove)
        (linq(app.col().vocab.with_any_question_in(self._value.get()))
         .select(lambda syn: syn.related_notes.perfect_synonyms)
         .for_each(lambda other_synonyms: other_synonyms._value.remove(self._vocab().get_question())))
