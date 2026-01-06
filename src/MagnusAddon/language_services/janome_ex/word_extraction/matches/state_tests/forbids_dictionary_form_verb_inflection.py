from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector
    from language_services.janome_ex.word_extraction.matches.requirements.requirement import MatchRequirement

class ForbidsDictionaryInflectionSurfaceWithBase(Slots):
    _failed: MatchRequirement = FailedMatchRequirement.forbids("dictionary_form_verb_inflection")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> MatchRequirement | None:
        if inspector.variant.is_surface and not inspector.word.is_compound and inspector.word.base_variant is not None and inspector.word.end_location.token.is_dictionary_verb_inflection:
            return cls._failed
        return None
