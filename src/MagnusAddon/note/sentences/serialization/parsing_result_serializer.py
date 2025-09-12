from __future__ import annotations

from typing import TYPE_CHECKING, override

import mylog
from autoslot import Slots
from note.notefields.json_object_field import ObjectSerializer
from note.sentences.parsed_word import ParsedMatch
from sysutils.ex_str import invisible_space, newline

if TYPE_CHECKING:
    from note.sentences.parsing_result import ParsingResult

class ParsingResultSerializer(ObjectSerializer["ParsingResult"], Slots):
    newline_replacement = f"NEWLINE{invisible_space}"
    @override
    def deserialize(self, serialized: str) -> ParsingResult:
        from note.sentences.parsing_result import ParsingResult

        rows = serialized.split(newline)
        if len(rows) < 2: return ParsingResult([], "", "")

        # noinspection PyBroadException
        try:
            return ParsingResult([ParsedMatch.serializer.from_row(row) for row in rows[2:]],
                                 self._restore_newline(rows[1]),
                                 rows[0]) if serialized else ParsingResult([], "", "")
        except Exception as ex:
            mylog.warning(f"""Failed to deserialize ParsingResult:
            message:
{ex}
{serialized}""")
            return ParsingResult([], "", "")

    def _replace_newline(self, value: str) -> str:
        return value.replace(newline, self.newline_replacement)

    def _restore_newline(self, serialized_value: str) -> str:
        return serialized_value.replace(self.newline_replacement, newline)

    @override
    def serialize(self, parsing_result: ParsingResult) -> str:
        return newline.join([parsing_result.parser_version,
                             self._replace_newline(parsing_result.sentence)]
                            + [ParsedMatch.serializer.to_row(word) for word in parsing_result.parsed_words])
