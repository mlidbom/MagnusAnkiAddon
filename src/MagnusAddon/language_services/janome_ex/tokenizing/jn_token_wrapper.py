from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.tokenizing.processed_token import SplitToken

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken

class JNTokenWrapper(SplitToken, Slots):
    def __init__(self, token: JNToken) -> None:
        super().__init__(token, token.surface, token.base_form, is_non_word_character=token.is_non_word_character, is_inflectable_word=token.is_inflectable_word)
        self.token: JNToken = token

    @property
    @override
    def is_past_tense_stem(self) -> bool: return self.token.is_past_tense_stem
    @property
    @override
    def is_te_form_stem(self) -> bool: return self.token.is_te_form_stem
    @property
    @override
    def is_ichidan_masu_stem(self) -> bool: return self.token.is_ichidan_masu_stem
    @property
    @override
    def is_past_tense_marker(self) -> bool: return self.token.is_past_tense_marker
    @property
    @override
    def is_special_nai_negative(self) -> bool: return self.token.is_special_nai_negative

    @property
    @override
    def is_masu_stem(self) -> bool: return self.token.is_masu_stem
