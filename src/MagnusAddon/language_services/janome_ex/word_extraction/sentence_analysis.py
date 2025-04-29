from typing import Optional

from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils.ex_str import newline

class TextLocation:
    def __init__(self, start_index:int, surface:str, base:str):
        self.start_index = start_index
        self.end_index = start_index + len(surface) - 1
        self.surface = surface
        self.base = base
        self.previous:Optional[TextLocation] = None
        self.next: Optional[TextLocation] = None

    def __repr__(self) -> str:
        return f"TextLocation('{self.start_index}-{self.end_index}, {self.surface} | {self.base}  prev.start:{self.previous.start_index if self.previous else None}, next.start:{self.next.start_index if self.next else None})"

class TokenTextLocation(TextLocation):
    def __init__(self, token: JNToken, start_index:int):
        super().__init__(start_index, token.surface, token.base_form)
        self.token = token

class TextAnalysis:
    _tokenizer = JNTokenizer()

    def __init__(self, sentence:str, exclusions:list[WordExclusion]):
        self.text = sentence
        self.exclusions = exclusions
        self.tokens = self._tokenizer.tokenize(sentence).tokens

        locations:list[TextLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.tokens):
            locations.append(TokenTextLocation(token, character_index))
            character_index += len(token.surface)

        for index, location in enumerate(locations[1:]):
            locations[index].next = location
            locations[index + 1].previous = location

        self.start_location = locations[0]

    def __repr__(self) -> str:
        repr = self.text + newline
        location:Optional[TextLocation] = self.start_location
        while location is not None:
            repr += location.__repr__() + newline
            location = location.next
        return repr