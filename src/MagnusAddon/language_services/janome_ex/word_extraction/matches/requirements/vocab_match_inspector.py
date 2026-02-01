from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

if TYPE_CHECKING:
    from jaslib.note.vocabulary.vocabnote_matching_rules import VocabMatchingRulesConfigurationRequiresForbidsFlags
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef

class VocabMatchInspector(MatchInspector, Slots):
    """Base class providing access to VocabMatch context and helper properties.

    This class holds a weak reference to a VocabMatch and provides convenient
    properties for inspecting the match's word, variant, location, and surrounding context.
    """

    def __init__(self, match: WeakRef[VocabMatch]) -> None:
        super().__init__(match)
        self._requires_forbids: VocabMatchingRulesConfigurationRequiresForbidsFlags | None = None

    @property
    @override
    def match(self) -> VocabMatch:
        return cast("VocabMatch", self._match())

    @property
    def requires_forbids(self) -> VocabMatchingRulesConfigurationRequiresForbidsFlags:
        if self._requires_forbids is None:
            self._requires_forbids = self.match.requires_forbids
        return self._requires_forbids

    @property
    def previous_location_is_irrealis(self) -> bool:
        return self.previous_location is not None and self.previous_location.token.is_irrealis

    @property
    def previous_location_is_godan(self) -> bool:
        return self.previous_location is not None and self.previous_location.token.is_godan_verb

    @property
    def previous_location_is_ichidan(self) -> bool:
        return self.previous_location is not None and self.previous_location.token.is_ichidan_verb

    @property
    def base_equals_surface(self) -> bool:
        word = self.word
        return word.surface_form == word.base_form
