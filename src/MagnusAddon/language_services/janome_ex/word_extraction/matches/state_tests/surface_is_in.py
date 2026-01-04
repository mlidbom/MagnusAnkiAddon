from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from typed_linq_collections.collections.q_set import QSet

class ForbidsSurfaceIsIn(CustomForbids, Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector, surfaces: QSet[str]) -> MatchRequirement | None:
        if inspector.word.surface_variant.form in surfaces:
            return FailedMatchRequirement.forbids(f"""surface_in:{",".join(surfaces)}""")

        return None