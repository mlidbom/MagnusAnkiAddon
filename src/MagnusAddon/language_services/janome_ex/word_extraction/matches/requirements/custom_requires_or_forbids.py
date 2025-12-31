from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
    from language_services.janome_ex.word_extraction.candidate_word_variant import CandidateWordVariant
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from language_services.janome_ex.word_extraction.text_location import TextAnalysisLocation
    from note.sentences.sentence_configuration import SentenceConfiguration
    from sysutils.weak_ref import WeakRef


class CustomRequiresOrForbids(MatchRequirement, Slots):
    """Base class for fused RequiresOrForbids + MatchStateTest implementations.
    
    Eliminates the double-wrapping overhead by combining both responsibilities.
    Subclasses must implement: is_required, is_forbidden, and is_in_state.
    """
    
    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        # Don't call super().__init__() since we don't have a state_test
        self._match: WeakRef[VocabMatch] = match
        self._cached_state: bool | None = None

    @property
    def is_required(self) -> bool:
        """Whether this state is required."""
        raise NotImplementedError()

    @property
    def is_forbidden(self) -> bool:
        """Whether this state is forbidden."""
        raise NotImplementedError()

    @property
    def is_in_state(self) -> bool:
        """Whether the match is currently in this state."""
        if self._cached_state is not None:
            return self._cached_state
        
        self._cached_state = self._internal_is_in_state()
        return self._cached_state

    @property
    def description(self) -> str:
        """Description of this state for error messages."""
        raise NotImplementedError()

    @property
    @override
    def is_fulfilled(self) -> bool:
        if self.is_required and not self.is_in_state:
            return False

        return not (self.is_forbidden and self.is_in_state)

    @property
    @override
    def failure_reason(self) -> str:
        if self.is_fulfilled:
            return ""

        if self.is_required:
            return f"required::{self.description}"

        if self.is_forbidden:
            return f"forbids::{self.description}"

        raise AssertionError("This should never happen")

    def _internal_is_in_state(self) -> bool:
        """Internal implementation of state checking. Override this in subclasses."""
        raise NotImplementedError()

    # Convenience properties for accessing match context
    @property
    def match(self) -> VocabMatch:
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
