from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class RequiresOrForbidsPrecedingAdverb(Slots):
    _required_reason: FailedMatchRequirement = FailedMatchRequirement.required("preceding-adverb")
    _forbidden_reason: FailedMatchRequirement = FailedMatchRequirement.forbids("preceding-adverb")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        if inspector.requires_forbids.preceding_adverb.is_required and not inspector.has_preceding_adverb:
            return cls._required_reason
        if inspector.requires_forbids.preceding_adverb.is_forbidden and inspector.has_preceding_adverb:
            return cls._forbidden_reason
        return None
