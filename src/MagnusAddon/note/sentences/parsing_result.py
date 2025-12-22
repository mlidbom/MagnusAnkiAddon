from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.sentences.parsed_match import ParsedMatch
from note.sentences.serialization.parsing_result_serializer import ParsingResultSerializer
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

class ParsingResult(Slots):
    serializer: ParsingResultSerializer = ParsingResultSerializer()
    def __init__(self, words: list[ParsedMatch], sentence: str, parser_version: str) -> None:
        self.parsed_words: list[ParsedMatch] = words
        self.sentence: str = sentence
        self.parser_version: str = parser_version
        self.matched_vocab_ids: QSet[int] = QSet(parsed.vocab_id for parsed in self.parsed_words if parsed.vocab_id != -1)

    def parsed_words_strings(self) -> QList[str]: return QList(parsed.parsed_form for parsed in self.parsed_words)

    @classmethod
    def from_analysis(cls, analysis: TextAnalysis) -> ParsingResult:
        return ParsingResult([ParsedMatch.from_match(match) for match in analysis.valid_word_variant_valid_matches],
                             analysis.text,
                             analysis.version)
