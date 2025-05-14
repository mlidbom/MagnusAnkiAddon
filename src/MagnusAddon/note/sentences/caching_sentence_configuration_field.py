from __future__ import annotations

from typing import TYPE_CHECKING

from note.note_constants import SentenceNoteFields
from note.notefields.string_field import StringField
from note.sentences.parsed_word import ParsedWord
from note.sentences.parsing_result import ParsingResult
from note.sentences.sentence_configuration import SentenceConfiguration
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from note.sentences.sentencenote import SentenceNote
    from note.sentences.word_exclusion_set import WordExclusionSet

class CachingSentenceConfigurationField:
    def __init__(self, note: SentenceNote) -> None:
        self.field = StringField(note, SentenceNoteFields.configuration)
        self._value: Lazy[SentenceConfiguration] = Lazy(lambda: SentenceConfiguration.serializer.deserialize(self.field.get(), self._save))

    @property
    def incorrect_matches(self) -> WordExclusionSet: return self._value.instance().incorrect_matches

    @property
    def hidden_matches(self) -> WordExclusionSet: return self._value.instance().hidden_matches

    def highlighted_words(self) -> list[str]: return self._value.instance().highlighted_words

    def remove_highlighted_word(self, word: str) -> None:
        if word in self.highlighted_words():
            self.highlighted_words().remove(word)
        self._save()

    def reset_highlighted_words(self) -> None:
        self._value.instance().highlighted_words = []
        self._save()

    def position_highlighted_word(self, vocab: str, index: int = -1) -> None:
        vocab = vocab.strip()
        self.remove_highlighted_word(vocab)
        if index == -1:
            self.highlighted_words().append(vocab)
        else:
            self.highlighted_words().insert(index, vocab)
        self._save()

    def parsing_result(self) -> ParsingResult: return self._value.instance().parsing_result
    def set_parsing_result(self, analysis: TextAnalysis) -> None:
        self._value.instance().parsing_result = ParsingResult([ParsedWord(word.form) for word in analysis.all_words],
                                                              analysis.text,
                                                              analysis.version)
        self._save()

    def _save(self) -> None:
        self.field.set(SentenceConfiguration.serializer.serialize(self._value.instance()))
