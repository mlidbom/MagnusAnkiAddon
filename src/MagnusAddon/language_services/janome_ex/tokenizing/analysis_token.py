from __future__ import annotations

from autoslot import Slots


# the interface that is used in the text analysis pipeline, defaults to returning False for all bool properties
# and inheritors get to override whatever properties they can.
class IAnalysisToken(Slots):
    @property
    def surface(self) -> str: raise NotImplementedError()
    @property
    def base_form(self) -> str: raise NotImplementedError()
    @property
    def is_past_tense_stem(self) -> bool: return False
    @property
    def is_ichidan_masu_stem(self) -> bool: return False
    @property
    def is_te_form_stem(self) -> bool: return False
    @property
    def is_past_tense_marker(self) -> bool: return False
    @property
    def is_special_nai_negative(self) -> bool: return False
    @property
    def is_inflectable_word(self) -> bool: return False
    @property
    def is_non_word_character(self) -> bool: return False

    # <Only true for split tokens>
    @property
    def is_godan_potential_stem(self) -> bool: return False
    @property
    def is_godan_imperative_stem(self) -> bool: return False
    @property
    def is_ichidan_imperative_stem(self) -> bool: return False
    @property
    def is_godan_potential_inflection(self) -> bool: return False
    @property
    def is_godan_imperative_inflection(self) -> bool: return False
    @property
    def is_ichidan_imperative_inflection(self) -> bool: return False
    # </Only true for split tokens>

    @property
    def is_masu_stem(self) -> bool: raise NotImplementedError()
