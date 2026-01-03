from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from language_services.janome_ex.word_extraction import analysis_constants  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.match import Match
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.sentences.sentence_configuration import SentenceConfiguration
    from sysutils.weak_ref import WeakRef

class MatchInspector(Slots):
    """Base class providing access to Match context and helper properties.

    This class holds a weak reference to a Match and provides convenient
    properties for inspecting the match's word, variant, location, and surrounding context.
    """

    def __init__(self, match: WeakRef[Match]) -> None:
        self._match: WeakRef[Match] = match

    @property
    def match(self) -> Match:
        return self._match()

    @property
    def variant(self) -> CandidateWordVariant:
        return self.match.variant

    @property
    def word(self) -> CandidateWord:
        return self.variant.word

    @property
    def start_location(self) -> TextAnalysisLocation:
        return self.word.start_location

    @property
    def end_location(self) -> TextAnalysisLocation:
        return self.word.end_location

    @property
    def configuration(self) -> SentenceConfiguration:
        return self.variant.configuration

    @property
    def previous_location(self) -> TextAnalysisLocation | None:
        return self.word.start_location.previous() if self.word.start_location.previous else None

    @property
    def prefix(self) -> str:
        return self.previous_location.token.surface if self.previous_location else ""

    @property
    def next_location(self) -> TextAnalysisLocation | None:
        return self.word.end_location.next() if self.word.end_location.next else None

    @property
    def suffix(self) -> str:
        return self.next_location.token.surface if self.next_location else ""

    @property
    def tokenized_form(self) -> str:
        return self.match.tokenized_form

    @property
    def parsed_form(self) -> str:
        return self.match.parsed_form

    @property
    def has_godan_imperative_part(self) -> bool:
        return self.word.start_location.token.is_godan_imperative_inflection or self.word.start_location.token.is_godan_imperative_stem

    @property
    def has_godan_potential_start(self) -> bool:
        return self.word.start_location.token.is_godan_potential_inflection or self.word.start_location.token.is_godan_potential_stem

    @property
    def is_ichidan_covering_godan_potential(self) -> bool:
        return self.word.location_count == 2 and self.has_godan_potential_start and self.has_godan_potential_ending


    @property
    def has_godan_potential_ending(self) -> bool:
        return self.word.end_location.token.is_godan_potential_inflection

    @property
    def has_godan_ichidan_imperative_part(self) -> bool:
        return self.word.start_location.token.is_ichidan_imperative_stem or self.word.start_location.token.is_ichidan_imperative_inflection

    @property
    def is_end_of_statement(self) -> bool:
        if len(self.suffix) == 0:
            return True

        if self.suffix[0].isspace():
            return True

        if self.suffix in analysis_constants.sentence_end_characters:  # noqa: SIM103
            return True

        return False
