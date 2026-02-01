from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.note.note_constants import SentenceNoteFields
from jaslib.note.notefields.mutable_string_field import MutableStringField
from jaslib.note.sentences.sentence_configuration import SentenceConfiguration
from jaslib.sysutils.weak_ref import WeakRef, WeakRefable
from typed_linq_collections.collections.q_set import QSet

from jaslib import app

if TYPE_CHECKING:
    from jaslib.note.sentences.sentencenote import SentenceNote
    from jaslib.note.sentences.word_exclusion_set import WordExclusionSet
    from jaslib.note.vocabulary.vocabnote import VocabNote
    from typed_linq_collections.collections.q_unique_list import QUniqueList

class CachingSentenceConfigurationField(WeakRefable, Slots):
    def __init__(self, sentence: WeakRef[SentenceNote]) -> None:
        self._sentence: WeakRef[SentenceNote] = sentence
        self.field: MutableStringField = MutableStringField(sentence, SentenceNoteFields.configuration)
        self._value: SentenceConfiguration = SentenceConfiguration.serializer().deserialize(self.field.value, self._save)

    @property
    def configuration(self) -> SentenceConfiguration:
        return self._value

    @property
    def incorrect_matches(self) -> WordExclusionSet: return self._value.incorrect_matches

    @property
    def hidden_matches(self) -> WordExclusionSet: return self._value.hidden_matches

    def highlighted_words(self) -> QUniqueList[str]: return self._value.highlighted_words

    @property
    def highlighted_vocab(self) -> QSet[VocabNote]:
        return QSet(vocab for vocab in (app.col().vocab.with_any_form_in(list(self.highlighted_words())))
                    if vocab.get_id() in self._sentence().parsing_result.get().matched_vocab_ids)

    # noinspection PyUnusedFunction
    def remove_highlighted_word(self, word: str) -> None:
        self.highlighted_words().discard(word)
        self._save()

    # noinspection PyUnusedFunction
    def reset_highlighted_words(self) -> None:
        self._value.highlighted_words.clear()
        self._save()

    def add_highlighted_word(self, vocab: str) -> None:
        self.highlighted_words().add(vocab.strip())
        self._save()

    def _save(self) -> None:
        self.field.set(SentenceConfiguration.serializer().serialize(self._value))
        self._sentence().update_parsed_words(force=True)
