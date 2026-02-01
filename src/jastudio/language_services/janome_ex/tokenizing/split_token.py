from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.tokenizing.godan_dictionary_form_stem import SplitTokenBase

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken

#todo replace this jack of all trades class with custom classes
class SplitToken(SplitTokenBase, Slots):
    def __init__(self,
                 source: JNToken,
                 surface: str,
                 base: str,
                 is_non_word_character: bool = False,
                 is_inflectable_word: bool = False,
                 is_godan_potential_stem: bool = False,
                 is_godan_imperative_stem: bool = False,
                 is_ichidan_imperative_stem: bool = False,
                 is_godan_potential_inflection: bool = False,
                 is_godan_imperative_inflection: bool = False,
                 is_ichidan_imperative_inflection: bool = False) -> None:
        super().__init__(source, surface, base)

        self._is_inflectable_word: bool = is_inflectable_word
        self._is_non_word_character: bool = is_non_word_character
        self._is_godan_potential_stem: bool = is_godan_potential_stem
        self._is_godan_imperative_stem: bool = is_godan_imperative_stem
        self._is_ichidan_imperative_stem: bool = is_ichidan_imperative_stem
        self._is_godan_potential_inflection: bool = is_godan_potential_inflection
        self._is_godan_imperative_inflection: bool = is_godan_imperative_inflection
        self._is_ichidan_imperative_inflection: bool = is_ichidan_imperative_inflection

    # <IAnalysisToken implementation>
    @property
    @override
    def has_te_form_stem(self) -> bool: return self.is_godan_potential_inflection
    @property
    @override
    def is_inflectable_word(self) -> bool: return self._is_inflectable_word
    @property
    @override
    def is_non_word_character(self) -> bool: return self._is_non_word_character
    @property
    @override
    def is_godan_verb(self) -> bool: return self.is_godan_potential_stem or self.is_godan_imperative_stem or self.is_godan_potential_inflection or self.is_godan_imperative_inflection
    @property
    @override
    def is_ichidan_verb(self) -> bool: return self.is_ichidan_imperative_stem or self.is_ichidan_imperative_inflection
    @property
    @override
    def is_godan_potential_stem(self) -> bool: return self._is_godan_potential_stem
    @property
    @override
    def is_godan_imperative_stem(self) -> bool: return self._is_godan_imperative_stem
    @property
    @override
    def is_ichidan_imperative_stem(self) -> bool: return self._is_ichidan_imperative_stem
    @property
    @override
    def is_godan_potential_inflection(self) -> bool: return self._is_godan_potential_inflection
    @property
    @override
    def is_godan_imperative_inflection(self) -> bool: return self._is_godan_imperative_inflection
    @property
    @override
    def is_ichidan_imperative_inflection(self) -> bool: return self._is_ichidan_imperative_inflection
    # </IAnalysisToken implementation>
