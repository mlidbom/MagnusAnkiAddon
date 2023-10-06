from language_services.janome_ex.tokenizing.jn_token import JNToken

class JNTokenizedText:
    def __init__(self, text: str, tokens: list[JNToken]) -> None:
        self.text = text
        self.tokens = tokens
