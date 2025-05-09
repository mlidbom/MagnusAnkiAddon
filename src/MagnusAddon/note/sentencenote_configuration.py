from __future__ import annotations
from sysutils import ex_json
from typing import Any

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

class SentenceConfiguration:
    def __init__(self, highlighted_words: list[str], word_exclusions: list[WordExclusion]):
        self.highlighted_words = highlighted_words or []
        self.incorrect_matches = word_exclusions or []

    def to_dict(self) -> dict[str, Any]:
        return {
            'highlighted_words': self.highlighted_words,
            'incorrect_matches': [exclusion.to_dict() for exclusion in self.incorrect_matches]
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SentenceConfiguration:
        highlighted_words = data['highlighted_words']
        exclusions_data = data['incorrect_matches']
        word_exclusions = [WordExclusion.from_dict(exclusion_data) for exclusion_data in exclusions_data]

        return cls(highlighted_words=highlighted_words, word_exclusions=word_exclusions)

    def to_json(self) -> str:
        return ex_json.dict_to_json(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SentenceConfiguration:
        return cls.from_dict(ex_json.json_to_dict(json_str)) if json_str.strip() else cls([], [])
