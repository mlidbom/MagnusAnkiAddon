from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
from note.sentences.serialization.parsed_word_serializer import ParsedWordSerializer
from sysutils.ex_str import invisible_space

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class ParsedWord(Slots):
    serializer: ParsedWordSerializer = ParsedWordSerializer()
    def __init__(self, start_index: int, is_displayed: bool, type: str, word: str, base: str, vocab_id: int, information_string: str) -> None:
        self.start_index: int = start_index
        self.is_displayed: bool = is_displayed
        self.type: str = type
        self.word: str = word
        self.base_form: str = base
        self.vocab_id: int = vocab_id
        self.information_string = information_string

    @classmethod
    def _base_form_from_match(self, match: Match) -> str:
        if not match.base_form: return "NONE"
        return match.base_form if match.base_form != match.base_form else "SAME"

    @classmethod
    def from_match(cls, match: Match) -> ParsedWord:
        return cls(match.start_index,
                   match.is_displayed,
                   "S" if match.variant.is_surface else "B",
                   match.parsed_form,
                   cls._base_form_from_match(match),
                   match.vocab.get_id() if isinstance(match, VocabMatch) else -1,
                   f"""{" ".join(match.failure_reasons)} {invisible_space} {" ".join(match.hiding_reasons)} {"highlighted" if match.is_highlighted else ""}""")
