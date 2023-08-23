from janome.tokenizer import Tokenizer

from parsing.janome_extensions.parts_of_speech import PartsOfSpeech
from parsing.janome_extensions.token_ext import TokenExt
from sysutils import typed


class TokenizedText:
    def __init__(self, text: str, tokens: list[TokenExt]) -> None:
        self.text = text
        self.tokens = tokens


class TokenizerExt:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def tokenize(self, text: str) -> TokenizedText:
        return TokenizedText(text, [token for token in
                                    (TokenExt(typed.str_(token.base_form),
                                              typed.str_(token.surface),
                                              typed.str_(token.infl_type).replace("*", ""),
                                              typed.str_(token.infl_form).replace("*", ""),
                                              typed.str_(token.reading),
                                              typed.str_(token.phonetic),
                                              typed.str_(token.node_type),
                                              PartsOfSpeech.fetch(typed.str_(token.part_of_speech))) for token in self._tokenizer.tokenize(text))
                                    if not token.parts_of_speech.is_noise()])
