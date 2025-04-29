from typing import Union, Any

from language_services.janome_ex.tokenizing.jn_parts_of_speech import PartOfSpeechDescription

class ExtractedWord:
    def __init__(self, word: str, surface: str, character_index:int, parts_of_speech: Union[PartOfSpeechDescription, None] = None) -> None:
        self.word = word
        self.surface = surface
        self.parts_of_speech = parts_of_speech
        self.character_index = character_index

    def surface_length(self) -> int: return len(self.surface)
    def word_length(self) -> int: return len(self.word)

    def __repr__(self) -> str:
        return f"ExtractedWord('{self.word}')"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ExtractedWord):
            return self.word == other.word
        return False

    def __hash__(self) -> int:
        return hash((self.word, self.parts_of_speech))

    def is_surface(self) -> bool:
        return self.word == self.surface