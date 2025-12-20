from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from note.vocabulary.vocabnote import VocabNote
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration
    from sysutils.weak_ref import WeakRef


class VocabMatchStateTest(MatchStateTest, Slots):
    def __init__(self, match: WeakRef[VocabMatch], name: str, cache_is_in_state: bool) -> None:
        super().__init__(match, name, cache_is_in_state)
        self.name: str = name

    @property
    @override
    def match(self) -> VocabMatch:
        from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch  # pyright: ignore[reportUnusedImport]
        return cast(VocabMatch, super().match)

    @property
    def rules(self) -> VocabNoteMatchingConfiguration: return self.match.vocab.matching_configuration

    @property
    def vocab(self) -> VocabNote: return self.match.vocab
