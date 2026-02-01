from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.language_services.janome_ex.word_extraction.matches.state_tests.head.failed_match_requirement import FailedMatchRequirement

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb(Slots):
    _failed: FailedMatchRequirement = FailedMatchRequirement.forbids("inflected_surface_with_valid_base")

    _prefixes_that_indicates_verb_if_followed_by_end_of_statement: set[str] = {"を", "が"}
    @classmethod
    def apply_to(cls, inspector: MatchInspector) -> FailedMatchRequirement | None:
        if (inspector.variant.is_surface
                and inspector.word.has_base_variant_with_valid_match
                and (inspector.word.is_inflected_word or (inspector.prefix and inspector.prefix[-1] in cls._prefixes_that_indicates_verb_if_followed_by_end_of_statement and inspector.is_end_of_statement))):
            return ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb._failed
        return None
