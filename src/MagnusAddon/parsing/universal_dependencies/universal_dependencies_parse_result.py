from typing import Union

from spacy.tokens import Doc, Token
from unidic2ud import UniDic2UDEntry, UDPipeEntry

from parsing.universal_dependencies.universal_dependencies_token import UDToken


class UniversalDependenciesParseResult:
    def __init__(self, wrapped: Union[UniDic2UDEntry, Doc]):

        if isinstance(wrapped, Doc):
            self._wrapped = wrapped

            sents = [sent for sent in wrapped.sents]
            if len(sents) != 1:
                raise Exception(f"No idea how to handle {len(sents)} sents")

            self._wrapped_tokens:list[Token] = [token for token in sents[0]]

            self.tokens = [UDToken(token) for token in self._wrapped_tokens]

        if isinstance(wrapped, UniDic2UDEntry):
            self._wrapped = wrapped
            self._wrapped_tokens:list[UDPipeEntry] = [token for token in wrapped]
            self.tokens = [UDToken(token) for token in self._wrapped_tokens]

        for token in self.tokens:
            # noinspection PyProtectedMember
            token.head = self.tokens[token._head_id]

    def to_tree(self) -> str:
        if isinstance(self._wrapped, UniDic2UDEntry):
            return self._wrapped.to_tree()
        else:
            return "to_tree_UNSUPPORTED"