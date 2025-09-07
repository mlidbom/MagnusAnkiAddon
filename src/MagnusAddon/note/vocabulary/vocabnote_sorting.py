from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

def sort_vocab_list_by_studying_status(vocabs: list[VocabNote], primary_voc: list[str] | None = None, preferred_kanji: str | None = None) -> list[VocabNote]:
    def prefer_primary_vocab_in_order(local_vocab: VocabNote) -> int:
        for index, primary in enumerate(_primary_voc):
            if local_vocab.get_question() == primary or local_vocab.question.without_noise_characters() == primary or (local_vocab.readings.get() and local_vocab.readings.get()[0] == primary):
                return index

        return 1000

    def prefer_vocab_with_kanji(local_vocab: VocabNote) -> int:
        return 0 if preferred_kanji is None or preferred_kanji in local_vocab.get_question() else 1

    def prefer_studying_vocab(local_vocab: VocabNote) -> int:
        return 1 if local_vocab.is_studying() else 2

    def prefer_studying_sentences(local_vocab: VocabNote) -> int:
        return 1 if local_vocab.sentences.studying() else 2

    def prefer_more_sentences(local_vocab: VocabNote) -> int:
        return -len(local_vocab.sentences.all())

    def prefer_high_priority(_vocab: VocabNote) -> int:
        return _vocab.meta_data.priority_spec().priority

    _primary_voc = primary_voc if primary_voc else []

    result = vocabs.copy()

    result.sort(key=lambda local_vocab: (prefer_vocab_with_kanji(local_vocab),
                                         prefer_primary_vocab_in_order(local_vocab),
                                         prefer_studying_vocab(local_vocab),
                                         prefer_studying_sentences(local_vocab),
                                         prefer_more_sentences(local_vocab),
                                         prefer_high_priority(local_vocab),
                                         local_vocab.get_question()))

    return result
