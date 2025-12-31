from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector


class CustomRequiresOrForbids(MatchRequirement, Slots):
    """Base class for fused RequiresOrForbids + MatchStateTest implementations.
    
    Uses composition with a shared VocabMatchInspector for memory efficiency.
    Subclasses must implement: is_required, is_forbidden, and _internal_is_in_state.
    """
    
    def __init__(self, inspector: VocabMatchInspector) -> None:
        # Don't call super().__init__() since we don't have a state_test
        self.inspector: VocabMatchInspector = inspector
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

    # Delegate to inspector for convenience
    @property
    def match(self):
        return self.inspector.match

    @property
    def variant(self):
        return self.inspector.variant

    @property
    def word(self):
        return self.inspector.word

    @property
    def start_location(self):
        return self.inspector.start_location

    @property
    def end_location(self):
        return self.inspector.end_location

    @property
    def configuration(self):
        return self.inspector.configuration

    @property
    def previous_location(self):
        return self.inspector.previous_location

    @property
    def prefix(self):
        return self.inspector.prefix

    @property
    def next_location(self):
        return self.inspector.next_location

    @property
    def suffix(self):
        return self.inspector.suffix

    @property
    def tokenized_form(self):
        return self.inspector.tokenized_form

    @property
    def parsed_form(self):
        return self.inspector.parsed_form
