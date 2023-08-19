from janome.tokenizer import Tokenizer
from parsing.janome_extensions.token_ext import TokenExt


class TokenizerExt:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def tokenize(self, text: str) -> list[TokenExt]:
        return [token for token in
                (TokenExt(tok) for tok in self._tokenizer.tokenize(text))
                if not token.parts_of_speech.is_noise()]