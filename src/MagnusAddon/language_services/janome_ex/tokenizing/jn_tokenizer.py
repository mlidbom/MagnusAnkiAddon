from __future__ import annotations

from typing import final

from janome.tokenizer import Token, Tokenizer  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.tokenizing.jn_parts_of_speech import JNPartsOfSpeech
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenized_text import JNTokenizedText
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils import ex_str, typed
from typed_linq_collections.collections.q_list import QList


@final
class JNTokenizer(Slots):
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def tokenize(self, text: str) -> JNTokenizedText:
        # apparently janome does not fully understand that invisible spaces are word separators, so we replace them with ordinary spaces
        sanitized_text = text.replace(ex_str.invisible_space, " ")
        tokens = [typed.checked_cast(Token, token) for token in self._tokenizer.tokenize(sanitized_text)]

        # Create JNToken objects
        jn_tokens = [JNToken(JNPartsOfSpeech.fetch(typed.str_(token.part_of_speech)),  # pyright: ignore[reportAny]
                             typed.str_(token.base_form),  # pyright: ignore[reportAny]
                             typed.str_(token.surface),  # pyright: ignore[reportAny]
                             typed.str_(token.infl_type),  # pyright: ignore[reportAny]
                             typed.str_(token.infl_form),  # pyright: ignore[reportAny]
                             typed.str_(token.reading),  # pyright: ignore[reportAny]
                             typed.str_(token.phonetic),  # pyright: ignore[reportAny]
                             typed.str_(token.node_type),  # pyright: ignore[reportAny]
                             token) for token in tokens]

        # Link tokens with previous/next pointers
        for i in range(len(jn_tokens)):
            if i > 0:
                jn_tokens[i].previous = jn_tokens[i - 1]
            if i < len(jn_tokens) - 1:
                jn_tokens[i].next = jn_tokens[i + 1]

        return JNTokenizedText(text,
                               QList(tokens),
                               QList(jn_tokens))
