from __future__ import annotations
import json
from typing import Dict, Any, List, Optional

from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion

class SentenceConfiguration:
    def __init__(self, highlighted_words: List[str], word_exclusions: List[WordExclusion]):
        self.highlighted_words = highlighted_words or []
        self.word_exclusions = word_exclusions or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            'highlighted_words': self.highlighted_words,
            'word_exclusions': [exclusion.to_dict() for exclusion in self.word_exclusions]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SentenceConfiguration:
        highlighted_words = data.get('highlighted_words', [])
        exclusions_data = data.get('word_exclusions', [])
        word_exclusions = [WordExclusion.from_dict(exclusion_data) for exclusion_data in exclusions_data]

        return cls(highlighted_words=highlighted_words, word_exclusions=word_exclusions)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> SentenceConfiguration:
        data = json.loads(json_str)
        return cls.from_dict(data)