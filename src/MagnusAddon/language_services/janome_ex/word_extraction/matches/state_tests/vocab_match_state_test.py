from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from language_services.janome_ex.word_extraction.matches.state_tests.match_state_test import MatchStateTest
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.matches.vocab_match import VocabMatch
    from note.vocabulary.vocabnote_matching_rules import VocabNoteMatchingConfiguration


class VocabMatchStateTest(MatchStateTest):
    def __init__(self, match: VocabMatch, name: str) -> None:
        super().__init__(match, name)
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
