from typing import Union

from spacy.tokens import Doc, Token
from unidic2ud import UniDic2UDEntry, UDPipeEntry # type: ignore

from parsing.universal_dependencies.core.ud_token import UDToken
from sysutils.listutils import ListUtils
from sysutils.typed import checked_cast


class UDParseResult:
    def __init__(self, wrapped: Union[UniDic2UDEntry, Doc]):
        self._wrapped = wrapped

        self._wrapped_tokens: Union[list[UDPipeEntry], list[Token]]

        if isinstance(wrapped, Doc):
            sents = [sent for sent in wrapped.sents]
            self._wrapped_sent_tokens:list[list[Token]] = [[token for token in sent] for sent in sents]
            self._wrapped_tokens = ListUtils.flatten_list(self._wrapped_sent_tokens)

            self.tokens = [UDToken(token) for token in self._wrapped_tokens]

            for token in self.tokens:
                # noinspection PyProtectedMember
                token.head = self.tokens[token._head_id]

        if isinstance(wrapped, UniDic2UDEntry):
            self._wrapped_tokens = [token for token in wrapped][1:] # The first is always empty so get rid of it
            self.tokens = [UDToken(token) for token in self._wrapped_tokens]

            for token in self.tokens:
                # noinspection PyProtectedMember
                token.head = self.tokens[token._head_id - 1]


    def to_tree(self) -> str:
        if isinstance(self._wrapped, UniDic2UDEntry):
            return checked_cast(str, self._wrapped.to_tree())
        else:
            return "to_tree_UNSUPPORTED"