from __future__ import annotations

from autoslot import Slots
from janome.tokenizer import Token, Tokenizer
from language_services.janome_ex.tokenizing.jn_parts_of_speech import JNPartsOfSpeech
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenized_text import JNTokenizedText
from sysutils import ex_str, typed


class JNTokenizer(Slots):
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    def tokenize(self, text: str) -> JNTokenizedText:
        # apparently janome does not fully understand that invisible spaces are word separators, so we replace them with ordinary spaces
        sanitized_text = text.replace(ex_str.invisible_space, " ")
        tokens = [typed.checked_cast(Token, token) for token in self._tokenizer.tokenize(sanitized_text)]

        return JNTokenizedText(text,
                               tokens,
                               [JNToken(JNPartsOfSpeech.fetch(typed.str_(token.part_of_speech)),
                                        typed.str_(token.base_form),
                                        typed.str_(token.surface),
                                        typed.str_(token.infl_type).replace("*", ""),
                                        typed.str_(token.infl_form).replace("*", ""),
                                        typed.str_(token.reading),
                                        typed.str_(token.phonetic),
                                        typed.str_(token.node_type),
                                        token) for token in tokens])
