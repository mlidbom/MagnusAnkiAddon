from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsIsPoisonWord(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("poison_word")

    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        if inspector.match.vocab.matching_configuration.bool_flags.is_poison_word.is_set():
            return cls._failed
        return None

