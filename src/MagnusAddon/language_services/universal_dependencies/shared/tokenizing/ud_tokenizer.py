from language_services.shared.jatokenizer import JATokenizer
from language_services.universal_dependencies.shared.tokenizing.ud_tokenized_text import UDTokenizedText


class UDTokenizer(JATokenizer):
    def __init__(self, name: str):
        self.name = name
    def tokenize(self, text: str) -> UDTokenizedText: raise Exception("Should have been overridden")
