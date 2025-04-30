from typing import Optional

from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_location import TextLocation, TokenTextLocation
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from sysutils.ex_str import newline

class TextAnalysis:
    _tokenizer = JNTokenizer()

    def __init__(self, sentence:str, exclusions:list[WordExclusion]):
        self.text = sentence
        self.exclusions = exclusions
        self.tokens = self._tokenizer.tokenize(sentence).tokens
        self.version = "janome_extractor_1"

        locations:list[TextLocation] = []

        character_index = 0
        for token_index, token in enumerate(self.tokens):
            locations.append(TokenTextLocation(token, character_index))
            character_index += len(token.surface)

        for index, location in enumerate(locations[1:]):
            locations[index].next = location
            locations[index + 1].previous = location

        self.start_location = locations[0]

        self.start_location.run_analysis()

        print("###################")
        print(self)

    def __repr__(self) -> str:
        repr = self.text + newline
        location:Optional[TextLocation] = self.start_location
        while location is not None:
            repr += location.__repr__() + newline
            location = location.next
        return repr