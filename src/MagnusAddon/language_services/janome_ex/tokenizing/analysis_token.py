from __future__ import annotations

from autoslot import Slots


class IAnalysisToken(Slots):
    @property
    def is_past_tense_stem(self) -> bool: raise NotImplementedError()
    @property
    def is_ichidan_masu_stem(self) -> bool: raise NotImplementedError()
    @property
    def is_te_form_stem(self) -> bool: raise NotImplementedError()
    @property
    def is_past_tense_marker(self) -> bool: raise NotImplementedError()
    @property
    def is_special_nai_negative(self) -> bool: raise NotImplementedError()
    @property
    def is_godan_potential_stem(self) -> bool: raise NotImplementedError()
    @property
    def is_godan_potential_inflection(self) -> bool: raise NotImplementedError()
    @property
    def is_ichidan_imperative_stem(self) -> bool: raise NotImplementedError()
    @property
    def surface(self) -> str: raise NotImplementedError()
    @property
    def base_form(self) -> str: raise NotImplementedError()
    @property
    def is_inflectable_word(self) -> bool: raise NotImplementedError()
    @property
    def is_non_word_character(self) -> bool: raise NotImplementedError()
    @property
    def is_godan_imperative_inflection(self) -> bool: raise NotImplementedError()
    @property
    def is_ichidan_imperative_inflection(self) -> bool: raise NotImplementedError()
    @property
    def is_godan_imperative_stem(self) -> bool: raise NotImplementedError()
    @property
    def is_masu_stem(self) -> bool: raise NotImplementedError()
