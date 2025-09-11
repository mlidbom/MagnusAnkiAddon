from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.ex_str import invisible_space

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedWord

class ParsedWordSerializer(Slots):
    separator = f" {invisible_space} "

    @staticmethod
    def to_dict(self: ParsedWord) -> str: return ParsedWordSerializer.separator.join([
        str(self.start_index),  # 0
        str(1 if self.is_displayed else 0),  # 1
        self.word,  # 2
        self.base_form,  # 3
        str(self.vocab_id),  # 4
    ])

    @staticmethod
    def from_row(serialized: str) -> ParsedWord:
        from note.sentences.parsed_word import ParsedWord
        values = serialized.split(ParsedWordSerializer.separator)
        try:
            return ParsedWord(values[2],
                              values[3],
                              int(values[4]),
                              bool(int(values[1])),
                              int(values[0]))
        except Exception:
            return ParsedWord("", "", 0, False, 0)
