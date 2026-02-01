from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from jastudio.note.sentences.parsed_match import ParsedMatch
from jastudio.note.sentences.serialization.parsing_result_serializer import ParsingResultSerializer
from jastudio.sysutils import ex_str
from jastudio.sysutils.memory_usage import string_auto_interner
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.collections.q_set import QSet
from typed_linq_collections.collections.q_unique_list import QUniqueList

if TYPE_CHECKING:
    from jastudio.language_services.janome_ex.word_extraction.text_analysis import TextAnalysis

class ParsingResult(Slots):
    serializer: ParsingResultSerializer = ParsingResultSerializer()
    def __init__(self, words: list[ParsedMatch], sentence: str, parser_version: str) -> None:
        self.parsed_words: QList[ParsedMatch] = QList(words)
        self.sentence: str = string_auto_interner.auto_intern(sentence.replace(ex_str.invisible_space, ""))
        self.parser_version: str = string_auto_interner.auto_intern(parser_version)

    @property
    def matched_vocab_ids(self) -> QSet[int]: return QSet(parsed.vocab_id for parsed in self.parsed_words if parsed.vocab_id != -1)


    def parsed_words_strings(self) -> QUniqueList[str]: return QUniqueList(parsed.parsed_form for parsed in self.parsed_words)

    @classmethod
    def from_analysis(cls, analysis: TextAnalysis) -> ParsingResult:
        return ParsingResult([ParsedMatch.from_match(match) for match in analysis.valid_matches],
                             analysis.text,
                             analysis.version)
