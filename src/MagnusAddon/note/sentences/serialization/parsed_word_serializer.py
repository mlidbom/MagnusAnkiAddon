from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.ex_str import invisible_space

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedWord

class ParsedWordSerializer(Slots):
    separator = f" {invisible_space} "

    @staticmethod
    def to_row(parsed_word: ParsedWord) -> str: return ParsedWordSerializer.separator.join([
        str(parsed_word.start_index),  # 0
        str(1 if parsed_word.is_displayed else 0),  # 1
        parsed_word.type, # 2
        parsed_word.word,  # 3
        parsed_word.base_form,  # 4
        str(parsed_word.vocab_id),  # 5
        parsed_word.information_string,  # 6
    ])

    @staticmethod
    def from_row(serialized: str) -> ParsedWord:
        from note.sentences.parsed_word import ParsedWord
        values = serialized.split(ParsedWordSerializer.separator)

        return ParsedWord(int(values[0]),
                          bool(int(values[1])),
                          values[2],
                          values[3],
                          values[4],
                          int(values[5]),
                          "")
