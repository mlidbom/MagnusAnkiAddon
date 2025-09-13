from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class PrefixIsIn(MatchStateTest):
    def __init__(self, match: WeakRef[Match], prefixes: set[str]) -> None:
        super().__init__(match, f"""prefix_in:{",".join(prefixes)}""", cache_is_in_state=True)
        self.prefixes: set[str] = prefixes

    @override
    def _internal_match_is_in_state(self) -> bool:
        if any(prefix for prefix in self.prefixes if self.prefix.endswith(prefix)):  # noqa: SIM103
            return True
        return False
