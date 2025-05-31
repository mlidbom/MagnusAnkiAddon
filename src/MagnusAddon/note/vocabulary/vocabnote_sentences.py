from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef


class SentenceCounts:
    def __init__(self, sentences:VocabNoteSentences) -> None:
        sentences = sentences.with_owned_form()
        self.studying_reading = self._get_studying_sentence_count(sentences, NoteFields.VocabNoteType.Card.Reading)
        self.studying_listening = self._get_studying_sentence_count(sentences, NoteFields.VocabNoteType.Card.Listening)
        self.total = len(sentences)

    @staticmethod
    def _get_studying_sentence_count(sentences: list[SentenceNote], card: str = "") -> int:
        return len([sentence for sentence in sentences if sentence.is_studying(card)])

class VocabNoteSentences(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        self.counts:Lazy[SentenceCounts] = Lazy(lambda: SentenceCounts(self))

    @property
    def _vocab(self) -> VocabNote: return self.__vocab()

    @property
    def _collection(self) -> JPCollection: return self._vocab.collection

    def all(self) -> list[SentenceNote]:
        return self._collection.sentences.with_vocab(self._vocab)

    def with_owned_form(self) -> list[SentenceNote]:
        return self._collection.sentences.with_vocab_owned_form(self._vocab)

    def with_primary_form(self) -> list[SentenceNote]:
        return self._collection.sentences.with_form(self._vocab.get_question())

    def user_highlighted(self) -> list[SentenceNote]:
        return list(self._collection.sentences.with_highlighted_vocab(self._vocab))

    def studying(self) -> list[SentenceNote]:
        return [sentence for sentence in self.all() if sentence.is_studying()]
