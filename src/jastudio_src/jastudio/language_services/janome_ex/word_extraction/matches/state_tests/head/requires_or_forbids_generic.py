from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from collections.abc import Callable

    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from jastudio.note.notefields.require_forbid_flag_field import RequireForbidFlagField

class RequiresOrForbids(Slots):
    def __init__(self, name: str,
                 get_requirement: Callable[[VocabMatchInspector], RequireForbidFlagField],
                 is_in_state: Callable[[VocabMatchInspector], bool]) -> None:
        self._get_requirement: Callable[[VocabMatchInspector], RequireForbidFlagField] = get_requirement
        self._is_in_state: Callable[[VocabMatchInspector], bool] = is_in_state
        self._required_failure: FailedMatchRequirement = FailedMatchRequirement.required(name)
        self._forbidden_failure: FailedMatchRequirement = FailedMatchRequirement.forbids(name)

    def apply_to(self, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        requirement = self._get_requirement(inspector)

        if requirement.is_required and not self._is_in_state(inspector):
            return self._required_failure
        if requirement.is_forbidden and self._is_in_state(inspector):
            return self._forbidden_failure
        return None
