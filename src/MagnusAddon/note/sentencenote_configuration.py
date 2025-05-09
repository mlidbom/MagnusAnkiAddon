from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from note.note_constants import SentenceNoteFields
from note.notefields.string_note_field import StringField
from sysutils import ex_json
from sysutils.ex_json import JsonDictReader
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.sentencenote import SentenceNote
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

class ParsedWord:
    def __init__(self, word: str) -> None:
        self.word = word

    def to_json(self) -> str: return ex_json.dict_to_json({'word': self.word})

    @classmethod
    def from_json(cls, reader: JsonDictReader) -> ParsedWord: return cls(reader.get_string('word'))

class ParsingResult:
    def __init__(self, words: list[ParsedWord], sentence: str, parser_version: str) -> None:
        self.parsed_words = words
        self.sentence = sentence
        self.parser_version = parser_version

    def to_json(self) -> str: return ex_json.dict_to_json({'words': [word.to_json() for word in self.parsed_words],
                                                           'sentence': self.sentence,
                                                           'parser_version': self.parser_version})

    @classmethod
    def from_json(cls, reader: Optional[JsonDictReader]) -> Optional[ParsingResult]:
        return cls([ParsedWord.from_json(word_json) for word_json in reader.get_object_list('words')],
                   reader.get_string('sentence'),
                   reader.get_string('parser_version')) if reader else None

class SentenceConfiguration:
    def __init__(self, json: str) -> None:
        reader = ex_json.json_to_dict(json) if json else None
        self.highlighted_words: list[str] = reader.get_string_list('highlighted_words') if reader else []
        self.incorrect_matches: list[WordExclusion] = \
            [WordExclusion.from_dict(exclusion_data)
             for exclusion_data in reader.get_object_list('incorrect_matches')] if reader else []
        self.parsing_result: Optional[ParsingResult] = ParsingResult.from_json(reader.get_object_or_none('parsing_result')) if reader else None

    def to_json(self) -> str:
        return ex_json.dict_to_json({'highlighted_words': self.highlighted_words,
                                     'incorrect_matches': [exclusion.to_dict() for exclusion in self.incorrect_matches]})

    def incorrect_matches_words(self) -> set[str]:
        return {exclusion.word for exclusion in self.incorrect_matches}

class CachingSentenceConfigurationField:
    def __init__(self, note: SentenceNote) -> None:
        self._field = StringField(note, SentenceNoteFields.configuration)
        self._value: Lazy[SentenceConfiguration] = Lazy(lambda: SentenceConfiguration(self._field.get()))

    def highlighted_words(self) -> list[str]: return self._value.instance().highlighted_words
    def incorrect_matches(self) -> list[WordExclusion]: return self._value.instance().incorrect_matches
    def incorrect_matches_words(self) -> set[str]: return self._value.instance().incorrect_matches_words()

    def _save(self) -> None: self._field.set(self._value.instance().to_json())
