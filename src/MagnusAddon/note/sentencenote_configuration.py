from __future__ import annotations
from typing import Any, TYPE_CHECKING

from note.note_constants import SentenceNoteFields
from note.notefields.string_note_field import StringField
from sysutils import ex_json
from sysutils.ex_json import JsonDictReader
from sysutils.lazy import Lazy
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

if TYPE_CHECKING:
    from note.sentencenote import SentenceNote
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

class ParsedWord:
    def __init__(self, word: str) -> None:
        self.word = word

    def to_dict(self) -> dict[str, Any]: return {'word': self.word}

    @classmethod
    def from_json(cls, reader: JsonDictReader) -> ParsedWord: return cls(reader.get_string('word'))

class ParsingResult:
    def __init__(self, words: list[ParsedWord], sentence: str, parser_version: str) -> None:
        self.parsed_words = words
        self.sentence = sentence
        self.parser_version = parser_version

    def to_dict(self) -> dict[str, Any]: return {'words': [word.to_dict() for word in self.parsed_words],
                                                 'sentence': self.sentence,
                                                 'parser_version': self.parser_version}

    def parsed_words_strings(self) -> list[str]: return [parsed.word for parsed in self.parsed_words]

    @classmethod
    def from_json(cls, reader: JsonDictReader) -> ParsingResult:
        return cls([ParsedWord.from_json(word_json) for word_json in reader.get_object_list('words')],
                   reader.get_string('sentence'),
                   reader.get_string('parser_version'))
    @classmethod
    def empty(cls) -> ParsingResult:
        return cls([], "", "")

class SentenceConfiguration:
    def __init__(self, highlighted_words: list[str], incorrect_matches: list[WordExclusion], parsing_result: ParsingResult) -> None:
        self.highlighted_words: list[str] = highlighted_words
        self.incorrect_matches: list[WordExclusion] = incorrect_matches
        self.parsing_result: ParsingResult = parsing_result

    def to_json(self) -> str:
        return ex_json.dict_to_json({'highlighted_words': self.highlighted_words,
                                     'incorrect_matches': [exclusion.to_dict() for exclusion in self.incorrect_matches],
                                     'parsing_result': self.parsing_result.to_dict()})

    @classmethod
    def from_json(cls, json: str) -> SentenceConfiguration:
        try:
            reader = ex_json.json_to_dict(json) if json else None
            highlighted_words: list[str] = reader.get_string_list('highlighted_words') if reader else []
            incorrect_matches: list[WordExclusion] = \
                [WordExclusion.from_dict(exclusion_data)
                 for exclusion_data in reader.get_object_list('incorrect_matches')] if reader else []

            parsing_json_dict = reader.get_object_or_none('parsing_result') if reader else None
            parsing_result: ParsingResult = ParsingResult.from_json(parsing_json_dict) if parsing_json_dict else ParsingResult.empty()

            return cls(highlighted_words, incorrect_matches, parsing_result)
        except: #todo: remove this ugly hack
            return SentenceConfiguration([], [], ParsingResult.empty())

    def incorrect_matches_words(self) -> set[str]:
        return {exclusion.word for exclusion in self.incorrect_matches}

class CachingSentenceConfigurationField:
    def __init__(self, note: SentenceNote) -> None:
        self._field = StringField(note, SentenceNoteFields.configuration)
        self._value: Lazy[SentenceConfiguration] = Lazy(lambda: SentenceConfiguration.from_json(self._field.get()))

    def highlighted_words(self) -> list[str]: return self._value.instance().highlighted_words
    def incorrect_matches(self) -> list[WordExclusion]: return self._value.instance().incorrect_matches
    def incorrect_matches_words(self) -> set[str]: return self._value.instance().incorrect_matches_words()

    def remove_highlighted_word(self, word: str) -> None:
        if word in self.highlighted_words():
            self.highlighted_words().remove(word)
        self._save()

    def _set_incorrect_matches(self, exclusions: set[WordExclusion]) -> None:
        self._value.instance().incorrect_matches = sorted(exclusions, key=lambda x: x.index)
        self._save()

    def _set_highlighted_words(self, words: list[str]) -> None:
        self._value.instance().highlighted_words = words
        self._save()

    def reset_highlighted_words(self) -> None: self._set_highlighted_words([])

    def reset_incorrect_matches(self) -> None: self._set_incorrect_matches(set())

    def add_incorrect_match(self, vocab: str) -> None:
        self._value.instance().incorrect_matches.append(WordExclusion.from_string(vocab))
        self._save()

    def position_highlighted_word(self, vocab: str, index: int = -1) -> None:
        vocab = vocab.strip()
        self.remove_highlighted_word(vocab)
        if index == -1:
            self.highlighted_words().append(vocab)
        else:
            self.highlighted_words().insert(index, vocab)
        self._save()

    def remove_incorrect_match(self, exclusion: WordExclusion) -> None:
        if exclusion in self.incorrect_matches():
            self.incorrect_matches().remove(exclusion)
        self._save()

    def parsing_result(self) -> ParsingResult: return self._value.instance().parsing_result
    def set_parsing_result(self, analysis: TextAnalysis) -> None:
        self._value.instance().parsing_result = ParsingResult([ParsedWord(word.form) for word in analysis.all_words],
                                                              analysis.text,
                                                              analysis.version)
        self._save()

    def _save(self) -> None: self._field.set(self._value.instance().to_json())
