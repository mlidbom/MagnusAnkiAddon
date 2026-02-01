from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsDictionaryInflectionSurfaceWithBase(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("dictionary_form_verb_inflection")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> FailedMatchRequirement | None:
        if inspector.variant.is_surface and not inspector.word.is_compound and inspector.word.base_variant is not None and inspector.word.end_location.token.is_dictionary_verb_inflection:
            return cls._failed
        return None
