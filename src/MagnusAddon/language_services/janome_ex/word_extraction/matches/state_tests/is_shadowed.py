from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.requirements.match_custom_forbids_no_cache import MatchCustomForbidsNoCache

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.requirements.match_inspector import MatchInspector

class ForbidsIsShadowed(MatchCustomForbidsNoCache, Slots):
    def __init__(self, inspector: MatchInspector) -> None:
        super().__init__(inspector)

    @property
    @override
    def description(self) -> str: return f"shadowed_by:{self.inspector.match.word.shadowed_by_text}"

    @override
    def _internal_is_in_state(self) -> bool: return self.inspector.match.is_shadowed
