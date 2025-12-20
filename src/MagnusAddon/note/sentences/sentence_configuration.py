from __future__ import annotations

from typing import TYPE_CHECKING, override

from manually_copied_in_libraries.autoslot import Slots
from note.sentences.serialization.sentence_configuration_serializer import SentenceConfigurationSerializer
from note.sentences.word_exclusion_set import WordExclusionSet
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

class SentenceConfiguration(Slots):
    serializer: SentenceConfigurationSerializer = SentenceConfigurationSerializer()

    def __init__(self, highlighted_words: set[str], incorrect_matches: WordExclusionSet, hidden_matches: WordExclusionSet) -> None:
        self.highlighted_words: set[str] = highlighted_words
        self.incorrect_matches: WordExclusionSet = incorrect_matches
        self.hidden_matches: WordExclusionSet = hidden_matches

    @classmethod
    def from_incorrect_matches(cls, incorrect_matches: list[WordExclusion]) -> SentenceConfiguration:
        return cls.from_values(set(), incorrect_matches, [])

    @classmethod
    def from_hidden_matches(cls, incorrect_matches: list[WordExclusion]) -> SentenceConfiguration:
        return cls.from_values(set(), [], incorrect_matches)

    @classmethod
    def from_values(cls, highlighted: set[str], incorrect_matches: list[WordExclusion], hidden_matches: list[WordExclusion]) -> SentenceConfiguration:
        return cls(highlighted,
                   WordExclusionSet(lambda: None, incorrect_matches),
                   WordExclusionSet(lambda: None, hidden_matches))

    @classmethod
    def empty(cls) -> SentenceConfiguration: return cls.from_values(set(), [], [])

    @override
    def __repr__(self) -> str: return (SkipFalsyValuesDebugReprBuilder()
                                       .prop("highlighted_words", self.highlighted_words)
                                       .prop("incorrect_matches", self.incorrect_matches)
                                       .prop("hidden_matches", self.hidden_matches)
                                       .repr)
