from __future__ import annotations

from typing import cast, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch


class VocabMatchStateTest(MatchStateTest):
    def __init__(self, match: VocabMatch, name: str) -> None:
        super().__init__(match, name)
        self.name: str = name

    @property
    @override
    def match(self) -> VocabMatch: return cast(VocabMatch, super().match)
