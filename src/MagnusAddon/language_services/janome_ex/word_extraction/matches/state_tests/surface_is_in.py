from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.custom_forbids import CustomForbids

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.vocab_match_inspector import VocabMatchInspector
    from typed_linq_collections.collections.q_set import QSet

class ForbidsSurfaceIsIn(CustomForbids, Slots):
    def __init__(self, inspector: VocabMatchInspector, surfaces: QSet[str]) -> None:
        super().__init__(inspector)
        self.surfaces: QSet[str] = surfaces

    @staticmethod
    def for_if(inspector: VocabMatchInspector, surfaces: QSet[str]) -> ForbidsSurfaceIsIn | None:
        return ForbidsSurfaceIsIn(inspector, surfaces) if surfaces else None

    @property
    @override
    def description(self) -> str: return f"""surface_in:{",".join(self.surfaces)}"""

    @override
    def _internal_is_in_state(self) -> bool:
        if self.inspector.word.surface_variant.form in self.surfaces:  # noqa: SIM103
            return True
        return False
