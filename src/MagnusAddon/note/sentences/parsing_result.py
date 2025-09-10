from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.sentences.parsed_word import ParsedWord
from note.sentences.serialization.parsing_result_serializer import ParsingResultSerializer

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

class ParsingResult(Slots):
    serializer: ParsingResultSerializer = ParsingResultSerializer()
    def __init__(self, words: list[ParsedWord], sentence: str, parser_version: str) -> None:
        self.parsed_words = words
        self.sentence = sentence
        self.parser_version = parser_version

    def parsed_words_strings(self) -> list[str]: return [parsed.word for parsed in self.parsed_words]

    def detected_vocab(self) -> set[int]: return {parsed.vocab_id for parsed in self.parsed_words if parsed.vocab_id != -1}

    @classmethod
    def from_analysis(cls, analysis: TextAnalysis) -> ParsingResult:
        return ParsingResult([ParsedWord.from_match(match) for match in analysis.valid_word_variant_valid_matches],
                             analysis.text,
                             analysis.version)
