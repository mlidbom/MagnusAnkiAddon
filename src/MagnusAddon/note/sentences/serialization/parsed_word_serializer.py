from __future__ import annotations

from typing import TYPE_CHECKING, Any

from autoslot import Slots

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedWord
    from sysutils.json.json_reader import JsonReader

class ParsedWordSerializer(Slots):
    @staticmethod
    def to_dict(self: ParsedWord) -> dict[str, Any]: return {"w": self.word,
                                                             "s": self.surface,
                                                             "v": self.vocab_id,
                                                             "d": 1 if self.is_displayed else 0,
                                                             "i": self.start_index}

    @staticmethod
    def from_reader(reader: JsonReader) -> ParsedWord:
        from note.sentences.parsed_word import ParsedWord
        return ParsedWord(reader.string("w"),
                          reader.string("s"),
                          reader.integer("v"),
                          reader.integer("d") == 1,
                          reader.integer("i"))
