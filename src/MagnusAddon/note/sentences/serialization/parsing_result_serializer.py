from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.notefields.json_object_field import ObjectSerializer
from note.sentences.parsed_word import ParsedWord
from sysutils.ex_str import newline

if TYPE_CHECKING:
    from note.sentences.parsing_result import ParsingResult

class ParsingResultSerializer(ObjectSerializer["ParsingResult"], Slots):
    def deserialize(self, json: str) -> ParsingResult:
        from note.sentences.parsing_result import ParsingResult

        rows = json.split(newline)
        if len(rows) < 2: return ParsingResult([], "", "")

        return ParsingResult([ParsedWord.serializer.from_row(row) for row in rows[2:]],
                             rows[1],
                             rows[0]) if json else ParsingResult([], "", "")

    def serialize(self, parsing_result: ParsingResult) -> str:
        return newline.join([parsing_result.parser_version,
                             parsing_result.sentence]
                            + [ParsedWord.serializer.to_dict(word) for word in parsing_result.parsed_words])
