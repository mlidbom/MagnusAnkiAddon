from __future__ import annotations

from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.match import Match
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.sentences.sentence_configuration import SentenceConfiguration

class MatchStateTest:
    def __init__(self, match: Match, name: str) -> None:
        self._match: Match = match
        self.name: str = name

    @property
    def match(self) -> Match: return self._match
    @property
    def match_is_in_state(self) -> bool: raise NotImplementedError()
    @property
    def state_description(self) -> str: return self.name if self.match_is_in_state else f"not::{self.name}"
    @property
    def tokenized_form(self) -> str: return self.match.tokenized_form
    @property
    def variant(self) -> CandidateWordVariant: return self.match.variant
    @property
    def word(self) -> CandidateWord: return self.variant.word
    @property
    def end_location(self) -> TextAnalysisLocation: return self.word.end_location
    @property
    def configuration(self) -> SentenceConfiguration: return self.variant.configuration
    @property
    def start_index(self) -> int: return self.match.start_index

    @override
    def __repr__(self) -> str: return self.state_description
