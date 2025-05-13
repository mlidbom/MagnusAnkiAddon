from __future__ import annotations

from typing import TYPE_CHECKING, Any

from note.sentences.parsed_word import ParsedWord

if TYPE_CHECKING:
    from sysutils.ex_json import JsonDictReader


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
