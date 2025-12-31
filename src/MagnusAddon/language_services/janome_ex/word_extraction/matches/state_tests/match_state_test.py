from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.sentences.sentence_configuration import SentenceConfiguration

class MatchStateTest(Slots):
    def __init__(self, inspector: MatchInspector) -> None:
        self.inspector: MatchInspector = inspector
        self._cached_state: bool | None = None

    @property
    def match_is_in_state(self) -> bool:  # Profiling: don't use a lazy because this class is intantiated in very tight loops and the overhead of the required WeakRef and Lazy together becomes quite significant
        if self._cached_state is not None:
            return self._cached_state

        self._cached_state = self._internal_match_is_in_state()
        return self._cached_state

    @property
    def description(self) -> str: raise NotImplementedError()

    @property
    def has_godan_imperative_part(self) -> bool: return self.inspector.word.start_location.token.is_godan_imperative_inflection or self.inspector.word.start_location.token.is_godan_imperative_stem

    @property
    def has_godan_potential_part(self) -> bool: return self.inspector.word.start_location.token.is_godan_potential_inflection or self.inspector.word.start_location.token.is_godan_potential_stem

    @property
    def has_godan_ichidan_imperative_part(self) -> bool: return self.inspector.word.start_location.token.is_ichidan_imperative_stem or self.inspector.word.start_location.token.is_ichidan_imperative_inflection

    @property
    def state_description(self) -> str: return self.description
    @property
    def tokenized_form(self) -> str: return self.inspector.match.tokenized_form
    @property
    def parsed_form(self) -> str: return self.inspector.match.parsed_form
    @property
    def variant(self) -> CandidateWordVariant: return self.inspector.match.variant
    @property
    def word(self) -> CandidateWord: return self.inspector.variant.word
    @property
    def start_location(self) -> TextAnalysisLocation: return self.inspector.word.start_location
    @property
    def end_location(self) -> TextAnalysisLocation: return self.inspector.word.end_location
    @property
    def configuration(self) -> SentenceConfiguration: return self.inspector.variant.configuration
    @property
    def previous_location(self) -> TextAnalysisLocation | None: return self.inspector.word.start_location.previous() if self.inspector.word.start_location.previous else None
    @property
    def prefix(self) -> str: return self.inspector.previous_location.token.surface if self.inspector.previous_location else ""
    @property
    def next_location(self) -> TextAnalysisLocation | None: return self.inspector.word.end_location.next() if self.inspector.word.end_location.next else None
    @property
    def suffix(self) -> str: return self.inspector.next_location.token.surface if self.inspector.next_location else ""

    def _internal_match_is_in_state(self) -> bool: raise NotImplementedError()

    @override
    def __repr__(self) -> str: return self.state_description
