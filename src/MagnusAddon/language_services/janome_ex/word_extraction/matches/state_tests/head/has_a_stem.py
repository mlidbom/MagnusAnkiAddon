from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots
from language_services import conjugator
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class HasAStem(MatchStateTest, ProfilableAutoSlots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "a_stem", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if len(self.prefix) > 0 and self.prefix[-1] in conjugator.a_stem_characters:  # noqa: SIM103
            return True

        return False
