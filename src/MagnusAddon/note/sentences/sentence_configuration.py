from __future__ import annotations

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.sentences.parsing_result import ParsingResult
from sysutils import ex_json


class SentenceConfiguration:
    def __init__(self, highlighted_words: list[str], incorrect_matches: list[WordExclusion], parsing_result: ParsingResult) -> None:
        self.highlighted_words: list[str] = highlighted_words
        self.incorrect_matches: set[WordExclusion] = set(incorrect_matches)
        self.parsing_result: ParsingResult = parsing_result

    def to_json(self) -> str:
        return ex_json.dict_to_json({'highlighted_words': self.highlighted_words,
                                     'incorrect_matches': [exclusion.to_dict() for exclusion in self.incorrect_matches],
                                     'parsing_result': self.parsing_result.to_dict()})

    @classmethod
    def from_json(cls, json: str) -> SentenceConfiguration:
        # try:
        reader = ex_json.json_to_dict(json) if json else None
        highlighted_words: list[str] = reader.get_string_list('highlighted_words') if reader else []
        incorrect_matches: list[WordExclusion] = \
            [WordExclusion.from_dict(exclusion_data)
             for exclusion_data in reader.get_object_list('incorrect_matches')] if reader else []

        parsing_json_dict = reader.get_object_or_none('parsing_result') if reader else None
        parsing_result: ParsingResult = ParsingResult.from_json(parsing_json_dict) if parsing_json_dict else ParsingResult.empty()

        return cls(highlighted_words, incorrect_matches, parsing_result)
        # except: #todo: remove this ugly hack
        #     return SentenceConfiguration([], [], ParsingResult.empty())

    def incorrect_matches_words(self) -> set[str]:
        return {exclusion.word for exclusion in self.incorrect_matches}
