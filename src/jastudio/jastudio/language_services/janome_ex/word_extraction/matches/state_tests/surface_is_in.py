from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsSurfaceIsIn(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        surfaces = inspector.match.rules.surface_is_not.get()
        if inspector.word.surface_variant.form in surfaces:
            return FailedMatchRequirement.forbids(f"""surface_in:{",".join(surfaces)}""")

        return None