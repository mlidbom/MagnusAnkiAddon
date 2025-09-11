from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
from note.sentences.serialization.parsed_word_serializer import ParsedWordSerializer

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match

class ParsedWord(Slots):
    serializer: ParsedWordSerializer = ParsedWordSerializer()
    def __init__(self, word: str, base: str, vocab_id: int, is_displayed: bool, start_index: int) -> None:
        self.word: str = word
        self.vocab_id: int = vocab_id
        self.is_displayed: bool = is_displayed
        self.start_index: int = start_index
        self.base_form: str = base

    @classmethod
    def _base_form_from_match(self, match: Match) -> str:
        if not match.base_form: return "NONE"
        return match.base_form if match.base_form != match.base_form else "SAME"

    @classmethod
    def from_match(cls, match: Match) -> ParsedWord:
        return cls(match.parsed_form,
                   cls._base_form_from_match(match),
                   match.vocab.get_id() if isinstance(match, VocabMatch) else -1,
                   match.is_displayed,
                   match.start_index)
