from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from typed_linq_collections.q_iterable import query

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
    def surface_variant(self) -> CandidateWordVariant:
        return self.word.surface_variant

    @property
    def is_base(self) -> bool: return not self.variant.is_surface

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
        return self.start_location.previous() if self.start_location.previous else None

    @property
    def has_te_form_stem(self) -> bool:
        return self.start_location.token.has_te_form_stem

    @property
    def has_te_form_prefix(self) -> bool:
        previous_location = self.previous_location
        return previous_location is not None and previous_location.token.has_te_form_stem

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
        return self.start_location.token.is_godan_imperative_inflection or self.start_location.token.is_godan_imperative_stem

    @property
    def has_godan_potential_start(self) -> bool:
        return self.start_location.token.is_godan_potential_inflection or self.start_location.token.is_godan_potential_stem

    @property
    def is_verb_dictionary_form_compound(self) -> bool:
        return self.word.location_count == 2 and self.start_location.token.is_dictionary_verb_form_stem and self.end_location.token.is_dictionary_verb_inflection

    @property
    def is_ichidan_covering_godan_potential(self) -> bool:
        return self.word.location_count == 2 and self.has_godan_potential_start and self.has_godan_potential_ending

    @property
    def has_godan_potential_ending(self) -> bool:
        return self.word.end_location.token.is_godan_potential_inflection

    @property
    def compound_locations_all_have_valid_non_compound_matches(self) -> bool:
        return (query(self.word.locations)
                .select(lambda it: it())
                .all(lambda it: it.non_compound_candidate.has_valid_words()))

    @property
    def has_masu_stem(self) -> bool:
        return self.start_location.previous is not None and self.start_location.previous().token.is_masu_stem

    @property
    def has_preceding_adverb(self) -> bool:
        return self.start_location.previous is not None and self.start_location.previous().token.is_adverb

    @property
    def is_end_of_statement(self) -> bool:
        return self.end_location.token.is_end_of_statement
