from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from ankiutils.app import col
from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.json_object_field import JsonObjectField
    from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class Antonyms(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: JsonObjectField[RelatedVocabData]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._data: JsonObjectField[RelatedVocabData] = data

    def strings(self) -> set[str]: return self._data.get().antonyms
    def notes(self) -> list[VocabNote]:
        return col().vocab.with_any_form_in_prefer_exact_match(list(self.strings()))

    def add(self, antonym: str) -> None:
        self.strings().add(antonym)

        for similar in app.col().vocab.with_question(antonym):
            if self._vocab().get_question() not in similar.related_notes.antonyms.strings():
                similar.related_notes.antonyms.add(self._vocab().get_question())

        self._data.save()

    def remove(self, to_remove: str) -> None:
        self.strings().remove(to_remove)

        for similar in app.col().vocab.with_question(to_remove):
            if self._vocab().get_question() in similar.related_notes.antonyms.strings():
                similar.related_notes.antonyms.remove(self._vocab().get_question())

        self._data.save()