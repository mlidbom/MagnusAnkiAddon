from __future__ import annotations

from typing import TYPE_CHECKING

from anki.notes import NoteId
from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
from note.sentences.serialization.parsed_word_serializer import ParsedWordSerializer
from sysutils.ex_str import invisible_space

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class ParsedMatch(Slots):
    serializer: ParsedWordSerializer = ParsedWordSerializer()
    def __init__(self, variant: str, start_index: int, is_displayed: bool, word: str, information_string: str, vocab_id: NoteId) -> None:
        self.start_index: int = start_index
        self.is_displayed: bool = is_displayed
        self.variant: str = variant
        self.parsed_form: str = word
        self.vocab_id: NoteId = vocab_id
        self.information_string = information_string

    @property
    def end_index(self) -> int: return self.start_index + len(self.parsed_form)

    @classmethod
    def from_match(cls, match: Match) -> ParsedMatch:
        return ParsedMatch("S" if match.variant.is_surface else "B",
                           match.start_index,
                           match.is_displayed,
                           match.parsed_form,
                           f"""{" ".join(match.failure_reasons)}{f" {invisible_space} " if match.failure_reasons else ""}{" ".join(match.hiding_reasons)} {"highlighted" if match.is_highlighted else ""}""",
                           match.vocab.get_id() if isinstance(match, VocabMatch) else NoteId(-1))
