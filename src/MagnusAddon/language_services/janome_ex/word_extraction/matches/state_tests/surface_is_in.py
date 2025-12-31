from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from sysutils.weak_ref import WeakRef
    from typed_linq_collections.collections.q_set import QSet

class ForbidsSurfaceIsIn(CustomForbids, Slots):
    def __init__(self, match: WeakRef[VocabMatch], surfaces: QSet[str], is_requirement_active: bool = True) -> None:
        super().__init__(match, is_requirement_active)
        self.surfaces: QSet[str] = surfaces

    @property
    @override
    def description(self) -> str: return f"""surface_in:{",".join(self.surfaces)}"""

    @override
    def _internal_is_in_state(self) -> bool:
        if self.word.surface_variant.form in self.surfaces:  # noqa: SIM103
            return True
        return False
