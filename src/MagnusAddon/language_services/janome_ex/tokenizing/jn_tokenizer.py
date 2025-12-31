from __future__ import annotations

from typing import final

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from janome.tokenizer import Token, Tokenizer  # pyright: ignore[reportMissingTypeStubs]
from language_services.janome_ex.tokenizing.jn_parts_of_speech import JNPartsOfSpeech
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tokenizing.jn_tokenized_text import JNTokenizedText
from sysutils import ex_str, typed


@final
class JNTokenizer(Slots):
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()

    # apparently janome get's confused by some characters, so we replace them with ordinary spaces
    _character_that_confuses_janome_so_we_replace_them_with_ordinary_full_width_spaces = {ex_str.invisible_space, "!", "！"}

    def tokenize(self, text: str) -> JNTokenizedText:
        # apparently janome does not fully understand that invisible spaces are word separators, so we replace them with ordinary spaces since they are not anything that should need to be parsed...
        sanitized_text = text
        for character in self._character_that_confuses_janome_so_we_replace_them_with_ordinary_full_width_spaces:
            sanitized_text = sanitized_text.replace(character, " ")

        # it seems that janome is sometimes confused and changes its parsing if there is no whitespace after the text, so lets add one
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
                jn_tokens[i]._previous = jn_tokens[i - 1].weak_ref  # pyright: ignore [reportPrivateUsage]
            if i < len(jn_tokens) - 1:
                jn_tokens[i]._next = jn_tokens[i + 1].weak_ref  # pyright: ignore [reportPrivateUsage]

        return JNTokenizedText(text, tokens, jn_tokens)
