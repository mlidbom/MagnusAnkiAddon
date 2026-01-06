from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots
from language_services.janome_ex.tokenizing.analysis_token import IAnalysisToken

if TYPE_CHECKING:
    from language_services.janome_ex.tokenizing.jn_token import JNToken

# this is the interface that is actually used in the text analysis pipeline

class GodanDictionaryFormStem(IAnalysisToken, Slots):
    def __init__(self,
                 source: JNToken,
                 surface: str,
                 base: str) -> None:
        self.source: JNToken = source
        self._surface: str = surface
        self._base_form: str = base

    # <IAnalysisToken implementation>
    @property
    @override
    def surface(self) -> str: return self._surface
    @property
    @override
    def base_form(self) -> str: return self._base_form
    @property
    @override
    def is_dictionary_verb_form_stem(self) -> bool: return True
    # </IAnalysisToken implementation>

    @override
    def __repr__(self) -> str:
        return f"GodanDictionaryFormStem('{self.surface}', '{self.base_form}')"

class GodanDictionaryFormInflection(IAnalysisToken, Slots):
    def __init__(self,
                 source: JNToken,
                 surface: str,
                 base: str) -> None:
        self.source: JNToken = source
        self._surface: str = surface
        self._base_form: str = base

    # <IAnalysisToken implementation>
    @property
    @override
    def surface(self) -> str: return self._surface
    @property
    @override
    def base_form(self) -> str: return self._base_form
    @property
    @override
    def is_dictionary_verb_inflection(self) -> bool: return True
    # </IAnalysisToken implementation>

    @override
    def __repr__(self) -> str:
        return f"GodanDictionaryFormInflection('{self.surface}', '{self.base_form}')"

class IchidanDictionaryFormStem(IAnalysisToken, Slots):
    def __init__(self,
                 source: JNToken,
                 surface: str,
                 base: str) -> None:
        self.source: JNToken = source
        self._surface: str = surface
        self._base_form: str = base

    # <IAnalysisToken implementation>
    @property
    @override
    def surface(self) -> str: return self._surface
    @property
    @override
    def base_form(self) -> str: return self._base_form
    @property
    @override
    def is_dictionary_verb_form_stem(self) -> bool: return True
    # </IAnalysisToken implementation>

    @override
    def __repr__(self) -> str:
        return f"IchidanDictionaryFormStem('{self.surface}', '{self.base_form}')"

class IchidanDictionaryFormInflection(IAnalysisToken, Slots):
    def __init__(self,
                 source: JNToken,
                 surface: str) -> None:
        self.source: JNToken = source
        self._surface: str = surface

    # <IAnalysisToken implementation>
    @property
    @override
    def surface(self) -> str: return self._surface
    @property
    @override
    def base_form(self) -> str: return self._surface
    @property
    @override
    def is_dictionary_verb_inflection(self) -> bool: return True
    # </IAnalysisToken implementation>

    @override
    def __repr__(self) -> str:
        return f"IchidanDDictionaryFormInflection('{self.surface}', '{self.base_form}')"
