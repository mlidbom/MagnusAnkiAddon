from __future__ import annotations

from typing import TYPE_CHECKING, Any

from note.sentences.parsed_word import ParsedWord

if TYPE_CHECKING:
    from note.sentences.parsing_result import ParsingResult
    from sysutils.ex_json import JsonDictReader

class ParsingResultSerializer:
    @staticmethod
    def to_dict(self: ParsingResult) -> dict[str, Any]: return {'words': [ParsedWord.serializer.to_dict(word) for word in self.parsed_words],
                                                                'sentence': self.sentence,
                                                                'parser_version': self.parser_version}

    @staticmethod
    def from_reader(reader: JsonDictReader) -> ParsingResult:
        from note.sentences.parsing_result import ParsingResult
        return ParsingResult(reader.object_list('words', ParsedWord.serializer.from_reader),
                             reader.string('sentence'),
                             reader.string('parser_version'))
