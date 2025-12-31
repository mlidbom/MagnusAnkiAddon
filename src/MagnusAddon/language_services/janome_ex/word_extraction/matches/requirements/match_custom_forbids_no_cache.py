from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class MatchCustomForbidsNoCache(MatchRequirement, Slots):
    """Base class for fused Forbids + MatchStateTest implementations that cannot cache state.

    Used for display_requirements that must evaluate state freshly each time (like IsShadowed).
    Uses composition with MatchInspector for match context.
    Subclasses must implement: _internal_is_in_state and description.
    """

    def __init__(self, inspector: MatchInspector, is_requirement_active: bool = True) -> None:
        self.inspector: MatchInspector = inspector
        self.is_requirement_active: bool = is_requirement_active

    @property
    def is_in_state(self) -> bool:
        """Whether the match is currently in this state. NOT cached!"""
        return self._internal_is_in_state()

    @property
    def description(self) -> str:
        """Description of this state for error messages."""
        raise NotImplementedError()

    @property
    @override
    def is_fulfilled(self) -> bool:
        if not self.is_requirement_active:
            return True

        return not self.is_in_state

    @property
    @override
    def failure_reason(self) -> str:
        return f"""forbids::{self.description}""" if not self.is_fulfilled else ""

    def _internal_is_in_state(self) -> bool:
        """Internal implementation of state checking. Override this in subclasses."""
        raise NotImplementedError()
