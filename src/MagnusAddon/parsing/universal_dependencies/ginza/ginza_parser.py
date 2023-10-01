import spacy

from parsing.universal_dependencies.core.ud_parser import UDParser
from parsing.universal_dependencies.core.universal_dependencies_parse_result import UDParseResult
from sysutils.lazy import Lazy


class GinzaParser(UDParser):
    def __init__(self) -> None:
        super().__init__("ginza")
        self._lazy_parser = Lazy(lambda: spacy.load("ja_ginza"))

    def parse(self, text: str) -> UDParseResult:
        text = text.replace(" ", "").replace("　", "")
        return UDParseResult(self._lazy_parser.instance()(text))
