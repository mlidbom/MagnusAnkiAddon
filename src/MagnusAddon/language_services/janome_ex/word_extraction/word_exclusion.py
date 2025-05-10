from __future__ import annotations
from typing import TYPE_CHECKING

from sysutils.ex_json import JsonDictReader

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.hierarchicalword import HierarchicalWord

from typing import Any

class WordExclusion:
    _separator = "####"
    _no_index = -1
    def __init__(self, word: str, index: int = _no_index) -> None:
        self.word = word
        self.index = index

    def excludes(self, word: HierarchicalWord) -> bool:
        return word.word.word == self.word and (self.index == WordExclusion._no_index or self.index == word.word.character_index)

    def excludes_form_at_index(self, form: str, index: int) -> bool:
        return form == self.word and (self.index == WordExclusion._no_index or self.index == index)

    @classmethod
    def from_string(cls, exclusion: str) -> WordExclusion:
        if cls._separator in exclusion:
            parts = exclusion.split(cls._separator)
            try:
                return WordExclusion(parts[1].strip(), int(parts[0].strip()))
            except ValueError:
                pass
        return WordExclusion(exclusion.strip())

    def as_string(self) -> str:
        return self.word if self.index == WordExclusion._no_index else f"""{self.index}{self._separator}{self.word}"""

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, WordExclusion):
            return self.word == other.word and self.index == other.index
        return False

    def __hash__(self) -> int:
        return hash((self.word, self.index))

    def __repr__(self) -> str:
        return f"WordExclusion('{self.word}', {self.index})"

    def covers(self, other: WordExclusion) -> bool:
        return self.word == other.word and (self.index == WordExclusion._no_index or self.index == other.index)

    def to_dict(self) -> dict[str, Any]:
        return {'word': self.word, 'index': self.index}

    @classmethod
    def from_dict(cls, reader: JsonDictReader) -> 'WordExclusion':
        return cls(word=reader.get_string('word'), index=reader.get_int('index'))
