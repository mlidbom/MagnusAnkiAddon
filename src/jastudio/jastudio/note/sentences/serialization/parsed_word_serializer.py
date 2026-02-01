from __future__ import annotations

from typing import TYPE_CHECKING, cast

from anki.notes import NoteId
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils.ex_str import invisible_space

if TYPE_CHECKING:
    from jastudio.note.sentences.parsed_match import ParsedMatch

class ParsedWordSerializer(Slots):
    separator: str = f" {invisible_space} "

    @classmethod
    def to_row(cls, parsed_word: ParsedMatch) -> str: return ParsedWordSerializer.separator.join([
            parsed_word.variant,  # 0
            str(parsed_word.start_index),  # 1
            str(1 if parsed_word.is_displayed else 0),  # 2
            parsed_word.parsed_form,  # 3
            str(parsed_word.vocab_id),  # 4
    ])

    @classmethod
    def from_row(cls, serialized: str) -> ParsedMatch:
        from jastudio.note.sentences.parsed_match import ParsedMatch
        values = serialized.split(ParsedWordSerializer.separator)

        return ParsedMatch(values[0],
                           int(values[1]),
                           values[2] != "0",
                           values[3],
                           cast(NoteId, int(values[4])))
