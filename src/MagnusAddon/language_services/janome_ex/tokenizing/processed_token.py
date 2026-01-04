from __future__ import annotations

from typing import override

from autoslot import Slots


class ProcessedToken(Slots):
    def __init__(self, surface: str, base: str,
                 is_non_word_character: bool = False,
                 is_inflectable_word: bool = False,
                 is_godan_potential_stem: bool = False,
                 is_godan_imperative_stem: bool = False,
                 is_ichidan_imperative_stem: bool = False,
                 is_godan_potential_inflection: bool = False,
                 is_godan_imperative_inflection: bool = False,
                 is_ichidan_imperative_inflection: bool = False
                 ) -> None:
        self.surface: str = surface
        self.base_form: str = base
        self.is_inflectable_word: bool = is_inflectable_word
        self.is_non_word_character: bool = is_non_word_character
        self.is_godan_potential_stem: bool = is_godan_potential_stem
        self.is_godan_imperative_stem: bool = is_godan_imperative_stem
        self.is_ichidan_imperative_stem: bool = is_ichidan_imperative_stem
        self.is_godan_potential_inflection: bool = is_godan_potential_inflection
        self.is_godan_imperative_inflection: bool = is_godan_imperative_inflection
        self.is_ichidan_imperative_inflection: bool = is_ichidan_imperative_inflection

    def is_past_tense_stem(self) -> bool: return False
    def is_ichidan_masu_stem(self) -> bool: return False
    def is_te_form_stem(self) -> bool: return self.is_godan_potential_inflection
    def is_past_tense_marker(self) -> bool: return False
    def is_special_nai_negative(self) -> bool: return False

    @property
    def is_masu_stem(self) -> bool: return False

    @override
    def __repr__(self) -> str:
        return f"ProcessedToken('{self.surface}', '{self.base_form}', {self.is_inflectable_word})"
