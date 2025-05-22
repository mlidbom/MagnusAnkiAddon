from __future__ import annotations

from typing import TYPE_CHECKING, Any

from autoslot import Slots

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedWord
    from sysutils.json.json_reader import JsonReader

class ParsedWordSerializer(Slots):
    @staticmethod
    def to_dict(self:ParsedWord) -> dict[str, Any]: return {"word": self.word}

    @staticmethod
    def from_reader(reader: JsonReader) -> ParsedWord:
        from note.sentences.parsed_word import ParsedWord
        return ParsedWord(reader.string("word"))