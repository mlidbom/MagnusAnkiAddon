from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from jaslib.language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken

if TYPE_CHECKING:
    from jaslib.language_services.janome_ex.tokenizing.jn_token import JNToken

# this is the interface that is actually used in the text analysis pipeline

class SplitTokenBase(IAnalysisToken, Slots):
    def __init__(self,
                 source: JNToken,
                 surface: str,
                 base: str) -> None:
        self.source: JNToken = source
        self._surface: str = surface
        self._base_form: str = base

    @property
    @override
    def source_token(self) -> JNToken: return self.source
    @property
    @override
    def surface(self) -> str: return self._surface
    @property
    @override
    def base_form(self) -> str: return self._base_form

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.surface}', '{self.base_form}')"

class DictionaryFormsTokenBase(SplitTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_inflectable_word(self) -> bool: return True  # todo: this feels odd, but without it it seems that things go haywire...

class DictionaryFormStem(DictionaryFormsTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_dictionary_verb_form_stem(self) -> bool: return True

class DictionaryFormInflection(DictionaryFormsTokenBase, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_dictionary_verb_inflection(self) -> bool: return True

class GodanDictionaryFormStem(DictionaryFormStem, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

class GodanPotentialDictionaryFormStem(GodanDictionaryFormStem, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_godan_potential_stem(self) -> bool: return True

    @property
    @override
    def is_godan_verb(self) -> bool: return True  # todo this leaves us with, these tokens claiming both to be an ichidan(via the base class) and a godan... We can't tell which, but still..

class GodanDictionaryFormInflection(DictionaryFormInflection, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

class GodanPotentialInflectionDictionaryFormStem(DictionaryFormStem, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

    @property
    @override
    def is_godan_potential_inflection(self) -> bool: return True

class GodanPotentialInflectionDictionaryFormInflection(DictionaryFormInflection, Slots):
    def __init__(self, source: JNToken) -> None:
        super().__init__(source, "る", "る")

class IchidanDictionaryFormStem(DictionaryFormStem, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

class IchidanDictionaryFormInflection(DictionaryFormInflection, Slots):
    def __init__(self, source: JNToken) -> None:
        super().__init__(source, "る", "る")

class KuruVerbDictionaryFormStem(DictionaryFormStem, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

class KuruVerbDictionaryFormInflection(DictionaryFormInflection, Slots):
    def __init__(self, source: JNToken) -> None:
        super().__init__(source, "る", "る")

class SuruVerbDictionaryFormStem(DictionaryFormStem, Slots):
    def __init__(self, source: JNToken, surface: str, base: str) -> None:
        super().__init__(source, surface, base)

class SuruVerbDictionaryFormInflection(DictionaryFormInflection, Slots):
    def __init__(self, source: JNToken) -> None:
        super().__init__(source, "る", "る")
