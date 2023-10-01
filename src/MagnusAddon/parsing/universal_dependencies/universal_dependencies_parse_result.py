from typing import Union

from unidic2ud import UniDic2UDEntry, UDPipeEntry

from parsing.universal_dependencies.universal_dependencies_token import UDToken


class UniversalDependenciesParseResult:
    def __init__(self, wrapped: Union[UniDic2UDEntry]):

        if isinstance(wrapped, UniDic2UDEntry):
            self._wrapped = wrapped
            self._wrapped_tokens:list[UDPipeEntry] = [token for token in wrapped]
            self.tokens = [UDToken(token) for token in self._wrapped_tokens]

        for token in self.tokens:
            token.head = self.tokens[token.head_id]

    def to_tree(self) -> str:
        if isinstance(self._wrapped, UniDic2UDEntry):
            return self._wrapped.to_tree()
        else:
            return "to_tree_UNSUPPORTED"