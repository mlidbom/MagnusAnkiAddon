from typing import Union, Any

from language_services.janome_ex.tokenizing.jn_parts_of_speech import PartOfSpeechDescription
from sysutils import kana_utils


class ExtractedWord:
    def __init__(self, word: str, parts_of_speech: Union[PartOfSpeechDescription, None] = None) -> None:
        self.word = word
        self.parts_of_speech = parts_of_speech

    def is_kana_only(self) -> bool: return kana_utils.is_only_kana(self.word)
    def to_hiragana(self) -> str: return kana_utils.to_hiragana(self.word)

    def __repr__(self) -> str:
        return f"ParsedWord('{self.word}')"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ExtractedWord):
            return self.word == other.word
        return False

    def __hash__(self) -> int:
        return hash((self.word, self.parts_of_speech))