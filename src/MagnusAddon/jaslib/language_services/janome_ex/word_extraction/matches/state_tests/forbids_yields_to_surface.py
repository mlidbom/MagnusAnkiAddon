from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector

class ForbidsYieldsToValidSurfaceSurface(Slots):
    @classmethod
    def apply_to(cls, inspector: VocabMatchInspector) -> FailedMatchRequirement | None:
        surfaces = inspector.match.rules.yield_to_surface.get()
        surface_variant = inspector.surface_variant
        if surface_variant.has_valid_match and surface_variant.form in surfaces:
            return FailedMatchRequirement.forbids(f"""valid_surface_in:{",".join(surfaces)}""")

        return None