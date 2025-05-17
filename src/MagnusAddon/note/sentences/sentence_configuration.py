from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.sentences.serialization.sentence_configuration_serializer import SentenceConfigurationSerializer
from note.sentences.word_exclusion_set import WordExclusionSet

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

class SentenceConfiguration(Slots):
    serializer: SentenceConfigurationSerializer = SentenceConfigurationSerializer()
    def __init__(self, highlighted_words: list[str], incorrect_matches: WordExclusionSet, hidden_matches: WordExclusionSet) -> None:
        self.highlighted_words: list[str] = highlighted_words
        self.incorrect_matches: WordExclusionSet = incorrect_matches
        self.hidden_matches: WordExclusionSet = hidden_matches

    @classmethod
    def from_incorrect_matches(cls, incorrect_matches: list[WordExclusion]) -> SentenceConfiguration:
        return cls.from_lists([], incorrect_matches, [])

    @classmethod
    def from_lists(cls, highlighted: list[str], incorrect_matches: list[WordExclusion], hidden_matches: list[WordExclusion]) -> SentenceConfiguration:
        return cls(highlighted,
                   WordExclusionSet(lambda: None, incorrect_matches),
                   WordExclusionSet(lambda: None, hidden_matches))

    @classmethod
    def empty(cls) -> SentenceConfiguration: return cls.from_lists([], [], [])
