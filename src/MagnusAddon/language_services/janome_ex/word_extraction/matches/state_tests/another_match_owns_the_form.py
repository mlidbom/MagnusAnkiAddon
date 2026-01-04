from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsAnotherMatchOwnsTheForm(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("another_match_owns_the_form")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> MatchRequirement | None:
        if cls._internal_is_in_state(inspector):
            return cls._failed
        return None

    @staticmethod
    def _internal_is_in_state(inspector: VocabMatchInspector) -> bool:
        if inspector.match.vocab.forms.is_owned_form(inspector.tokenized_form):
            return False

        if any(other_match for other_match in inspector.variant.vocab_matches  # noqa: SIM103
               if other_match != inspector.match
                  and other_match.vocab.forms.is_owned_form(inspector.tokenized_form)
                  and other_match.is_valid):
            return True
        return False
