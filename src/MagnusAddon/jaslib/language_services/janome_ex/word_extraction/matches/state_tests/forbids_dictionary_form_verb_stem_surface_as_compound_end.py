from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsDictionaryVerbFormStemAsCompoundEnd(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("dictionary_form_verb_stem_as_compound_end")

    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> FailedMatchRequirement | None:
        if inspector.variant.is_surface and inspector.word.base_variant is not None and inspector.word.end_location.token.is_dictionary_verb_form_stem:
            return cls._failed
        return None
