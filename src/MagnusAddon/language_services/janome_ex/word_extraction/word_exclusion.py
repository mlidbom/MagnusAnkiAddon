from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.hierarchicalword import HierarchicalWord
    from sysutils.ex_json import JsonDictReader

from typing import Any


class WordExclusion:
    secret = "aoesunth9cgrcgf"
    _no_index = -1
    def __init__(self, word: str, index: int, _secret:str) -> None:
        if _secret != "aoesunth9cgrcgf": raise ValueError("please use the factory methods instead of this private constructor")
        self.word = word
        self.index = index

    def excludes(self, word: HierarchicalWord) -> bool:
        return word.word.word == self.word and (self.index == WordExclusion._no_index or self.index == word.word.character_index)

    def excludes_form_at_index(self, form: str, index: int) -> bool:
        return form == self.word and (self.index == WordExclusion._no_index or self.index == index)

    @classmethod
    def global_(cls, exclusion: str) -> WordExclusion: return WordExclusion(exclusion.strip(), WordExclusion._no_index, WordExclusion.secret)
    @classmethod
    def at_index(cls, exclusion: str, index: int) -> WordExclusion: return WordExclusion(exclusion.strip(), index, WordExclusion.secret)

    def __eq__(self, other: object) -> bool:
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
        return {"word": self.word, "index": self.index}

    @classmethod
    def from_reader(cls, reader: JsonDictReader) -> WordExclusion:
        return cls(word=reader.string("word"), index=reader.int("index"), _secret=WordExclusion.secret)
