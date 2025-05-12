from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection
    from note.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteSentences:
    def __init__(self, vocab: VocabNote) -> None:
        self._vocab = vocab

    @property
    def _collection(self) -> JPCollection: return self._vocab.collection

    def all(self) -> list[SentenceNote]:
        return self._collection.sentences.with_vocab(self._vocab)

    def with_owned_form(self) -> list[SentenceNote]:
        return self._collection.sentences.with_vocab_owned_form(self._vocab)

    def with_primary_form(self) -> list[SentenceNote]:
        return self._collection.sentences.with_form(self._vocab.get_question())

    def user_highlighted(self) -> list[SentenceNote]:
        return [sentence for sentence in self._collection.sentences.with_highlighted_vocab(self._vocab)]

    def studying(self) -> list[SentenceNote]:
        return [sentence for sentence in self.all() if sentence.is_studying()]
