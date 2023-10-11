from unidic2ud import unidic2ud  # type: ignore

from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.shared.tokenizing.ud_tokenized_text import UDTokenizedText
from sysutils.lazy import Lazy


class UD2UDTokenizer(UDTokenizer):
    def __init__(self, name: str):
        super().__init__(name)
        self._lazy_parser = Lazy(lambda: unidic2ud.load(name if name != "built-in" else None))

    def tokenize(self, text: str) -> UDTokenizedText:
        return UDTokenizedText(self._lazy_parser.instance()(text))
