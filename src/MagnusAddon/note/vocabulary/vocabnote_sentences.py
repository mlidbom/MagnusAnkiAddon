from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteSentences:
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab

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
