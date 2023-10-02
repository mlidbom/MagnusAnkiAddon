from unidic2ud import unidic2ud  # type: ignore

from parsing.universal_dependencies.core.ud_parser import UDParser
from parsing.universal_dependencies.core.universal_dependencies_parse_result import UDParseResult
from sysutils.lazy import Lazy


class UD2UDParser(UDParser):
    def __init__(self, name: str):
        super().__init__(name)
        self._lazy_parser = Lazy(lambda: unidic2ud.load(name if name != "built-in" else None))

    def parse(self, text: str) -> UDParseResult:
        return UDParseResult(self._lazy_parser.instance()(text))
