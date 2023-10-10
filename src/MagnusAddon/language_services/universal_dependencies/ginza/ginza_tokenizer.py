import spacy

from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tokenizing.ud_tokenized_text import UDTokenizedText
from sysutils.ex_str import full_width_space
from sysutils.lazy import Lazy


class GinzaTokenizer(UDTokenizer):
    def __init__(self) -> None:
        super().__init__("ginza")
        self._lazy_parser = Lazy(lambda: spacy.load("ja_ginza"))

    def tokenize(self, text: str) -> UDTokenizedText:
        text = text.replace(" ", "").replace(full_width_space, "")
        return UDTokenizedText(self._lazy_parser.instance()(text))
