from typing import Sequence

from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.shared.jatoken import JAToken
from language_services.shared.jatokenizedtext import JATokenizedText

class JNTokenizedText(JATokenizedText):
    def __init__(self, text: str, tokens: list[JNToken]) -> None:
        self.text = text
        self.tokens = tokens

    def get_tokens(self) -> Sequence[JAToken]:
        return self.tokens
