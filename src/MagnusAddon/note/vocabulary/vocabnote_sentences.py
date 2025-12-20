from __future__ import annotations

import time
from typing import TYPE_CHECKING

from autoslot import Slots  # type: ignore[reportMissingTypeStubs]
from note.note_constants import NoteFields
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection
    from note.sentences.sentencenote import SentenceNote
    from note.vocabulary.vocabnote import VocabNote

class SentenceCounts(Slots):
    def __init__(self, parent: WeakRef[VocabNoteSentences]) -> None:
        self._parent: WeakRef[VocabNoteSentences] = parent
        self._studying_reading: int = 0
        self._studying_listening: int = 0
        self._total: int = 0
        self._last_update_time: float = 0
        self._cache_seconds: int = 0

    @property
    def total(self) -> int: return self._up_to_date_self()._total
    @property
    def studying_reading(self) -> int: return self._up_to_date_self()._studying_reading
    @property
    def studying_listening(self) -> int: return self._up_to_date_self()._studying_listening

    def _up_to_date_self(self) -> SentenceCounts:
        def _how_long_to_cache_for() -> int:
            if self._total < 10: return 60
            if self._total < 100: return 600
            return 6000

        def get_studying_sentence_count(card: str = "") -> int:
            return len([sentence for sentence in sentences if sentence.is_studying(card)])

        if time.time() - self._last_update_time > self._cache_seconds:
            self._last_update_time = time.time()
            sentences = self._parent().with_owned_form()
            self._studying_reading = get_studying_sentence_count(NoteFields.VocabNoteType.Card.Reading)
            self._studying_listening = get_studying_sentence_count(NoteFields.VocabNoteType.Card.Listening)
            self._total = len(sentences)
            self._cache_seconds = _how_long_to_cache_for()
        return self

class VocabNoteSentences(WeakRefable, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.__vocab = vocab
        weakrefthis = WeakRef(self)
        self.counts: Lazy[SentenceCounts] = Lazy(lambda: SentenceCounts(weakrefthis))

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
