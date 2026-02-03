from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots

from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from collections.abc import Callable

    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class Forbids(Slots):
    def __init__(self, name: str, is_in_state: Callable[[MatchInspector], bool]) -> None:
        self._is_in_state: Callable[[MatchInspector], bool] = is_in_state
        self._required_failure: FailedMatchRequirement = FailedMatchRequirement.forbids(name)

    def apply_to(self, inspector: MatchInspector) -> FailedMatchRequirement | None:
        if self._is_in_state(inspector):
            return self._required_failure
        return None
