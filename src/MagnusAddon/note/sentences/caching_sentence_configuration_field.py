from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from autoslot import Slots
from note.note_constants import SentenceNoteFields
from note.notefields.string_field import StringField
from note.sentences.sentence_configuration import SentenceConfiguration
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.sentences.sentencenote import SentenceNote
    from note.sentences.word_exclusion_set import WordExclusionSet

class CachingSentenceConfigurationField(WeakRefable, Slots):
    def __init__(self, sentence: WeakRef[SentenceNote]) -> None:
        self._sentence = sentence
        self.field = StringField(sentence, SentenceNoteFields.configuration)

        weak_self_ref = WeakRef(self)
        self._value: Lazy[SentenceConfiguration] = Lazy(lambda: SentenceConfiguration.serializer.deserialize(self.field.get(), weak_self_ref()._save))

        self._update_callbacks: list[Callable[[], None]] = []

    @property
    def configuration(self) -> SentenceConfiguration:
        return self._value()

    @property
    def incorrect_matches(self) -> WordExclusionSet: return self._value.instance().incorrect_matches

    @property
    def hidden_matches(self) -> WordExclusionSet: return self._value.instance().hidden_matches

    def highlighted_words(self) -> set[str]: return self._value.instance().highlighted_words

    def remove_highlighted_word(self, word: str) -> None:
        self.highlighted_words().discard(word)
        self._save()

    def reset_highlighted_words(self) -> None:
        self._value.instance().highlighted_words.clear()
        self._save()

    def add_highlighted_word(self, vocab: str) -> None:
        self.highlighted_words().add(vocab.strip())
        self._save()

    def _save(self) -> None:
        self.field.set(SentenceConfiguration.serializer.serialize(self._value.instance()))
        self._sentence().update_parsed_words(force=True)
