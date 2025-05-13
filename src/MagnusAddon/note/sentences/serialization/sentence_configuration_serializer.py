from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.sentences.parsing_result import ParsingResult
from sysutils import ex_json

if TYPE_CHECKING:
    from note.sentences.sentence_configuration import SentenceConfiguration

class SentenceConfigurationSerializer:
    @staticmethod
    def deserialize(json: str) -> SentenceConfiguration:
        from note.sentences.sentence_configuration import SentenceConfiguration
        reader = ex_json.json_to_dict(json) if json else None
        highlighted_words: list[str] = reader.get_string_list('highlighted_words') if reader else []
        incorrect_matches: list[WordExclusion] = \
            [WordExclusion.from_dict(exclusion_data)
             for exclusion_data in reader.get_object_list('incorrect_matches')] if reader else []

        parsing_json_dict = reader.get_object_or_none('parsing_result') if reader else None
        parsing_result: ParsingResult = ParsingResult.serializer.from_reader(parsing_json_dict) if parsing_json_dict else ParsingResult.empty()

        return SentenceConfiguration(highlighted_words, incorrect_matches, parsing_result)

    @staticmethod
    def serialize(config: SentenceConfiguration) -> str:
        return ex_json.dict_to_json({'highlighted_words': config.highlighted_words,
                                     'incorrect_matches': [exclusion.to_dict() for exclusion in config.incorrect_matches],
                                     'parsing_result': ParsingResult.serializer.to_dict(config.parsing_result)})
