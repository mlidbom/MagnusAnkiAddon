from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef
    from typed_linq_collections.collections.q_set import QSet

class SuffixIsIn(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match], suffixes: QSet[str]) -> None:
        super().__init__(match, f"""suffix_in:{",".join(suffixes)}""", cache_is_in_state=True)
        self.suffixes: QSet[str] = suffixes

    @override
    def _internal_match_is_in_state(self) -> bool:
        if any(suffix for suffix in self.suffixes if self.suffix.startswith(suffix)):  # noqa: SIM103
            return True

        return False
