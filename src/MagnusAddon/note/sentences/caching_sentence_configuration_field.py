from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.note_constants import SentenceNoteFields
from note.notefields.string_field import StringField
from note.sentences.parsed_word import ParsedWord
from note.sentences.parsing_result import ParsingResult
from note.sentences.sentence_configuration import SentenceConfiguration
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
    from note.sentences.sentencenote import SentenceNote


class CachingSentenceConfigurationField:
    def __init__(self, note: SentenceNote) -> None:
        self._field = StringField(note, SentenceNoteFields.configuration)
        self._value: Lazy[SentenceConfiguration] = Lazy(lambda: SentenceConfiguration.from_json(self._field.get()))

    def highlighted_words(self) -> list[str]: return self._value.instance().highlighted_words
    def incorrect_matches(self) -> set[WordExclusion]: return self._value.instance().incorrect_matches
    def incorrect_matches_words(self) -> set[str]: return self._value.instance().incorrect_matches_words()

    def remove_highlighted_word(self, word: str) -> None:
        if word in self.highlighted_words():
            self.highlighted_words().remove(word)
        self._save()

    def _set_incorrect_matches(self, exclusions: set[WordExclusion]) -> None:
        self._value.instance().incorrect_matches = exclusions
        self._save()

    def _set_highlighted_words(self, words: list[str]) -> None:
        self._value.instance().highlighted_words = words
        self._save()

    def reset_highlighted_words(self) -> None: self._set_highlighted_words([])

    def reset_incorrect_matches(self) -> None: self._set_incorrect_matches(set())

    def add_incorrect_match(self, vocab: str) -> None:
        self._value.instance().incorrect_matches.add(WordExclusion.from_string(vocab))
        self._save()

    def position_highlighted_word(self, vocab: str, index: int = -1) -> None:
        vocab = vocab.strip()
        self.remove_highlighted_word(vocab)
        if index == -1:
            self.highlighted_words().append(vocab)
        else:
            self.highlighted_words().insert(index, vocab)
        self._save()

    def remove_incorrect_match_string(self, to_remove: str) -> None:
        for exclusion in [ex for ex in self.incorrect_matches() if ex.word == to_remove]:
            self.incorrect_matches().remove(exclusion)
        self._save()

    def parsing_result(self) -> ParsingResult: return self._value.instance().parsing_result
    def set_parsing_result(self, analysis: TextAnalysis) -> None:
        self._value.instance().parsing_result = ParsingResult([ParsedWord(word.form) for word in analysis.all_words],
                                                              analysis.text,
                                                              analysis.version)
        self._save()

    def _save(self) -> None: self._field.set(self._value.instance().to_json())
