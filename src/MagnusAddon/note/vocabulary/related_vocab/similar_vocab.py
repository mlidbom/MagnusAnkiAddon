from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots

if TYPE_CHECKING:
    from note.notefields.json_object_field import JsonObjectField
    from note.vocabulary.related_vocab.related_vocab_data import RelatedVocabData
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class SimilarVocab(Slots):
    def __init__(self, vocab: WeakRef[VocabNote], data: JsonObjectField[RelatedVocabData]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self._data: JsonObjectField[RelatedVocabData] = data

    def get(self) -> set[str]: return self._data.get().similar

    def add(self, new_similar: str) -> None:
        self.get().add(new_similar)

        for similar in app.col().vocab.with_question(new_similar):
            if self._vocab().get_question() not in similar.related_notes.similar_meanings():
                similar.related_notes.add_similar_meaning(self._vocab().get_question(), _is_recursive_call=True)
