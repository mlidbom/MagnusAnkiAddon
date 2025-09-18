from __future__ import annotations

from typing import final

from ex_autoslot import AutoSlots
from janome.tokenizer import Token, Tokenizer  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.tokenizing.jn_parts_of_speech import JNPartsOfSpeech
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenized_text import JNTokenizedText
from sysutils import ex_str, typed
from sysutils.collections.linq.q_iterable import QList


@final
class JNTokenizer(AutoSlots):
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def tokenize(self, text: str) -> JNTokenizedText:
        # apparently janome does not fully understand that invisible spaces are word separators, so we replace them with ordinary spaces
        sanitized_text = text.replace(ex_str.invisible_space, " ")
        tokens = [typed.checked_cast(Token, token) for token in self._tokenizer.tokenize(sanitized_text)]

        return JNTokenizedText(text,
                               QList(tokens),
                               QList(JNToken(JNPartsOfSpeech.fetch(typed.str_(token.part_of_speech)),  # pyright: ignore[reportAny]
                                             typed.str_(token.base_form),  # pyright: ignore[reportAny]
                                             typed.str_(token.surface),  # pyright: ignore[reportAny]
                                             typed.str_(token.infl_type),  # pyright: ignore[reportAny]
                                             typed.str_(token.infl_form),  # pyright: ignore[reportAny]
                                             typed.str_(token.reading),  # pyright: ignore[reportAny]
                                             typed.str_(token.phonetic),  # pyright: ignore[reportAny]
                                             typed.str_(token.node_type),  # pyright: ignore[reportAny]
                                             token) for token in tokens))
