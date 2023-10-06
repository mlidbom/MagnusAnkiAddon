from language_services.universal_dependencies.shared.tokenizing.ud_tokenized_text import UDTokenizedText


class UDTokenizer:
    def __init__(self, name: str):
        self.name = name
    def parse(self, text: str) -> UDTokenizedText: raise Exception("Should have been overridden")
