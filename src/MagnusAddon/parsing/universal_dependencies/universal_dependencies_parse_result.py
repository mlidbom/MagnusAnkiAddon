from unidic2ud import UniDic2UDEntry, UDPipeEntry

from parsing.universal_dependencies.universal_dependencies_token import UD2UDToken


class UniversalDependenciesParseResult:
    def __init__(self, wrapped: UniDic2UDEntry):
        self._wrapped = wrapped
        self._wrapped_tokens:list[UDPipeEntry] = [token for token in wrapped]
        self.tokens = [UD2UDToken(token) for token in self._wrapped_tokens]

        for token in self.tokens:
            token.head = self.tokens[token.head_id]

    def to_tree(self) -> str:
        return self._wrapped.to_tree()