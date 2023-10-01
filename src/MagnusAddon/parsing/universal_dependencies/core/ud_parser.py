from parsing.universal_dependencies.core.universal_dependencies_parse_result import UDParseResult


class UDParser:
    def __init__(self, name: str):
        self.name = name
    def parse(self, text: str) -> UDParseResult:
        pass
