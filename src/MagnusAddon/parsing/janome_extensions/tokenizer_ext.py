from janome.tokenizer import Tokenizer
from parsing.janome_extensions.token_ext import TokenExt


class TokenizedText:
    def __init__(self, text: str, tokens: list[TokenExt]) -> None:
        self.text = text
        self.tokens = tokens



class TokenizerExt:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def tokenize(self, text: str) -> TokenizedText:
        return TokenizedText(text, [token for token in
                                    (TokenExt(tok) for tok in self._tokenizer.tokenize(text))
                                    if not token.parts_of_speech.is_noise()])