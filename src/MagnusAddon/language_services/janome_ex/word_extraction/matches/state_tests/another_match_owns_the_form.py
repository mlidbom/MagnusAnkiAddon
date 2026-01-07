from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsAnotherMatchOwnsTheForm(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("another_match_owns_the_form")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        if inspector.match.another_match_is_higher_priority:
            return cls._failed
        return None
