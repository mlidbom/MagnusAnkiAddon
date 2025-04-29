from typing import Sequence, Union
from unidic2ud import UniDic2UDEntry, UDPipeEntry # type: ignore

from language_services.shared.jatoken import JAToken
from language_services.shared.jatokenizedtext import JATokenizedText
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from sysutils import ex_sequence, ex_str
from sysutils.typed import str_

class UDTokenizedText(JATokenizedText):
    def __init__(self, wrapped: UniDic2UDEntry):
        self._wrapped = wrapped

        self._wrapped_tokens: list[UDPipeEntry]

        self._wrapped_tokens = [token for token in wrapped][1:] # The first is always empty so get rid of it
        self.tokens = [UDToken(token) for token in self._wrapped_tokens]

        for token in self.tokens:
            # noinspection PyProtectedMember
            token.head = self.tokens[token._head_id - 1]

    def __str__(self) -> str:
        return self.str_()

    def str_(self, exclude_lemma_and_norm:bool = False) -> str:
        return "\n".join([tok.str_(ex_str.pad_to_length, exclude_lemma_and_norm) for tok in self.tokens])

    #This is super useful for debugging. It's not going unless we remove unidic alltogether.
    # noinspection PyUnusedFunction
    def to_tree(self) -> str:
        if isinstance(self._wrapped, UniDic2UDEntry):
            return str_(self._wrapped.to_tree())
        else:
            return "to_tree_UNSUPPORTED"

    def get_tokens(self) -> Sequence[JAToken]:
        return self.tokens