from __future__ import annotations

from typing import TYPE_CHECKING

from note.sentences.serialization.sentence_configuration_serializer import SentenceConfigurationSerializer

if TYPE_CHECKING:
    from note.sentences.word_exclusion_set import WordExclusionSet

class SentenceConfiguration:
    serializer:SentenceConfigurationSerializer = SentenceConfigurationSerializer()
    def __init__(self, highlighted_words: list[str], incorrect_matches: WordExclusionSet, hidden_matches: WordExclusionSet) -> None:
        self.highlighted_words: list[str] = highlighted_words
        self.incorrect_matches: WordExclusionSet = incorrect_matches
        self.hidden_matches: WordExclusionSet = hidden_matches
