from janome.tokenizer import Tokenizer

from parsing.janome_extensions.token_ext import TokenExt


class TokenizerExt:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def tokenize(self, text: str) -> list[TokenExt]:
        return [TokenExt(token) for token in self._tokenizer.tokenize(text)]