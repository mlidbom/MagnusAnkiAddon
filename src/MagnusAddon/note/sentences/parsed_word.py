from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from sysutils.ex_json import JsonDictReader


class ParsedWord:
    def __init__(self, word: str) -> None:
        self.word = word

    def to_dict(self) -> dict[str, Any]: return {'word': self.word}

    @classmethod
    def from_json(cls, reader: JsonDictReader) -> ParsedWord: return cls(reader.get_string('word'))
