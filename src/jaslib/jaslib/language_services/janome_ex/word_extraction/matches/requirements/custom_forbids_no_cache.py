from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from jaslib.language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
from jaslib.sysutils.abstract_method_called_error import AbstractMethodCalledError

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector


class CustomForbidsNoCache(MatchRequirement, Slots):
    """Base class for fused Forbids + MatchStateTest implementations that cannot cache state.

    Used for display_requirements that must evaluate state freshly each time.
    Uses composition with VocabMatchInspector for match context.
    Subclasses must implement: _internal_is_in_state.
    """

    def __init__(self, inspector: VocabMatchInspector) -> None:
        self.inspector: VocabMatchInspector = inspector

    @property
    def is_in_state(self) -> bool:
        """Whether the match is currently in this state. NOT cached!"""
        return self._internal_is_in_state()

    @property
    def description(self) -> str:
        """Description of this state for error messages."""
        raise AbstractMethodCalledError()

    @property
    @override
    def is_fulfilled(self) -> bool:
        return not self.is_in_state

    @property
    @override
    def failure_reason(self) -> str:
        return f"""forbids::{self.description}""" if not self.is_fulfilled else ""

    def _internal_is_in_state(self) -> bool:
        """Internal implementation of state checking. Override this in subclasses."""
        raise AbstractMethodCalledError()
