from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.json_object_field import JsonObjectSerializer
from note.sentences.parsed_word import ParsedWord
from sysutils.json import ex_json
from sysutils.json.json_reader import JsonReader

if TYPE_CHECKING:
    from note.sentences.parsing_result import ParsingResult

class ParsingResultSerializer(JsonObjectSerializer["ParsingResult"], Slots):

    def deserialize(self, json: str) -> ParsingResult:
        from note.sentences.parsing_result import ParsingResult
        if not json: return ParsingResult([], "", "")

        reader = JsonReader.from_json(json)
        return ParsingResult(reader.object_list("words", ParsedWord.serializer.from_reader),
                             reader.string("sentence"),
                             reader.string("parser_version")) if json else ParsingResult([], "", "")

    def serialize(self, parsing_result: ParsingResult) -> str:
        return ex_json.dict_to_json({"words": [ParsedWord.serializer.to_dict(word) for word in parsing_result.parsed_words],
                                     "sentence": parsing_result.sentence,
                                     "parser_version": parsing_result.parser_version})
