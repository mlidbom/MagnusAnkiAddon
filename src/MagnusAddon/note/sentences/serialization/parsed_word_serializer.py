from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedWord
    from sysutils.ex_json import JsonDictReader


class ParsedWordSerializer:
    @staticmethod
    def to_dict(self:ParsedWord) -> dict[str, Any]: return {"word": self.word}

    @staticmethod
    def from_reader(reader: JsonDictReader) -> ParsedWord:
        from note.sentences.parsed_word import ParsedWord
        return ParsedWord(reader.string("word"))