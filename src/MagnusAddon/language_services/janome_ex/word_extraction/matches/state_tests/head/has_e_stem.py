from __future__ import annotations

from typing import TYPE_CHECKING, override

from language_services import conjugator
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from manually_copied_in_libraries.autoslot import Slots
from sysutils import kana_utils

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.match import Match
    from sysutils.weak_ref import WeakRef

class HasEStem(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[Match]) -> None:
        super().__init__(match, "e_stem", cache_is_in_state=True)

    @override
    def _internal_match_is_in_state(self) -> bool:
        if not self.prefix:
            return False

        if self.prefix[-1] in conjugator.e_stem_characters:
            return True

        if kana_utils.character_is_kanji(self.prefix[-1]):  # noqa: SIM103
            return True
        return False
