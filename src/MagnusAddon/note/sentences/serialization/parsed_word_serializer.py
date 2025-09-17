from __future__ import annotations

from typing import TYPE_CHECKING, cast

from anki.notes import NoteId
from ex_autoslot import ProfilableAutoSlots
from sysutils.ex_str import invisible_space

if TYPE_CHECKING:
    from note.sentences.parsed_word import ParsedMatch

class ParsedWordSerializer(ProfilableAutoSlots):
    separator: str = f" {invisible_space} "

    @staticmethod
    def to_row(parsed_word: ParsedMatch) -> str: return ParsedWordSerializer.separator.join([
        parsed_word.variant,  # 0
        str(parsed_word.start_index),  # 1
        str(1 if parsed_word.is_displayed else 0),  # 2
        parsed_word.parsed_form,  # 3
        parsed_word.information_string or "#",  # 4
        str(parsed_word.vocab_id),  # 5
    ])

    @staticmethod
    def from_row(serialized: str) -> ParsedMatch:
        from note.sentences.parsed_word import ParsedMatch
        values = serialized.split(ParsedWordSerializer.separator)

        return ParsedMatch(values[0],
                           int(values[1]),
                           values[2] != "0",
                           values[3],
                           values[4],
                           cast(NoteId, int(values[5])))
