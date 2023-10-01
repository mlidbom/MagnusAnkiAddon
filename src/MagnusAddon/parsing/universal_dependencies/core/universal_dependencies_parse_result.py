from typing import Union

from spacy.tokens import Doc, Token
from unidic2ud import UniDic2UDEntry, UDPipeEntry

from parsing.universal_dependencies.core.ud_token import UDToken
from sysutils.listutils import ListUtils


class UDParseResult:
    def __init__(self, wrapped: Union[UniDic2UDEntry, Doc]):

        if isinstance(wrapped, Doc):
            self._wrapped = wrapped

            sents = [sent for sent in wrapped.sents]
            self._wrapped_sent_tokens:list[list[Token]] = [[token for token in sent] for sent in sents]
            self._wrapped_tokens:list[Token] = ListUtils.flatten_list(self._wrapped_sent_tokens)

            self.tokens = [UDToken(token) for token in self._wrapped_tokens]

        if isinstance(wrapped, UniDic2UDEntry):
            self._wrapped = wrapped
            self._wrapped_tokens:list[UDPipeEntry] = [token for token in wrapped]
            self.tokens = [UDToken(token) for token in self._wrapped_tokens] # The first is always empty

        for token in self.tokens:
            # noinspection PyProtectedMember
            token.head = self.tokens[token._head_id]

        if isinstance(wrapped, UniDic2UDEntry):
            self.tokens = self.tokens[1:] # The first is always empty so get rid of it

    def to_tree(self) -> str:
        if isinstance(self._wrapped, UniDic2UDEntry):
            return self._wrapped.to_tree()
        else:
            return "to_tree_UNSUPPORTED"