from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
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

    def get(self) -> set[str]: return self._data.get().synonyms

    def add(self, antonym: str) -> None:
        self.get().add(antonym)

        for similar in app.col().vocab.with_question(antonym):
            if self._vocab().get_question() not in similar.related_notes.antonyms.get():
                similar.related_notes.antonyms.add(self._vocab().get_question())

        self._data.save()

    def remove(self, to_remove: str) -> None:
        self.get().remove(to_remove)

        for similar in app.col().vocab.with_question(to_remove):
            if self._vocab().get_question() in similar.related_notes.antonyms.get():
                similar.related_notes.antonyms.remove(self._vocab().get_question())

        self._data.save()
