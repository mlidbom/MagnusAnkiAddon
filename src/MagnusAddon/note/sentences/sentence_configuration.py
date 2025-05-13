from __future__ import annotations

from typing import TYPE_CHECKING

from note.sentences.serialization.sentence_configuration_serializer import SentenceConfigurationSerializer

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
    from note.sentences.parsing_result import ParsingResult

class SentenceConfiguration:
    serializer:SentenceConfigurationSerializer = SentenceConfigurationSerializer()
    def __init__(self, highlighted_words: list[str], incorrect_matches: list[WordExclusion], parsing_result: ParsingResult) -> None:
        self.highlighted_words: list[str] = highlighted_words
        self.incorrect_matches: set[WordExclusion] = set(incorrect_matches)
        self.parsing_result: ParsingResult = parsing_result

    def incorrect_matches_words(self) -> set[str]:
        return {exclusion.word for exclusion in self.incorrect_matches}
